# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import glob
import importlib
import json
import logging
import os
import shutil
import subprocess
import sys
import tempfile
from distutils import dir_util
from distutils.spawn import find_executable
from multiprocessing import Process

import coloredlogs
import git
import pytesseract

import firefox.app as fa
import firefox.downloader as fd
import firefox.extractor as fe
from api.core.key import Key, shutdown_process
from api.core.platform import Platform
from api.core.profile import Profile
from api.core.settings import Settings
from api.core.util.core_helper import get_module_dir, get_platform, get_run_id, get_current_run_dir, filter_list
from api.core.util.parse_args import parse_args
from api.core.util.test_loader import load_tests, scan_all_tests
from api.helpers.general import launch_firefox, quit_firefox, confirm_firefox_quit
from firefox import cleanup
from local_web_server import LocalWebServer
from test_runner import run

tmp_dir = None
restore_terminal_encoding = None
LOG_FILENAME = 'iris_log.log'
LOG_FORMAT = '%(asctime)s [%(levelname)s] [%(name)s] %(message)s'
logger = logging.getLogger(__name__)

coloredlogs.DEFAULT_LOG_FORMAT = LOG_FORMAT
coloredlogs.DEFAULT_FIELD_STYLES = {'levelname': {'color': 'cyan', 'bold': True},
                                    'name': {'color': 'cyan', 'bold': True}}
coloredlogs.DEFAULT_LEVEL_STYLES = {'warning': {'color': 'yellow', 'bold': True},
                                    'success': {'color': 'green', 'bold': True},
                                    'error': {'color': 'red', 'bold': True}}


def main():
    """This is the main entry point defined in setup.py"""
    Iris()


class Iris(object):

    def __init__(self):
        cleanup.init()
        Iris.fix_terminal_encoding()
        self.initialize_platform()
        self.verify_config()
        self.control_center()
        self.initialize_run()
        run(self)

    def verify_config(self):
        self.check_keyboard_state()
        self.init_tesseract_path()
        self.check_7zip()

    def initialize_platform(self):
        self.args = parse_args()
        self.module_dir = get_module_dir()
        self.platform = get_platform()
        self.os = Settings.get_os()
        self.create_working_directory()
        self.create_run_directory()
        initialize_logger(LOG_FILENAME, self.args.level)
        self.clear_profile_cache()
        self.process_list = []
        self.local_web_root = os.path.join(self.module_dir, 'iris', 'local_web')
        self.base_local_web_url = 'http://127.0.0.1:%s' % self.args.port
        self.create_test_json()
        self.create_arg_json()

    def control_center(self):
        if self.args.control:
            # Copy web assets to working directory.
            dir_util.copy_tree(os.path.join(self.module_dir, 'iris', 'cc_files'), self.args.workdir)
            # Copy profile for Firefox.
            profile_path = os.path.join(self.args.workdir, 'cc_profile')
            if not os.path.exists(profile_path):
                Profile.get_staged_profile(Profile.LIKE_NEW, profile_path)

            # Open local installation of Firefox.
            if Settings.get_os() == Platform.MAC:
                fx_path = '/Applications/Firefox.app/Contents/MacOS/firefox'
            elif Settings.get_os() == Platform.WINDOWS:
                if os.path.exists('C:\\Program Files (x86)\\Mozilla Firefox\\firefox'):
                    fx_path = 'C:\\Program Files (x86)\\Mozilla Firefox\\firefox'
                else:
                    fx_path = 'C:\\Program Files\\Mozilla Firefox'
            else:
                fx_path = '/usr/lib/firefox/firefox'

            launch_firefox(fx_path, profile=profile_path, url=self.base_local_web_url)
            server = LocalWebServer(self.args.workdir, self.args.port)

            # Iris waits for the user to make a choice in the control center. Once they
            # make a decision, Firefox will quit.
            quit_firefox()

            # Check the result of the user's decision. If they have chosen to run tests,
            # we will continue. Otherwise, abort the current run.
            if server.result is not None:
                # Temporary - we will parse this returned value and turn it into runtime data.
                print server.result
            else:
                # Temporary - we will quit Iris gracefully and clean up.
                print "Nothing"

        return

    def initialize_run(self):
        self.start_local_web_server(self.local_web_root, self.args.port)
        self.get_firefox()
        self.update_run_index()
        self.update_run_log()
        load_tests(self)
        self.current_test = 0
        self.total_tests = len(self.test_list)

    def get_firefox(self):
        global tmp_dir
        tmp_dir = self.__create_tempdir()

        if self.args.firefox == 'local':
            # Use default Firefox installation
            logger.info('Running with default installed Firefox build')
            if Settings.get_os() == Platform.MAC:
                self.fx_app = self.get_test_candidate('/Applications/Firefox.app/Contents')
            elif Settings.get_os() == Platform.WINDOWS:
                if os.path.exists('C:\\Program Files (x86)\\Mozilla Firefox'):
                    self.fx_app = self.get_test_candidate('C:\\Program Files (x86)\\Mozilla Firefox')
                else:
                    self.fx_app = self.get_test_candidate('C:\\Program Files\\Mozilla Firefox')
            else:
                self.fx_app = self.get_test_candidate('/usr/lib/firefox')
        else:
            self.fx_app = self.get_test_candidate(self.args.firefox)

        self.fx_channel = self.fx_app.release
        self.fx_path = self.fx_app.exe
        self.version = self.fx_app.version
        self.build_id = self.fx_app.build_id
        self.fx_locale = self.args.locale

    def create_working_directory(self):
        # Create workdir (usually ~/.iris, used for caching etc.)
        # Assumes that no previous code will write to it.
        if not os.path.exists(self.args.workdir):
            logger.debug('Creating working directory %s' % self.args.workdir)
            os.makedirs(self.args.workdir)
        if not os.path.exists(os.path.join(self.args.workdir, 'js')):
            os.makedirs(os.path.join(self.args.workdir, 'js'))

    def create_run_directory(self):
        master_run_directory = os.path.join(self.args.workdir, 'runs')
        if self.args.clear:
            if os.path.exists(master_run_directory):
                shutil.rmtree(master_run_directory, ignore_errors=True)
        if not os.path.exists(master_run_directory):
            os.mkdir(master_run_directory)
        run_directory = os.path.join(master_run_directory, get_run_id())
        os.mkdir(run_directory)

    def clear_profile_cache(self):
        profile_temp = os.path.join(parse_args().workdir, 'cache', 'profiles')
        if os.path.exists(profile_temp):
            shutil.rmtree(profile_temp, ignore_errors=True)

    def update_run_index(self, new_data=None):
        # Prepare the current entry.
        current_run = {}
        current_run['id'] = get_run_id()
        current_run['version'] = self.version
        current_run['build'] = self.build_id
        current_run['channel'] = self.fx_channel
        current_run['locale'] = self.fx_locale

        # If this run is just starting, initialize with blank values
        # to indicate incomplete run.
        if new_data is None:
            logger.debug('Updating runs.json with initial run data.')
            current_run['total'] = '*'
            current_run['failed'] = '*'
        else:
            logger.debug('Updating runs.json with completed run data.')
            current_run['total'] = new_data['total']
            current_run['failed'] = new_data['failed']

        # Temporary code to deal with legacy runs.json file.
        # It will be removed before launch.
        old_run_file = os.path.join(parse_args().workdir, 'js', 'runs.json')
        if os.path.exists(old_run_file):
            os.remove(old_run_file)

        run_file = os.path.join(parse_args().workdir, 'js', 'all_runs.json')

        if os.path.exists(run_file):
            logger.debug('Updating run file: %s' % run_file)
            with open(run_file, 'r') as f:
                run_file_data = json.load(f)
            for run in run_file_data['runs']:
                if run['id'] == get_run_id():
                    run_file_data['runs'].remove(run)
            run_file_data['runs'].append(current_run)
        else:
            logger.debug('Creating run file: %s' % run_file)
            run_file_data = {'runs': []}
            run_file_data['runs'].append(current_run)

        with open(run_file, 'w') as f:
            json.dump(run_file_data, f, sort_keys=True, indent=True)

    def update_run_log(self, new_data=None):
        # Prepare the current entry.
        meta = {}
        meta['run_id'] = get_run_id()
        meta['fx_version'] = self.version
        meta['fx_build_id'] = self.build_id
        meta['platform'] = self.os
        meta['channel'] = self.fx_channel
        meta['locale'] = self.fx_locale
        meta['args'] = ' '.join(sys.argv)
        meta['params'] = vars(self.args)
        meta['log'] = os.path.join(get_current_run_dir(), 'iris_log.log')

        repo = git.Repo(self.module_dir)
        meta['iris_version'] = 0.1
        meta['iris_repo'] = repo.working_tree_dir
        meta['iris_branch'] = repo.active_branch.name
        meta['iris_branch_head'] = repo.head.object.hexsha

        # If this run is just starting, initialize with blank values
        # to indicate incomplete run.
        if new_data is None:
            logger.debug('Updating run.json with initial run data.')
            meta['total'] = 0
            meta['passed'] = 0
            meta['failed'] = 0
            meta['skipped'] = 0
            meta['errors'] = 0
            meta['start_time'] = 0
            meta['end_time'] = 0
            meta['total_time'] = 0
            tests = []
        else:
            logger.debug('Updating runs.json with completed run data.')
            meta['total'] = new_data['total']
            meta['passed'] = new_data['passed']
            meta['failed'] = new_data['failed']
            meta['skipped'] = new_data['skipped']
            meta['errors'] = new_data['errors']
            meta['start_time'] = new_data['start_time']
            meta['end_time'] = new_data['end_time']
            meta['total_time'] = new_data['total_time']
            tests = new_data['tests']

        run_file = os.path.join(get_current_run_dir(), 'run.json')
        run_file_data = {}
        run_file_data['meta'] = meta
        run_file_data['tests'] = tests

        with open(run_file, 'w') as f:
            json.dump(run_file_data, f, sort_keys=True, indent=True)

    def create_test_json(self):
        self.all_tests = []
        self.all_packages = []
        self.all_tests, self.all_packages = scan_all_tests(self.args.directory)
        self.master_test_list = {}
        for package in self.all_packages:
            self.master_test_list[os.path.basename(package)] = []

        for index, module in enumerate(self.all_tests, start=1):
            try:
                current_module = importlib.import_module(module)
                current_test = current_module.Test(self)
                current_package = os.path.basename(os.path.dirname(current_module.__file__))

                test_object = {}
                test_object['name'] = module
                test_object['module'] = current_module.__file__
                test_object['meta'] = current_test.meta
                test_object['package'] = current_package

                if current_test.fx_version is '':
                    test_object['fx_version'] = 'all'
                else:
                    test_object['fx_version'] = current_test.fx_version

                test_object['platform'] = filter_list(current_test.platform, current_test.exclude)
                test_object['channel'] = filter_list(current_test.channel, current_test.exclude)
                test_object['locale'] = filter_list(current_test.locale, current_test.exclude)
                test_object['enabled'] = self.os in filter_list(current_test.platform, current_test.exclude)
                test_object['test_case_id'] = current_test.test_case_id
                test_object['test_suite_id'] = current_test.test_suite_id
                test_object['blocked_by'] = current_test.blocked_by
                self.master_test_list[current_package].append(test_object)
            except AttributeError as e:
                print e.args
                logger.warning('[%s] is not a test file. Skipping...', module)

        test_log_file = os.path.join(self.args.workdir, 'js', 'all_tests.json')
        with open(test_log_file, 'w') as f:
            json.dump(self.master_test_list, f, sort_keys=True, indent=True)

    def create_arg_json(self):
        arg_data = {}
        arg_data['email'] = {'type': 'bool', 'value': ['true', 'false'], 'default': 'false'}
        arg_data['firefox'] = {'type': 'str', 'value': ['local', 'release', 'esr', 'beta', 'nightly'],
                               'default': 'release'}
        arg_data['highlight'] = {'type': 'bool', 'value': ['true', 'false'], 'default': 'false'}
        arg_data['level'] = {'type': 'str', 'value': ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG'],
                             'default': 'INFO'}
        arg_data['locale'] = {'type': 'str', 'value': ['en-us'], 'default': 'en-us'}
        arg_data['mouse'] = {'type': 'float', 'value': ['0.0', '0.5', '1.0', '2.0'], 'default': '0.5'}
        arg_data['override'] = {'type': 'bool', 'value': ['true', 'false'], 'default': 'false'}
        arg_data['port'] = {'type': 'int', 'value': ['2000'], 'default': '2000'}
        arg_data['report'] = {'type': 'bool', 'value': ['true', 'false'], 'default': 'false'}
        arg_data['rerun'] = {'type': 'bool', 'value': ['true', 'false'], 'default': 'false'}
        arg_data['save'] = {'type': 'bool', 'value': ['true', 'false'], 'default': 'false'}

        arg_log_file = os.path.join(self.args.workdir, 'js', 'all_args.json')
        with open(arg_log_file, 'w') as f:
            json.dump(arg_data, f, sort_keys=True, indent=True)

    def start_local_web_server(self, path, port):
        """
        Web servers are spawned in new Process instances, which
        must be saved in a list in order to be terminated later.
        """
        try:
            logger.debug('Starting local web server on port %s for directory %s' % (port, path))
            web_server_process = Process(target=LocalWebServer, args=(path, port,))
            self.process_list.append(web_server_process)
            web_server_process.start()
        except IOError:
            logger.critical('Unable to launch local web server, aborting Iris.')
            self.finish(code=13)

    def write_test_failures(self, failures):
        master_run_directory = os.path.join(self.args.workdir, 'runs')
        path = os.path.join(master_run_directory, 'last_fail.txt')

        if len(failures):
            last_fail = open(path, 'w')
            for item in failures:
                    for package in self.master_test_list:
                        for test in self.master_test_list[package]:
                            if test["name"] in item:
                                last_fail.write(test["module"] + '\n')
            last_fail.close()

    def finish(self, code=0):
        """
        All exit points of Iris need to call this function in order to exit properly.
        """
        if hasattr(self, 'process_list'):
            logger.debug('There are %s queued process(es) to terminate.' % len(self.process_list))
            for process in self.process_list:
                logger.debug('Terminating process.')
                process.terminate()
                process.join()
        sys.exit(code)

    def check_keyboard_state(self):
        is_lock_on = False
        if Settings.get_os() != Platform.MAC:
            if Key.is_lock_on(Key.CAPS_LOCK):
                logger.error('Cannot run Iris because Key.CAPS_LOCK is on. Please turn it off to continue.')
                is_lock_on = True
            if Key.is_lock_on(Key.NUM_LOCK):
                logger.error('Cannot run Iris because Key.NUM_LOCK is on. Please turn it off to continue.')
                is_lock_on = True
            if Key.is_lock_on(Key.SCROLL_LOCK):
                logger.error('Cannot run Iris because Key.SCROLL_LOCK is on. Please turn it off to continue.')
                is_lock_on = True
        else:
            try:
                cmd = subprocess.Popen('xset q', shell=True, stdout=subprocess.PIPE)
            except subprocess.CalledProcessError as e:
                logger.error('Command failed: %s' % repr(e.cmd))
                raise Exception('Unable to run command')
            else:
                keys = ['Caps', 'Num', 'Scroll']
                locked = None
                for line in cmd.stdout:
                    for key in keys:
                        if key in line:
                            value = ' '.join(line.split())
                            if key in value[0:len(value) / 3]:
                                button = value[0:len(value) / 3]
                                if "off" in button:
                                    is_lock_on = False
                                else:
                                    is_lock_on = True
                                    locked = key
                                    break
                            elif key in value[len(value) / 3:len(value) / 3 + len(value) / 3]:
                                button = value[len(value) / 3:len(value) / 3 + len(value) / 3]
                                if "off" in button:
                                    is_lock_on = False
                                else:
                                    is_lock_on = True
                                    locked = key
                                    break
                            else:
                                button = value[len(value) / 3 * 2:len(value)]
                                if "off" in button:
                                    is_lock_on = False
                                else:
                                    is_lock_on = True
                                    locked = key
                                    break
                    if is_lock_on:
                        logger.error('Cannot run Iris because Key.%s_LOCK is toggled.' % locked.upper())
                        logger.error('Please turn it off to continue.')
                        break
                shutdown_process('Xquartz')
        if is_lock_on:
            self.finish(code=1)

    @staticmethod
    def __create_tempdir():
        """Helper function for creating the temporary directory.

        Writes to the global variable tmp_dir
        :return:
             Path of temporary directory.
        """
        temp_dir = tempfile.mkdtemp(prefix='iris_')
        logger.debug('Created temp dir "%s"' % temp_dir)
        return temp_dir

    @staticmethod
    def get_terminal_encoding():
        """Helper function to get current terminal encoding."""
        if sys.platform.startswith(Platform.WINDOWS):
            logger.debug('Running "chcp" shell command')
            chcp_output = os.popen('chcp').read().strip()
            logger.debug('chcp output: "%s"' % chcp_output)
            if chcp_output.startswith('Active code page:'):
                codepage = chcp_output.split(': ')[1]
                logger.debug('Active codepage is "%s"' % codepage)
                return codepage
            else:
                logger.warning('There was an error detecting the active codepage')
                return None
        else:
            logger.debug('Platform does not require switching terminal encoding')
            return None

    @staticmethod
    def set_terminal_encoding(encoding):
        """Helper function to set terminal encoding."""
        if os.path.exists('C:\\'):
            logger.debug('Running "chcp" shell command, setting codepage to "%s"', encoding)
            chcp_output = os.popen('chcp %s' % encoding).read().strip()
            logger.debug('chcp output: "%s"' % chcp_output)
            if chcp_output == 'Active code page: %s' % encoding:
                logger.debug('Successfully set codepage to "%s"' % encoding)
            else:
                logger.warning('Can\'t set codepage for terminal')

    @staticmethod
    def fix_terminal_encoding():
        """Helper function to set terminal to platform-specific UTF encoding."""
        global restore_terminal_encoding
        restore_terminal_encoding = Iris.get_terminal_encoding()
        if restore_terminal_encoding is None:
            return
        if os.path.exists('C:\\'):
            platform_utf_encoding = '65001'
        else:
            platform_utf_encoding = None
        if restore_terminal_encoding != platform_utf_encoding:
            Iris.set_terminal_encoding(platform_utf_encoding)

    def get_test_candidate(self, build):
        """Download and extract a build candidate.

        Build may either refer to a Firefox release identifier, package, or build directory.
        :param:
            build: str with firefox build
        :return:
            FirefoxApp object for test candidate
        """
        if os.path.isdir(build):
            candidate_app = fa.FirefoxApp(build, Settings.get_os(), False)
            return candidate_app
        else:
            platform = fd.FirefoxDownloader.detect_platform()
            if platform is None:
                logger.error('Unsupported platform: "%s"' % sys.platform)
                sys.exit(5)

            # `build` may refer to a build reference as defined in FirefoxDownloader,
            # a local Firefox package as produced by `mach build`, or a local build tree.
            if build in fd.FirefoxDownloader.build_urls:
                # Download test candidate by Firefox release ID
                logger.info('Downloading Firefox "%s" build for platform "%s"' % (build, platform))
                fdl = fd.FirefoxDownloader(self.args.workdir, cache_timeout=1 * 60 * 60)
                build_archive_file = fdl.download(build, self.args.locale, platform)
                if build_archive_file is None:
                    self.finish(code=-1)
                # Extract candidate archive
                candidate_app = fe.extract(build_archive_file, Settings.get_os(), self.args.workdir,
                                           cache_timeout=1 * 60 * 60)
                candidate_app.package_origin = fdl.get_download_url(build, platform)
            elif os.path.isfile(build):
                # Extract firefox build from archive
                logger.info('Using file "%s" as Firefox package' % build)
                candidate_app = fe.extract(build, Settings.get_os(), self.args.workdir, cache_timeout=1 * 60 * 60)
                candidate_app.package_origin = build
                logger.debug('Build candidate executable is "%s"' % candidate_app.exe)
            elif os.path.isfile(os.path.join(build, 'mach')):
                logger.info('Using Firefox build tree at `%s`' % build)
                dist_globs = sorted(glob.glob(os.path.join(build, 'obj-*', 'dist')))
                if len(dist_globs) == 0:
                    logger.critical('"%s" looks like a Firefox build directory, but can\'t find a build in it' % build)
                    self.finish(code=5)
                logger.debug('Potential globs for dist directory: %s' % dist_globs)
                dist_dir = dist_globs[-1]
                logger.info('Using "%s" as build distribution directory' % dist_dir)
                if 'apple-darwin' in dist_dir.split('/')[-2]:
                    # There is a special case for OS X dist directories:
                    # FirefoxApp expects OS X .dmg packages to contain the .app folder inside
                    # another directory. However, that directory isn't there in build trees,
                    # thus we need to point to the parent for constructing the app.
                    logger.info('Looks like this is an OS X build tree')
                    candidate_app = fa.FirefoxApp(os.path.abspath(os.path.dirname(dist_dir)), Settings.get_os(), True)
                    candidate_app.package_origin = os.path.abspath(build)
                else:
                    candidate_app = fa.FirefoxApp(os.path.abspath(dist_dir), Settings.get_os(), True)
                    candidate_app.package_origin = os.path.abspath(build)
            else:
                logger.critical('"%s" specifies neither a Firefox release, package file, or build directory' % build)
                logger.critical('Valid Firefox release identifiers are: %s' % ', '.join(fd.FirefoxDownloader.list()[0]))
                self.finish(5)

            logger.debug('Build candidate executable is "%s"' % candidate_app.exe)
            if candidate_app.platform != platform:
                logger.warning('Platform mismatch detected')
                logger.critical('Running a Firefox binary for "%s" on a "%s" platform will probably fail' %
                                (candidate_app.platform, platform))
            return candidate_app

    @staticmethod
    def check_tesseract_path(dir_path):
        if not isinstance(dir_path, str):
            return False
        if not os.path.exists(dir_path):
            return False
        return True

    def init_tesseract_path(self):

        win_tesseract_path = 'C:\\Program Files (x86)\\Tesseract-OCR'
        osx_linux_tesseract_path_1 = '/usr/local/bin/tesseract'
        osx_linux_tesseract_path_2 = '/usr/bin/tesseract'

        path_not_found = False
        current_os = Settings.get_os()

        if current_os == Platform.WINDOWS:
            if self.check_tesseract_path(win_tesseract_path):
                pytesseract.pytesseract.tesseract_cmd = win_tesseract_path + '\\tesseract'
            else:
                path_not_found = True
        elif current_os == Platform.LINUX or current_os == Platform.MAC:
            if self.check_tesseract_path(osx_linux_tesseract_path_1):
                pytesseract.pytesseract.tesseract_cmd = osx_linux_tesseract_path_1
            elif self.check_tesseract_path(osx_linux_tesseract_path_2):
                pytesseract.pytesseract.tesseract_cmd = osx_linux_tesseract_path_2
            else:
                path_not_found = True
        else:
            path_not_found = True

        if path_not_found:
            logger.critical('Unable to find Tesseract.')
            logger.critical('Please consult wiki for complete setup instructions.')
            self.finish(1)

    def check_7zip(self):
        # Find 7zip binary
        sz_bin = find_executable('7z')
        if sz_bin is None:
            logger.critical('Cannot find required library 7zip, aborting Iris.')
            logger.critical('Please consult wiki for complete setup instructions.')
            self.finish(code=5)


class RemoveTempDir(cleanup.CleanUp):
    """Class definition for cleanup helper responsible for deleting the temporary directory prior to exit."""

    @staticmethod
    def at_exit():
        global tmp_dir
        if tmp_dir is not None:
            logger.debug('Removing temp dir "%s"' % tmp_dir)
            shutil.rmtree(tmp_dir, ignore_errors=True)


class ResetTerminalEncoding(cleanup.CleanUp):
    """Class for restoring original terminal encoding at exit."""

    @staticmethod
    def at_exit():
        global restore_terminal_encoding
        if restore_terminal_encoding is not None:
            Iris.set_terminal_encoding(restore_terminal_encoding)


def initialize_logger_level(level):
    if level == 10:
        coloredlogs.install(level='DEBUG')
    elif level == 20:
        coloredlogs.install(level='INFO')
    elif level == 30:
        coloredlogs.install(level='WARNING')
    elif level == 40:
        coloredlogs.install(level='ERROR')
    elif level == 50:
        coloredlogs.install(level='CRITICAL')


def initialize_logger(output, level):
    if output:
        logging.basicConfig(filename=os.path.join(get_current_run_dir(), LOG_FILENAME), format=LOG_FORMAT)
    initialize_logger_level(level)

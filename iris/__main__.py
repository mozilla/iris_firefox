# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import importlib
import json
import shutil
import sys
from distutils import dir_util
from distutils.spawn import find_executable
from multiprocessing import Process

import coloredlogs
import pytesseract
from mozdownload import FactoryScraper
from mozinstall import install, get_binary
from mozversion import get_version

import firefox.app as fa
from api.core.key import Key
from api.core.profile import Profile
from api.core.settings import Settings
from api.core.util.core_helper import *
from api.core.util.parse_args import parse_args
from api.core.util.test_loader import load_tests, scan_all_tests
from api.core.util.version_parser import get_channel_from_version
from api.helpers.general import launch_firefox, quit_firefox
from firefox import cleanup
from local_web_server import LocalWebServer
from test_runner import run

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
    process_list = None

    def __init__(self):
        cleanup.init()
        Iris.fix_terminal_encoding()
        self.initialize_platform()
        self.verify_config()
        if self.control_center():
            self.initialize_run()
            run(self)
        else:
            self.finish(0)

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
        create_profile_cache()
        Iris.process_list = []
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
            if os.path.exists(profile_path):
                shutil.rmtree(profile_path)
            Profile.get_staged_profile(Profile.LIKE_NEW, profile_path)

            # Open local installation of Firefox.
            if Settings.get_os() == Platform.MAC:
                fx_path = '/Applications/Firefox.app/Contents/MacOS/firefox'
            elif Settings.get_os() == Platform.WINDOWS:
                if os.path.exists('C:\\Program Files (x86)\\Mozilla Firefox\\firefox'):
                    fx_path = 'C:\\Program Files (x86)\\Mozilla Firefox\\firefox'
                else:
                    fx_path = 'C:\\Program Files\\Mozilla Firefox\\firefox'
            else:
                fx_path = '/usr/lib/firefox/firefox'

            launch_firefox(fx_path, profile=profile_path, url=self.base_local_web_url)
            server = LocalWebServer(self.args.workdir, self.args.port)

            # Iris waits for the user to make a choice in the control center. Once they
            # make a decision, Firefox will quit.
            quit_firefox()

            # Check the result of the user's decision. If they have chosen to run tests,
            # we will continue. Otherwise, abort the current run.
            if server.result == 'cancel':
                # Temporary - we will quit Iris gracefully and clean up.
                logger.info('Canceling Iris run.')
                return False
            else:
                # Temporary - we will parse this returned value and turn it into runtime data.
                logger.info('Received data from control center: %s' % server.result)
                return True
        else:
            return True

    def initialize_run(self):
        self.start_local_web_server(self.local_web_root, self.args.port)
        self.get_firefox()
        self.update_run_index()
        self.update_run_log()
        load_tests(self)
        self.current_test = 0
        self.total_tests = len(self.test_list)

    def create_working_directory(self):
        # Create workdir (usually ~/.iris, used for caching etc.)
        # Assumes that no previous code will write to it.
        if not os.path.exists(self.args.workdir):
            logger.debug('Creating working directory %s' % self.args.workdir)
            os.makedirs(self.args.workdir)
        if not os.path.exists(os.path.join(self.args.workdir, 'data')):
            os.makedirs(os.path.join(self.args.workdir, 'data'))

    def create_run_directory(self):
        master_run_directory = os.path.join(self.args.workdir, 'runs')
        if self.args.clear:
            if os.path.exists(master_run_directory):
                shutil.rmtree(master_run_directory, ignore_errors=True)
        if not os.path.exists(master_run_directory):
            os.mkdir(master_run_directory)
        run_directory = os.path.join(master_run_directory, get_run_id())
        os.mkdir(run_directory)

    def update_run_index(self, new_data=None):
        # Prepare the current entry.
        current_run = {'id': get_run_id(), 'version': self.version, 'build': self.build_id, 'channel': self.fx_channel,
                       'locale': self.fx_locale}

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
        old_js_folder = os.path.join(parse_args().workdir, 'js')
        if os.path.exists(old_js_folder):
            shutil.rmtree(old_js_folder, ignore_errors=True)

        run_file = os.path.join(parse_args().workdir, 'data', 'all_runs.json')

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
        meta['config'] = '%s, %s-bit, %s' % (Platform.OS_VERSION, Platform.OS_BITS, Platform.PROCESSOR)
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

        test_log_file = os.path.join(self.args.workdir, 'data', 'all_tests.json')
        with open(test_log_file, 'w') as f:
            json.dump(self.master_test_list, f, sort_keys=True, indent=True)

    def create_arg_json(self):
        arg_data = {'email': {'type': 'bool', 'value': ['true', 'false'], 'default': 'false', 'label': 'Email results'},
                    'firefox': {'type': 'str', 'value': ['local', 'release', 'esr', 'beta', 'nightly'],
                                'default': 'beta', 'label': 'Firefox'},
                    'highlight': {'type': 'bool', 'value': ['true', 'false'], 'default': 'false',
                                  'label': 'Debug using highlighting'},
                    'level': {'type': 'str', 'value': ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG'],
                              'default': 'INFO', 'label': 'Debug level'},
                    'locale': {'type': 'str', 'value': fa.FirefoxApp.LOCALES, 'default': 'en-us', 'label': 'Locale'},
                    'mouse': {'type': 'float', 'value': ['0.0', '0.5', '1.0', '2.0'], 'default': '0.5',
                              'label': 'Mouse speed'},
                    'override': {'type': 'bool', 'value': ['true', 'false'], 'default': 'false',
                                 'label': 'Run disabled tests'},
                    'port': {'type': 'int', 'value': ['2000'], 'default': '2000', 'label': 'Local web server port'},
                    'report': {'type': 'bool', 'value': ['true', 'false'], 'default': 'false',
                               'label': 'Create TestRail report'},
                    'save': {'type': 'bool', 'value': ['true', 'false'], 'default': 'false',
                             'label': 'Save profiles to disk'}}

        arg_log_file = os.path.join(self.args.workdir, 'data', 'all_args.json')
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
            Iris.process_list.append(web_server_process)
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

    def get_firefox(self):
        self.fx_path = self.get_test_candidate()
        build_info = get_version(binary=self.fx_path)
        self.fx_channel = get_channel_from_version(self.args.firefox)
        self.version = build_info['application_version']
        self.build_id = build_info['platform_buildid']
        self.fx_locale = self.args.locale

    def get_test_candidate(self):
        """Download and extract a build candidate.
        Build may either refer to a Firefox release identifier, package, or build directory.
        :param:
            build: str with firefox build
        :return:
            FirefoxApp object for test candidate
        """

        location = ''
        candidate_app = ''

        if self.args.firefox == 'local':
            if Settings.is_mac():
                location = '/Applications/Firefox.app/Contents/'
                candidate_app = os.path.join(location, 'MacOS', 'firefox')
            elif Settings.is_windows():
                location = 'C:\\Program Files (x86)\\Mozilla Firefox'
                if not os.path.exists(location):
                    location = 'C:\\Program Files\\Mozilla Firefox'
                    candidate_app = os.path.join(location, 'firefox.exe')
            elif Settings.is_linux():
                location = '/usr/lib/firefox'
                candidate_app = os.path.join(location, 'firefox')
            else:
                logger.critical('Platform not supported')
                self.finish(code=5)

            if not os.path.isdir(location):
                logger.critical('Firefox not found. Please download if from https://www.mozilla.org/en-US/firefox/new/')
                self.finish(code=5)

            return candidate_app

        else:
            cache_dir = os.path.join(get_working_dir(), 'cache')
            scraper = FactoryScraper('candidate',
                                     version=self.args.firefox,
                                     destination=cache_dir,
                                     locale=self.args.locale)
            print(scraper.base_url)
            firefox_dmg = scraper.download()
            install_folder = install(src=firefox_dmg,
                                     dest=get_current_run_dir())

            return get_binary(install_folder, 'Firefox')

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
        tmp_dir = get_tempdir()
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


class TerminateSubprocesses(cleanup.CleanUp):
    """Class for terminiting subprocesses, such as local web server instances."""

    @staticmethod
    def at_exit():
        if hasattr(Iris, 'process_list'):
            logger.debug('There are %s queued process(es) to terminate.' % len(Iris.process_list))
            for process in Iris.process_list:
                logger.debug('Terminating process.')
                process.terminate()
                process.join()
        if Settings.is_mac():
            # Extra call to shutdown the program we use to check keyboard lock,
            # in case Iris was terminated abruptly.
            shutdown_process('Xquartz')


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

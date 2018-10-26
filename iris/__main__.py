# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import importlib
import json
import shutil
import sys
from distutils.spawn import find_executable
from multiprocessing import Process

import coloredlogs
import pytesseract
from distutils import dir_util
from mozdownload import FactoryScraper, errors
from mozinstall import install, get_binary

from api.core.key import Key
from api.core.profile import Profile
from api.core.settings import Settings
from api.core.util.core_helper import *
from api.core.util.parse_args import get_global_args, parse_args
from api.core.util.test_loader import load_tests, scan_all_tests
from api.core.util.version_parser import get_latest_scraper_details, get_version_from_path, get_scraper_details
from api.helpers.general import launch_firefox, quit_firefox, get_firefox_channel, get_firefox_version, \
    get_firefox_build_id
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
            self.delete_run_directory()
            self.finish(0)

    def verify_config(self):
        if not self.args.no_check:
            self.check_keyboard_state()
        self.init_tesseract_path()
        self.check_7zip()

    def initialize_platform(self):
        self.args = parse_args()
        self.module_dir = IrisCore.get_module_dir()
        self.platform = get_platform()
        self.os = Settings.get_os()
        self.create_working_directory()
        self.create_run_directory()
        initialize_logger(LOG_FILENAME, self.args.level)
        IrisCore.create_profile_cache()
        Iris.process_list = []
        self.local_web_root = os.path.join(self.module_dir, 'iris', 'local_web')
        self.base_local_web_url = 'http://127.0.0.1:%s' % self.args.port
        self.create_test_json()
        self.create_arg_json()
        self.test_list = []
        self.test_packages = []

    def control_center(self):
        # If user provides custom command-line arguments, we will skip the control center.
        if len(sys.argv) > 1 and not self.args.control:
            return True
        else:
            # Copy web assets to working directory.
            dir_util.copy_tree(os.path.join(self.module_dir, 'iris', 'cc_files'), self.args.workdir)
            # Copy profile for Firefox.
            profile_path = os.path.join(self.args.workdir, 'cc_profile')
            if os.path.exists(profile_path):
                shutil.rmtree(profile_path)
            Profile._get_staged_profile(Profile.LIKE_NEW, profile_path)

            # Open local installation of Firefox.
            paths = []
            is_installed = False
            fx_path = ''
            if Settings.get_os() == Platform.MAC:
                paths.append('/Applications/Firefox.app/Contents/MacOS/firefox')
                paths.append('/Applications/Firefox Developer Edition.app/Contents/MacOS/firefox')
                paths.append('/Applications/Firefox Nightly.app/Contents/MacOS/firefox')
            elif Settings.get_os() == Platform.WINDOWS:
                paths.append('C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe')
                paths.append('C:\\Program Files (x86)\\Firefox Developer Edition\\firefox.exe')
                paths.append('C:\\Program Files (x86)\\Nightly\\firefox.exe')
                paths.append('C:\\Program Files\\Mozilla Firefox\\firefox.exe')
                paths.append('C:\\Program Files\\Firefox Developer Edition\\firefox.exe')
                paths.append('C:\\Program Files\\Nightly\\firefox.exe')
            else:
                paths.append('/usr/bin/firefox')
                paths.append('/usr/lib/firefox/firefox')

            for path in paths:
                if os.path.exists(path):
                    fx_path = path
                    is_installed = True
                    break
            if not is_installed:
                logger.error('Can\'t find local Firefox installation, aborting Iris run.')
                self.finish(1)

            fx_runner = launch_firefox(fx_path, profile=profile_path, url=self.base_local_web_url)
            fx_runner.start()
            server = LocalWebServer(self.args.workdir, self.args.port)

            # Iris waits for the user to make a choice in the control center. Once they
            # make a decision, Firefox will quit.
            quit_firefox()
            status = fx_runner.process_handler.wait(Settings.FIREFOX_TIMEOUT)
            if status is None:
                logger.debug('Firefox did not quit. Executing force quit.')
                fx_runner.stop()
                fx_runner = None

            # Check the result of the user's decision. If they have chosen to run tests,
            # we will continue. Otherwise, abort the current run.
            if server.result == 'cancel':
                # We will quit Iris gracefully and clean up.
                logger.info('Canceling Iris run.')
                return False
            else:
                # We will parse this returned value and turn it into runtime data.
                logger.debug('Received data from control center: %s' % server.result)

                # Update app args with new values
                self.args.locale = server.result['locale']
                self.args.firefox = server.result['firefox']
                self.args.override = server.result['override']
                self.args.port = int(server.result['port'])
                self.args.email = server.result['email']
                self.args.highlight = server.result['highlight']
                self.args.mouse = float(server.result['mouse'])
                self.args.report = server.result['report']
                self.args.save = server.result['save']

                # For other parts of Iris that get their arguments from parse_args,
                # we have to update the values there as well.
                get_global_args().locale = self.args.locale
                get_global_args().firefox = self.args.firefox
                get_global_args().override = self.args.override
                get_global_args().port = self.args.port
                get_global_args().email = self.args.email
                get_global_args().highlight = server.result['highlight']
                get_global_args().mouse = self.args.mouse
                get_global_args().report = self.args.report
                get_global_args().save = self.args.save

                # Update this URL, used by test cases.
                self.base_local_web_url = 'http://127.0.0.1:%s' % self.args.port

                # Parse tests.
                tests = sorted(server.result['tests'])
                if len(tests):
                    for package in tests:
                        self.test_packages.append(package)
                        for test in server.result['tests'][package]:
                            self.test_list.append(test['name'])
                else:
                    logger.info('No tests selected, canceling Iris run.')
                    return False
                return True

    def initialize_run(self):
        self.start_local_web_server(self.local_web_root, self.args.port)
        self.get_firefox()
        self.update_run_index()
        self.update_run_log()
        # If tests exist already, they came from the control center.
        # Otherwise, use the command-line args.
        if len(self.test_list) == 0:
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

        # Remove all previous runs and downloaded builds.
        if self.args.clear:
            master_run_directory = os.path.join(self.args.workdir, 'runs')
            if os.path.exists(master_run_directory):
                shutil.rmtree(master_run_directory, ignore_errors=True)
            run_file = os.path.join(self.args.workdir, 'data', 'all_runs.json')
            if os.path.exists(run_file):
                os.remove(run_file)
            cache_builds_directory = os.path.join(self.args.workdir, 'cache')
            if os.path.exists(cache_builds_directory):
                shutil.rmtree(cache_builds_directory, ignore_errors=True)

    def create_run_directory(self):
        master_run_directory = os.path.join(self.args.workdir, 'runs')
        if not os.path.exists(master_run_directory):
            os.mkdir(master_run_directory)
        run_directory = os.path.join(master_run_directory, IrisCore.get_run_id())
        os.mkdir(run_directory)

    def delete_run_directory(self):
        master_run_directory = os.path.join(self.args.workdir, 'runs')
        run_directory = os.path.join(master_run_directory, IrisCore.get_run_id())
        if os.path.exists(run_directory):
            shutil.rmtree(run_directory, ignore_errors=True)

    def update_run_index(self, new_data=None):
        # Prepare the current entry.
        current_run = {'id': IrisCore.get_run_id(), 'version': self.version, 'build': self.build_id,
                       'channel': self.fx_channel,
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
                if run['id'] == IrisCore.get_run_id():
                    run_file_data['runs'].remove(run)
            run_file_data['runs'].append(current_run)
        else:
            logger.debug('Creating run file: %s' % run_file)
            run_file_data = {'runs': []}
            run_file_data['runs'].append(current_run)

        with open(run_file, 'w') as f:
            json.dump(run_file_data, f, sort_keys=True, indent=True)

    def update_run_log(self, new_data=None):
        meta = {'run_id': IrisCore.get_run_id(), 'fx_version': self.version, 'fx_build_id': self.build_id,
                'platform': self.os,
                'config': '%s, %s-bit, %s' % (Platform.OS_VERSION, Platform.OS_BITS, Platform.PROCESSOR),
                'channel': self.fx_channel, 'locale': self.fx_locale, 'args': ' '.join(sys.argv),
                'params': vars(self.args), 'log': os.path.join(IrisCore.get_current_run_dir(), 'iris_log.log')}

        repo = git.Repo(self.module_dir)
        meta['iris_version'] = 1.0
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

        run_file = os.path.join(IrisCore.get_current_run_dir(), 'run.json')
        run_file_data = {'meta': meta, 'tests': tests}
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

                test_object = {'name': module, 'module': current_module.__file__, 'meta': current_test.meta,
                               'package': current_package}

                if current_test.fx_version is '':
                    test_object['fx_version'] = 'all'
                else:
                    test_object['fx_version'] = current_test.fx_version

                test_object['platform'] = filter_list(current_test.platform, current_test.exclude)
                test_object['channel'] = filter_list(current_test.channel, current_test.exclude)
                test_object['locale'] = filter_list(current_test.locale, current_test.exclude)
                test_object['enabled'] = self.os in filter_list(current_test.platform, current_test.exclude)
                test_object['tags'] = current_test.tags
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
                    'firefox': {'type': 'str', 'value': ['local', 'latest', 'latest-esr', 'latest-beta', 'nightly'],
                                'default': 'latest-beta', 'label': 'Firefox'},
                    'highlight': {'type': 'bool', 'value': ['true', 'false'], 'default': 'false',
                                  'label': 'Debug using highlighting'},
                    'locale': {'type': 'str', 'value': Settings.LOCALES, 'default': 'en-US', 'label': 'Locale'},
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
            if os.path.exists(path):
                os.remove(path)
            last_fail = open(path, 'w')
            for item in failures:
                for package in self.master_test_list:
                    for test in self.master_test_list[package]:
                        if test["name"] == item:
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
        keyboard_keys = [Key.CAPS_LOCK, Key.NUM_LOCK, Key.SCROLL_LOCK]
        for key in keyboard_keys:
            if Key.is_lock_on(key):
                logger.error('Cannot run Iris because %s is on. Please turn it off to continue.' % key)
                is_lock_on = True

        if is_lock_on:
            logger.error('Please turn it off to continue.')
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
        self.fx_channel = get_firefox_channel(self.fx_path)
        self.version = get_firefox_version(self.fx_path)
        self.build_id = get_firefox_build_id(self.fx_path)
        self.fx_locale = self.args.locale

    def get_test_candidate(self):
        """Download and extract a build candidate.

        Build may either refer to a Firefox release identifier, package, or build directory.
        :param:
            build: str with firefox build
        :return:
            Installation path for the Firefox App
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
            try:
                locale = 'ja-JP-mac' if self.args.locale == 'ja' and Settings.is_mac() else self.args.locale
                type, scraper_details = get_scraper_details(self.args.firefox,
                                                            Settings.CHANNELS,
                                                            os.path.join(IrisCore.get_working_dir(), 'cache'),
                                                            locale)
                scraper = FactoryScraper(type, **scraper_details)

                firefox_dmg = scraper.download()
                install_folder = install(src=firefox_dmg,
                                         dest=IrisCore.get_current_run_dir())

                binary = get_binary(install_folder, 'Firefox')

                channel = get_firefox_channel(binary)
                latest_type, latest_scraper_details = get_latest_scraper_details(channel)
                latest_path = FactoryScraper(latest_type, **latest_scraper_details).filename

                self.latest_version = get_version_from_path(latest_path)
                logger.info('Latest available version for %s channel is: %s' % (channel, self.latest_version))

                return binary
            except errors.NotFoundError:
                logger.critical('Specified build (%s) has not been found. Closing Iris ...' % self.args.firefox)
                self.finish(5)

    @staticmethod
    def check_tesseract_path(dir_path):
        if not isinstance(dir_path, str):
            return False
        if not os.path.exists(dir_path):
            return False
        return True

    def init_tesseract_path(self):

        which_tesseract = \
            subprocess.Popen('which tesseract', stdout=subprocess.PIPE, shell=True).communicate()[0].rstrip()

        path_not_found = False
        current_os = Settings.get_os()

        if current_os == Platform.WINDOWS:
            win_default_tesseract_path = 'C:\\Program Files (x86)\\Tesseract-OCR'

            if '/c/' in str(which_tesseract):
                win_which_tesseract_path = which_tesseract.replace('/c/', 'C:\\').replace('/', '\\') + '.exe'
            else:
                win_which_tesseract_path = which_tesseract.replace('\\', '\\\\')

            if self.check_tesseract_path(win_default_tesseract_path):
                pytesseract.pytesseract.tesseract_cmd = win_default_tesseract_path + '\\tesseract'
            elif self.check_tesseract_path(win_which_tesseract_path):
                pytesseract.pytesseract.tesseract_cmd = win_which_tesseract_path
            else:
                path_not_found = True

        elif current_os == Platform.LINUX or current_os == Platform.MAC:
            if self.check_tesseract_path(which_tesseract):
                pytesseract.pytesseract.tesseract_cmd = which_tesseract
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
        tmp_dir = IrisCore.get_tempdir()
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
            IrisCore.shutdown_process('Xquartz')


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
        logging.basicConfig(filename=os.path.join(IrisCore.get_current_run_dir(), LOG_FILENAME), format=LOG_FORMAT)
    initialize_logger_level(level)

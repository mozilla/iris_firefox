# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import datetime
import os

import git
import inspect
import logging
import mss
import multiprocessing
import numpy
import pyautogui
import pytesseract
import shutil
import subprocess
import tempfile
from PIL import Image
from distutils.spawn import find_executable

from iris.api.core.errors import APIHelperError, ScreenshotError
from iris.api.core.platform import Platform
from parse_args import parse_args
from version_parser import check_version

SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()
SCREENSHOT_SIZE = Platform.SCREENSHOT_SIZE
SCREENSHOT_WIDTH, SCREENSHOT_HEIGHT = SCREENSHOT_SIZE

_run_id = datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')
_current_module = os.path.join(os.path.expanduser('~'), 'temp', 'test')

logger = logging.getLogger(__name__)

INVALID_GENERIC_INPUT = 'Invalid input'
INVALID_NUMERIC_INPUT = 'Expected numeric value'

MIN_CPU_FOR_MULTIPROCESSING = 4


def get_os():
    """Get the type of the operating system your script is running on."""
    current_system = Platform.OS_NAME
    if current_system == 'win':
        current_os = 'win'
    elif current_system == 'linux':
        current_os = 'linux'
    elif current_system == 'mac':
        current_os = 'osx'
    else:
        raise APIHelperError('Iris does not yet support your current environment: ' + current_system)
    return current_os


def get_os_version():
    """Get the version string of the operating system your script is running on."""
    os_version = Platform.OS_VERSION
    if Platform.OS_NAME == 'win' and os_version == '6.1':
        current_os_version = 'win7'
    elif Platform.OS_NAME == 'mac':
        current_os_version = 'osx_%s' % IrisCore.get_osx_screen_type()
    else:
        current_os_version = get_os()
    return current_os_version


def get_platform():
    """Get the version string of the operating system your script is running on."""
    return Platform.PROCESSOR


def is_multiprocessing_enabled():
    return multiprocessing.cpu_count() >= MIN_CPU_FOR_MULTIPROCESSING and get_os() != 'win'


class IrisCore(object):
    tmp_dir = None
    _mss = mss.mss()

    @staticmethod
    def get_current_module():
        """Returns the name of the active test module."""
        return _current_module

    @staticmethod
    def parse_module_path():
        """Returns the parent directory and module name of the calling file."""
        if '\\' in IrisCore.get_current_module():
            delimiter = '\\'
        else:
            delimiter = '/'
        temp = IrisCore.get_current_module().split(delimiter)
        parent = temp[len(temp) - 2]
        test = temp[len(temp) - 1].split('.py')[0]
        return parent, test

    @staticmethod
    def set_current_module(module):
        """Sets the active module name."""
        global _current_module
        _current_module = module

    @staticmethod
    def get_module_dir():
        """Returns the path to the root of the local Iris repo."""
        return os.path.realpath(os.path.split(__file__)[0] + '/../../../..')

    @staticmethod
    def get_working_dir():
        """Returns the path to the root of the directory where local data is stored."""
        IrisCore.create_working_directory()
        return parse_args().workdir

    @staticmethod
    def get_downloads_dir():
        """Returns the path to the downloads directory."""
        IrisCore.create_downloads_directory()
        return os.path.join(IrisCore.get_test_output_directory(), 'downloads')

    @staticmethod
    def get_tests_dir():
        """Returns the directory where tests are located."""
        return os.path.join(IrisCore.get_module_dir(), 'iris', 'tests')

    @staticmethod
    def get_current_run_dir():
        """Returns the directory inside the working directory of the active run."""
        IrisCore.create_run_directory()
        return os.path.join(parse_args().workdir, 'runs', IrisCore.get_run_id())

    @staticmethod
    def get_log_file_path():
        """Returns the path to the log file."""
        path = IrisCore.get_current_run_dir()
        if not os.path.exists(path):
            os.mkdir(path)
        return os.path.join(path, 'iris_log.log')

    @staticmethod
    def make_test_output_dir():
        """Creates directories inside the current run directory for test output."""
        parent, test = IrisCore.parse_module_path()
        parent_directory = os.path.join(IrisCore.get_current_run_dir(), parent)
        if not os.path.exists(parent_directory):
            os.makedirs(parent_directory)
        test_directory = os.path.join(parent_directory, test)
        if not os.path.exists(test_directory):
            os.mkdir(test_directory)
        return test_directory

    @staticmethod
    def get_test_output_directory():
        """Returns the path to the test output directory."""
        return IrisCore.make_test_output_dir()

    @staticmethod
    def get_image_debug_path():
        """Returns the root directory where a test's debug images are located."""
        parent, test = IrisCore.parse_module_path()
        path = os.path.join(parse_args().workdir, 'runs', IrisCore.get_run_id(), parent, test, 'debug_images')
        return path

    @staticmethod
    def __create_tempdir():
        """Creates the temporary directory.
        Writes to the global variable tmp_dir
        :return:
             Path of temporary directory.
        """
        global tmp_dir
        tmp_dir = tempfile.mkdtemp(prefix='iris_')
        logger.debug('Created temp dir "%s"' % tmp_dir)
        return tmp_dir

    @staticmethod
    def create_profile_cache():
        """Creates a temporary directory to hold the run's profile cache."""
        global tmp_dir
        tmp_dir = IrisCore.__create_tempdir()

    @staticmethod
    def get_tempdir():
        global tmp_dir
        return tmp_dir

    @staticmethod
    def get_run_id():
        global _run_id
        return _run_id

    @staticmethod
    def get_images_path():
        return os.path.join('images', get_os())

    @staticmethod
    def get_uhd_details():
        uhd_factor = SCREENSHOT_WIDTH / SCREEN_WIDTH
        is_uhd = True if uhd_factor > 1 else False
        return is_uhd, uhd_factor

    @staticmethod
    def is_ocr_text(input_text):
        is_ocr_string = True
        pattern_extensions = ('.png', '.jpg')
        if input_text.endswith(pattern_extensions):
            is_ocr_string = False
        return is_ocr_string

    @staticmethod
    def get_region(region=None, for_ocr=False):
        """Grabs image from region or full screen.

        :param Region || None region: Region param
        :param for_ocr: boolean param for ocr processing
        :return: Image
        """
        is_uhd, uhd_factor = IrisCore.get_uhd_details()

        if region is not None:
            grabbed_area = IrisCore.get_screenshot(region)

            if is_uhd and not for_ocr:
                grabbed_area = grabbed_area.resize([region.width, region.height])

            return grabbed_area
        else:
            grabbed_area = IrisCore.get_screenshot()

        if is_uhd and not for_ocr:
            return grabbed_area.resize([SCREEN_WIDTH, SCREEN_HEIGHT])
        else:
            return grabbed_area

    @staticmethod
    def get_test_name():
        white_list = ['general.py']
        all_stack = inspect.stack()
        for stack in all_stack:
            filename = os.path.basename(stack[1])
            method_name = stack[3]
            if filename is not '' and 'tests' in os.path.dirname(stack[1]):
                return filename
            elif filename in white_list:
                return method_name
        return

    @staticmethod
    def verify_test_compat(test, browser):
        if browser.channel is None or browser.version is None:
            return False

        not_excluded = True
        exclude = [test.exclude] if isinstance(test.exclude, str) else [i for i in test.exclude]
        for item in exclude:
            if item in browser.channel or item in get_os() or item in browser.locale:
                not_excluded = False
        correct_version = True if test.fx_version == '' else check_version(browser.version, test.fx_version)
        correct_channel = browser.channel in test.channel
        correct_locale = parse_args().locale in test.locale
        correct_platform = get_os() in test.platform
        blocked_by = IrisCore.test_is_blocked(test)
        result = True == correct_platform == correct_version == correct_channel == correct_locale == not_excluded \
                 != blocked_by
        return result

    @staticmethod
    def test_is_blocked(test):
        if test.blocked_by:
            blocked_dict = test.blocked_by
            if all(k in blocked_dict for k in ('id', 'platform')):
                platform = blocked_dict['platform']
                if get_os() in platform:
                    return True
            else:
                return False
        return False

    @staticmethod
    def get_git_details():
        repo_details = {}
        repo = git.Repo()
        repo_details['iris_version'] = 0.1
        repo_details['iris_repo'] = repo.working_tree_dir
        repo_details['iris_branch'] = repo.active_branch.name
        repo_details['iris_branch_head'] = repo.head.object.hexsha
        return repo_details

    @staticmethod
    def shutdown_process(process_name):
        if get_os() == Platform.WINDOWS:
            command_str = 'taskkill /IM ' + process_name + '.exe'
            try:
                subprocess.Popen(command_str, shell=True, stdout=subprocess.PIPE)
            except subprocess.CalledProcessError:
                logger.error('Command  failed: "%s"' % command_str)
                raise Exception('Unable to run Command.')
        elif get_os() == Platform.MAC or get_os() == Platform.LINUX:
            command_str = 'pkill ' + process_name
            try:
                subprocess.Popen(command_str, shell=True, stdout=subprocess.PIPE)
            except subprocess.CalledProcessError:
                logger.error('Command  failed: "%s"' % command_str)
                raise Exception('Unable to run Command.')

    @staticmethod
    def get_osx_screen_type():
        """
        Compare size of screenshot with the reported monitor size to determine if pixels match.
        :return: String
        """
        if Platform.HIGH_DEF:
            return 'retina'
        else:
            return 'non_retina'

    @staticmethod
    def get_screenshot(region=None):
        if Platform.OS_NAME != 'linux':
            grabbed_area = IrisCore._mss_screenshot(region=region)
        else:
            if region is not None:
                try:
                    grabbed_area = pyautogui.screenshot(region=(region.x, region.y, region.width, region.height))
                except (IOError, OSError):
                    logger.debug('Call to pyautogui.screnshot failed, using mss instead.')
                    grabbed_area = IrisCore._mss_screenshot(region=region)
            else:
                try:
                    grabbed_area = pyautogui.screenshot(region=(0, 0, SCREENSHOT_WIDTH, SCREENSHOT_HEIGHT))
                except (IOError, OSError):
                    logger.debug('Call to pyautogui.screnshot failed, using mss instead.')
                    grabbed_area = IrisCore._mss_screenshot(region=region)
        return grabbed_area

    @staticmethod
    def _mss_screenshot(region=None):
        if region is not None:
            screen_region = {'top': region.y, 'left': region.x, 'width': region.width, 'height': region.height}
        else:
            screen_region = {'top': 0, 'left': 0, 'width': SCREEN_WIDTH, 'height': SCREEN_HEIGHT}
        try:
            image = numpy.array(IrisCore._mss.grab(screen_region))
        except Exception:
            raise ScreenshotError('Unable to take screenshot.')
        return Image.fromarray(image, mode='RGBA')

    @staticmethod
    def get_base_local_web_url():
        return 'http://127.0.0.1:%s' % parse_args().port

    @staticmethod
    def get_local_web_root():
        return os.path.join(IrisCore.get_module_dir(), 'iris', 'local_web')

    @staticmethod
    def check_7zip():
        """Checks if 7zip is installed."""
        sz_bin = find_executable('7z')
        if sz_bin is None:
            logger.critical('Cannot find required library 7zip, aborting Iris.')
            logger.critical('Please consult wiki for complete setup instructions.')
            return False
        return True

    @staticmethod
    def init_tesseract_path():
        """Initialize Tesseract path."""
        which_tesseract = subprocess.Popen('which tesseract', stdout=subprocess.PIPE, shell=True).communicate()[
            0].rstrip()
        path_not_found = False

        if get_os() == 'win':
            win_default_tesseract_path = 'C:\\Program Files (x86)\\Tesseract-OCR'

            if '/c/' in str(which_tesseract):
                win_which_tesseract_path = which_tesseract.replace('/c/', 'C:\\').replace('/', '\\') + '.exe'
            else:
                win_which_tesseract_path = which_tesseract.replace('\\', '\\\\')

            if _check_path(win_default_tesseract_path):
                pytesseract.pytesseract.tesseract_cmd = win_default_tesseract_path + '\\tesseract'
            elif _check_path(win_which_tesseract_path):
                pytesseract.pytesseract.tesseract_cmd = win_which_tesseract_path
            else:
                path_not_found = True

        elif get_os() == 'linux' or get_os() == 'osx':
            if _check_path(which_tesseract):
                pytesseract.pytesseract.tesseract_cmd = which_tesseract
            else:
                path_not_found = True
        else:
            path_not_found = True

        if path_not_found:
            logger.critical('Unable to find Tesseract.')
            logger.critical('Please consult wiki for complete setup instructions.')
            return False
        return True

    @staticmethod
    def delete_run_directory():
        master_run_directory = os.path.join(parse_args().workdir, 'runs')
        run_directory = os.path.join(master_run_directory, IrisCore.get_run_id())
        if os.path.exists(run_directory):
            shutil.rmtree(run_directory, ignore_errors=True)

    @staticmethod
    def create_run_directory():
        IrisCore.create_working_directory()
        master_run_directory = os.path.join(parse_args().workdir, 'runs')
        if not os.path.exists(master_run_directory):
            os.mkdir(master_run_directory)
        run_directory = os.path.join(master_run_directory, IrisCore.get_run_id())
        if not os.path.exists(run_directory):
            os.mkdir(run_directory)

    @staticmethod
    def create_downloads_directory():
        IrisCore.create_run_directory()
        downloads_directory = os.path.join(IrisCore.get_test_output_directory(), 'downloads')
        if not os.path.exists(downloads_directory):
            os.mkdir(downloads_directory)

    @staticmethod
    def create_working_directory():
        if not os.path.exists(parse_args().workdir):
            logger.debug('Creating working directory %s' % parse_args().workdir)
            os.makedirs(parse_args().workdir)
        if not os.path.exists(os.path.join(parse_args().workdir, 'data')):
            os.makedirs(os.path.join(parse_args().workdir, 'data'))

        if parse_args().clear:
            master_run_directory = os.path.join(parse_args().workdir, 'runs')
            if os.path.exists(master_run_directory):
                shutil.rmtree(master_run_directory, ignore_errors=True)
            run_file = os.path.join(parse_args().workdir, 'data', 'all_runs.json')
            if os.path.exists(run_file):
                os.remove(run_file)
            cache_builds_directory = os.path.join(parse_args().workdir, 'cache')
            if os.path.exists(cache_builds_directory):
                shutil.rmtree(cache_builds_directory, ignore_errors=True)


def _check_path(dir_path):
    """Check if a path exists."""
    if not isinstance(dir_path, str):
        return False
    if not os.path.exists(dir_path):
        return False
    return True

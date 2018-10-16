# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import datetime
import inspect
import logging
import multiprocessing
import os
import subprocess
import tempfile

import git
import mss
import numpy
import pyautogui
from PIL import Image

from iris.api.core.errors import APIHelperError
from iris.api.core.platform import Platform
from parse_args import parse_args
from version_parser import check_version

SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()
SCREENSHOT_SIZE = Platform.SCREENSHOT_SIZE
SCREENSHOT_WIDTH, SCREENSHOT_HEIGHT = SCREENSHOT_SIZE

SUCCESS_LEVEL_NUM = 35
logging.addLevelName(SUCCESS_LEVEL_NUM, 'SUCCESS')

_run_id = datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')
_current_module = os.path.join(os.path.expanduser('~'), 'temp', 'test')


def success(self, message, *args, **kws):
    """Log 'msg % args' with severity 'SUCCESS' (level = 35).
    To pass exception information, use the keyword argument exc_info with
    a true value, e.g.
    logger.success('Houston, we have a %s', 'thorny problem', exc_info=1)
    """
    if self.isEnabledFor(SUCCESS_LEVEL_NUM):
        self._log(SUCCESS_LEVEL_NUM, message, args, **kws)


logging.Logger.success = success
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


def scroll(clicks):
    """Performs a scroll of the mouse scroll wheel.

    :param clicks: The amount of scrolling to perform.
    :return: None.
    """
    pyautogui.scroll(clicks)


def filter_list(original_list, exclude_list):
    new_list = []
    for item in original_list:
        if item not in exclude_list:
            new_list.append(item)
    return new_list


class IrisCore(object):
    tmp_dir = None

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
        return parse_args().workdir

    @staticmethod
    def get_current_run_dir():
        """Returns the directory inside the working directory of the active run."""
        return os.path.join(parse_args().workdir, 'runs', IrisCore.get_run_id())

    @staticmethod
    def make_test_output_dir():
        """Creates directories inside the current run directory for test output."""
        parent, test = IrisCore.parse_module_path()
        parent_directory = os.path.join(IrisCore.get_current_run_dir(), parent)
        if not os.path.exists(parent_directory):
            os.makedirs(parent_directory)
        test_directory = os.path.join(parent_directory, test)
        os.mkdir(test_directory)
        return test_directory

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
            r_x = uhd_factor * region.x if is_uhd else region.x
            r_y = uhd_factor * region.y if is_uhd else region.y
            r_w = uhd_factor * region.width if is_uhd else region.width
            r_h = uhd_factor * region.height if is_uhd else region.height


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
    def verify_test_compat(test, app):
        not_excluded = True
        exclude = [test.exclude] if isinstance(test.exclude, str) else [i for i in test.exclude]
        for item in exclude:
            if item in app.fx_channel or item in app.os or item in app.args.locale:
                not_excluded = False
        correct_version = True if test.fx_version == '' else check_version(app.version, test.fx_version)
        correct_channel = app.fx_channel in test.channel
        correct_locale = app.args.locale in test.locale
        correct_platform = app.os in test.platform
        result = True == correct_platform == correct_version == correct_channel == correct_locale == not_excluded
        return result

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

        if region is not None:
            screen_region = {'top': region.y, 'left': region.x, 'width': region.width, 'height': region.height}
            image = numpy.array(mss.mss().grab(screen_region))
        else:
            screen_region = {'top': 0, 'left': 0, 'width': SCREEN_WIDTH, 'height': SCREEN_HEIGHT}
            image = numpy.array(mss.mss().grab(screen_region))
        grabbed_area = Image.fromarray(image, mode='RGBA')
        return grabbed_area

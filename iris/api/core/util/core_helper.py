# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import datetime
import inspect
import logging
import multiprocessing
import os
import subprocess

import git
import pyautogui

from iris.api.core.platform import Platform
from parse_args import parse_args
from version_parser import check_version

SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()
SCREENSHOT_WIDTH, SCREENSHOT_HEIGHT = pyautogui.screenshot().size

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
        logger.error('Iris does not yet support your current environment: ' + current_system)

    return current_os


def get_os_version():
    """Get the version string of the operating system your script is running on."""
    return Platform.OS_VERSION


def get_platform():
    """Get the version string of the operating system your script is running on."""
    return Platform.PROCESSOR


def get_current_module():
    return _current_module


def parse_module_path():
    if '\\' in get_current_module():
        delimiter = '\\'
    else:
        delimiter = '/'
    temp = get_current_module().split(delimiter)
    parent = temp[len(temp) - 2]
    test = temp[len(temp) - 1].split('.py')[0]
    return parent, test


def set_current_module(module):
    global _current_module
    _current_module = module


def get_module_dir():
    return os.path.realpath(os.path.split(__file__)[0] + '/../../../..')


def get_working_dir():
    return parse_args().workdir


def get_current_run_dir():
    return os.path.join(parse_args().workdir, 'runs', get_run_id())


def make_test_output_dir():
    parent, test = parse_module_path()
    parent_directory = os.path.join(get_current_run_dir(), parent)
    if not os.path.exists(parent_directory):
        os.makedirs(parent_directory)
    test_directory = os.path.join(parent_directory, test)
    os.mkdir(test_directory)
    return test_directory


def get_image_debug_path():
    parent, test = parse_module_path()
    path = os.path.join(parse_args().workdir, 'runs', get_run_id(), parent, test, 'debug_images')
    return path


def is_image_save_enabled():
    return parse_args().level == 10


def get_run_id():
    global _run_id
    return _run_id


def get_images_path():
    return os.path.join('images', get_os())


def is_multiprocessing_enabled():
    return multiprocessing.cpu_count() >= MIN_CPU_FOR_MULTIPROCESSING and get_os() != 'win'


def scroll(clicks):
    pyautogui.scroll(clicks)


def get_uhd_details():
    uhd_factor = SCREENSHOT_WIDTH / SCREEN_WIDTH
    is_uhd = True if uhd_factor > 1 else False
    return is_uhd, uhd_factor


def is_ocr_text(input_text):
    is_ocr_string = True
    pattern_extensions = ('.png', '.jpg')
    if input_text.endswith(pattern_extensions):
        is_ocr_string = False
    return is_ocr_string


def get_region(region=None, for_ocr=False):
    """Grabs image from region or full screen.

    :param Region || None region: Region param
    :param for_ocr: boolean param for ocr processing
    :return: Image
    """
    is_uhd, uhd_factor = get_uhd_details()

    if region is not None:
        r_x = uhd_factor * region.x if is_uhd else region.x
        r_y = uhd_factor * region.y if is_uhd else region.y
        r_w = uhd_factor * region.width if is_uhd else region.width
        r_h = uhd_factor * region.height if is_uhd else region.height

        grabbed_area = pyautogui.screenshot(region=(r_x, r_y, r_w, r_h))

        if is_uhd and not for_ocr:
            grabbed_area = grabbed_area.resize([region.width, region.height])
        return grabbed_area

    grabbed_area = pyautogui.screenshot(region=(0, 0, SCREENSHOT_WIDTH, SCREENSHOT_HEIGHT))

    if is_uhd and not for_ocr:
        return grabbed_area.resize([SCREEN_WIDTH, SCREEN_HEIGHT])
    else:
        return grabbed_area


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


def filter_list(original_list, exclude_list):
    new_list = []
    for item in original_list:
        if item not in exclude_list:
            new_list.append(item)
    return new_list


def get_git_details():
    repo_details = {}
    repo = git.Repo()
    repo_details['iris_version'] = 0.1
    repo_details['iris_repo'] = repo.working_tree_dir
    repo_details['iris_branch'] = repo.active_branch.name
    repo_details['iris_branch_head'] = repo.head.object.hexsha
    return repo_details


def shutdown_process(process_name):
    if get_os() == Platform.WINDOWS:
        command_str = 'taskkill /IM ' + process_name + '.exe'
        try:

            subprocess.Popen(command_str, shell=True, stdout=subprocess.PIPE)
        except subprocess.CalledProcessError:
            logger.error('Command  failed: "%s"' % command_str)
            raise Exception('Unable to run Command')
    elif get_os() == Platform.MAC or get_os() == Platform.LINUX:
        command_str = 'pkill ' + process_name
        try:
            subprocess.Popen(command_str, shell=True, stdout=subprocess.PIPE)
        except subprocess.CalledProcessError:
            logger.error('Command  failed: "%s"' % command_str)
            raise Exception('Unable to run Command')


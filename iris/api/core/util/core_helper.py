# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import datetime
import inspect
import logging
import multiprocessing
import os
import platform

import pyautogui

from parse_args import parse_args

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
    current_system = platform.system()
    current_os = ''
    if current_system == 'Windows':
        current_os = 'win'
    elif current_system == 'Linux':
        current_os = 'linux'
    elif current_system == 'Darwin':
        current_os = 'osx'
    else:
        logger.error('Iris does not yet support your current environment: ' + current_system)

    return current_os


def get_os_version():
    """Get the version string of the operating system your script is running on."""
    return platform.release()


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


def get_current_run_dir():
    return os.path.join(parse_args().workdir, 'runs', get_run_id())


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


def get_platform():
    return platform.machine()


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

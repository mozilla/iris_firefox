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

from helpers.parse_args import parse_args

SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()
SCREENSHOT_WIDTH, SCREENSHOT_HEIGHT = pyautogui.screenshot().size

SUCCESS_LEVEL_NUM = 35
logging.addLevelName(SUCCESS_LEVEL_NUM, 'SUCCESS')
args = parse_args()


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


def get_module_dir():
    return os.path.realpath(os.path.split(__file__)[0] + '/../..')


def get_image_debug_path():
    return get_module_dir() + '/image_debug'


def is_image_save_enabled():
    return args.level == 10


def get_run_id():
    return datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')


def get_images_path():
    return os.path.join('images', get_os())


def get_platform():
    return platform.machine()


def is_multiprocessing_enabled():
    return multiprocessing.cpu_count() >= MIN_CPU_FOR_MULTIPROCESSING


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


def scroll(clicks):
    pyautogui.scroll(clicks)


def get_uhd_details():
    uhd_factor = SCREENSHOT_WIDTH / SCREEN_WIDTH
    is_uhd = True if uhd_factor > 1 else False
    return is_uhd, uhd_factor

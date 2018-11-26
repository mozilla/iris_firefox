# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import mozinfo
import mss
import pyautogui
from util.parse_args import parse_args



class Platform(object):
    """Class that holds all the supported operating systems (HIGH_DEF = High definition displays)."""
    WINDOWS = 'win'
    LINUX = 'linux'
    MAC = 'osx'
    OS_NAME = mozinfo.os
    OS_VERSION = mozinfo.os_version
    OS_BITS = mozinfo.bits
    PROCESSOR = mozinfo.processor

    ALL = [LINUX, MAC, WINDOWS]

    primary_monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080} if parse_args().headless_run else mss.mss().monitors[1]
    _screenshot = mss.mss().grab(primary_monitor)
    SCREENSHOT_SIZE = (_screenshot.width, _screenshot.height)
    HIGH_DEF = SCREENSHOT_SIZE != pyautogui.size()
    SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()
    LOW_RES = (SCREEN_WIDTH < 1280 or SCREEN_HEIGHT < 800)

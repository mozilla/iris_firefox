# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import mozinfo
import os
import pyautogui

class Platform(object):
    """Class that holds all supported operating systems (HIGH_DEF = High definition displays)."""
    WINDOWS = 'win'
    LINUX = 'linux'
    MAC = 'osx'
    OS_NAME = mozinfo.os
    OS_VERSION = mozinfo.version
    OS_BITS = mozinfo.bits
    PROCESSOR = mozinfo.processor

    ALL = [LINUX, MAC, WINDOWS]
    tmp_file_path = os.path.join(os.path.realpath(os.path.split(__file__)[0] + '/../../..'), '.temp.png')
    HIGH_DEF = not (pyautogui.screenshot(tmp_file_path).size == pyautogui.size())
    SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()
    LOW_RES = (SCREEN_WIDTH < 1280 or SCREEN_HEIGHT < 800)

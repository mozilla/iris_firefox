# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import pyautogui

from iris.api.helpers.core_helper import get_os


class Platform(object):
    """Class that holds all supported operating systems (HIGH_DEF = High definition displays)."""
    WINDOWS = 'win'
    LINUX = 'linux'
    MAC = 'osx'
    ALL = get_os()
    HIGH_DEF = not (pyautogui.screenshot().size == pyautogui.size())
    SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()
    LOW_RES = (SCREEN_WIDTH < 1280 or SCREEN_HEIGHT < 800)

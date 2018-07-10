# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import time

import pyautogui

from image_search import SCREEN_WIDTH, SCREEN_HEIGHT
from platform_iris import Platform
from settings import Settings


class ZoomType(object):
    IN = 300 if Settings.isWindows() else 1
    OUT = -300 if Settings.isWindows() else -1


def zoom_with_mouse_wheel(nr_of_times=1, zoom_type=None):
    """Zoom in/Zoom out using the mouse wheel

    :param nr_of_times: Number of times the 'zoom in'/'zoom out' action should take place
    :param zoom_type: Type of the zoom action('zoom in'/'zoom out') intended to perform
    :return: None
    """

    # move focus in the middle of the page to be able to use the scroll
    pyautogui.moveTo(SCREEN_WIDTH / 4, SCREEN_HEIGHT / 2)
    for i in range(nr_of_times):
        if Settings.getOS() == Platform.MAC:
            pyautogui.keyDown('command')
        else:
            pyautogui.keyDown('ctrl')
        pyautogui.scroll(zoom_type)
        if Settings.getOS() == Platform.MAC:
            pyautogui.keyUp('command')
        else:
            pyautogui.keyUp('ctrl')
        time.sleep(0.5)
    pyautogui.moveTo(0, 0)

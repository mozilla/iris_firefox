# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from iris.api.core.pattern import Pattern
from iris.api.core.settings import *


class AuxiliaryWindow(object):
    if Settings.get_os() == Platform.MAC:
        AUXILIARY_WINDOW_CONTROLS = Pattern(
            'auxiliary_window_controls.png')
        RED_BUTTON_PATTERN = Pattern('unhovered_red_control.png').similar(0.9)
        HOVERED_RED_BUTTON = Pattern('hovered_red_button.png')
    else:
        CLOSE_BUTTON = Pattern('auxiliary_window_close_button.png')
        MAXIMIZE_BUTTON = Pattern('auxiliary_window_maximize.png')
        ZOOM_RESTORE_BUTTON = Pattern('minimize_full_screen_auxiliary_window.png')
        MINIMIZE_BUTTON = Pattern('auxiliary_window_minimize.png')


class MainWindow(object):
    if Settings.get_os() == Platform.MAC:
        MAIN_WINDOW_CONTROLS = Pattern('main_window_controls.png')
        UNHOVERED_MAIN_RED_CONTROL = Pattern('unhovered_main_red_control.png')
        HOVERED_MAIN_RED_CONTROL = Pattern('hovered_red_main_control.png')
    else:
        CLOSE_BUTTON = Pattern('main_close_control.png')
        MINIMIZE_BUTTON = Pattern('main_minimize_control.png')
        MAXIMIZE_BUTTON = Pattern('main_maximize_control.png')
        RESIZE_BUTTON = Pattern('main_resize_control.png')

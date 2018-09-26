# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from platform import Platform
from util.core_helper import get_os, get_os_version
from util.parse_args import parse_args

DEFAULT_MIN_SIMILARITY = 0.8
DEFAULT_SLOW_MOTION_DELAY = 2
DEFAULT_MOVE_MOUSE_DELAY = parse_args().mouse
DEFAULT_OBSERVE_MIN_CHANGED_PIXELS = 50
DEFAULT_TYPE_DELAY = 0
DEFAULT_CLICK_DELAY = 0
DEFAULT_WAIT_SCAN_RATE = 3
DEFAULT_OBSERVE_SCAN_RATE = 3
DEFAULT_AUTO_WAIT_TIMEOUT = 3
DEFAULT_DELAY_BEFORE_MOUSE_DOWN = 0.3
DEFAULT_DELAY_BEFORE_DRAG = 0.3
DEFAULT_DELAY_BEFORE_DROP = 0.3
DEFAULT_SPOTLIGHT_DURATION = 2
DEFAULT_FX_DELAY = 0.5
DEFAULT_UI_DELAY = 1
DEFAULT_UI_DELAY_LONG = 2.5
DEFAULT_SYSTEM_DELAY = 5
DEFAULT_FIREFOX_TIMEOUT = 10

BETA = 'beta'
RELEASE = 'release'
NIGHTLY = 'nightly'
ESR = 'esr'


class _IrisSettings(object):

    def __init__(self):
        self._wait_scan_rate = DEFAULT_WAIT_SCAN_RATE
        self._type_delay = DEFAULT_TYPE_DELAY
        self._move_mouse_delay = DEFAULT_MOVE_MOUSE_DELAY
        self._click_delay = DEFAULT_CLICK_DELAY
        self._min_similarity = DEFAULT_MIN_SIMILARITY
        self._auto_wait_timeout = DEFAULT_AUTO_WAIT_TIMEOUT
        self._delay_before_mouse_down = DEFAULT_DELAY_BEFORE_MOUSE_DOWN
        self._delay_before_drag = DEFAULT_DELAY_BEFORE_DRAG
        self._delay_before_drop = DEFAULT_DELAY_BEFORE_DROP
        self._slow_motion_delay = DEFAULT_SLOW_MOTION_DELAY
        self._observe_scan_rate = DEFAULT_OBSERVE_SCAN_RATE
        self._observe_min_changed_pixels = DEFAULT_OBSERVE_MIN_CHANGED_PIXELS
        self._spotlight_duration = DEFAULT_SPOTLIGHT_DURATION
        self._fx_delay = DEFAULT_FX_DELAY
        self._ui_delay = DEFAULT_UI_DELAY
        self._ui_delay_long = DEFAULT_UI_DELAY_LONG
        self._system_delay = DEFAULT_SYSTEM_DELAY
        self._channels = [BETA, RELEASE, NIGHTLY, ESR]
        self._locales = ['en-US', 'zh-CN', 'es-ES', 'de', 'fr', 'ru', 'ar', 'ko', 'pt-PT', 'vi', 'pl', 'tr', 'ro', 'ja']
        self._firefox_timeout = DEFAULT_FIREFOX_TIMEOUT

    @property
    def FX_DELAY(self):
        """Getter for the fx_delay property."""
        return self._fx_delay

    @property
    def UI_DELAY(self):
        """Getter for the ui_delay property."""
        return self._ui_delay

    @property
    def UI_DELAY_LONG(self):
        """Getter for the ui_delay_long property."""
        return self._ui_delay_long

    @property
    def SYSTEM_DELAY(self):
        """Getter for the system_delay property."""
        return self._system_delay

    @property
    def CHANNELS(self):
        """Getter for the channels property."""
        return self._channels

    @property
    def LOCALES(self):
        """Getter for the locales property."""
        return self._locales

    @property
    def FIREFOX_TIMEOUT(self):
        return self._firefox_timeout

    @property
    def wait_scan_rate(self):
        """Getter for the wait_scan_rate property."""
        return self._wait_scan_rate

    @wait_scan_rate.setter
    def wait_scan_rate(self, value):
        """Setter for the wait_scan_rate property."""
        self._wait_scan_rate = value

    @property
    def type_delay(self):
        """Getter for the type_delay property."""
        return self._type_delay

    @type_delay.setter
    def type_delay(self, value):
        """Setter for the type_delay property."""
        if value > 1:
            self._type_delay = 1
        else:
            self._type_delay = value

    @property
    def move_mouse_delay(self):
        """Getter for the move_mouse_delay property."""
        return self._move_mouse_delay

    @move_mouse_delay.setter
    def move_mouse_delay(self, value):
        """Setter for the move_mouse_delay property."""
        self._move_mouse_delay = value

    @property
    def click_delay(self):
        """Getter for the click_delay property."""
        return self._click_delay

    @click_delay.setter
    def click_delay(self, value):
        """Setter for the click_delay property."""
        if value > 1:
            self._click_delay = 1
        else:
            self._click_delay = value

    @property
    def min_similarity(self):
        """Getter for the min_similarity property."""
        return self._min_similarity

    @min_similarity.setter
    def min_similarity(self, value):
        """Setter for the min_similarity property."""
        if value > 1:
            self._min_similarity = 1
        else:
            self._min_similarity = value

    @property
    def auto_wait_timeout(self):
        """Getter for the auto_wait_timeout property."""
        return self._auto_wait_timeout

    @auto_wait_timeout.setter
    def auto_wait_timeout(self, value):
        """Setter for the auto_wait_timeout property."""
        self._auto_wait_timeout = value

    @property
    def delay_before_mouse_down(self):
        """Getter for the delay_before_mouse_down property."""
        return self._delay_before_mouse_down

    @delay_before_mouse_down.setter
    def delay_before_mouse_down(self, value):
        """Setter for the delay_before_mouse_down property."""
        self._delay_before_mouse_down = value

    @property
    def delay_before_drag(self):
        """Getter for the delay_before_drag property."""
        return self._delay_before_drag

    @delay_before_drag.setter
    def delay_before_drag(self, value):
        """Setter for the delay_before_drag property."""
        self._delay_before_drag = value

    @property
    def delay_before_drop(self):
        """Getter for the delay_before_drop property."""
        return self._delay_before_drop

    @delay_before_drop.setter
    def delay_before_drop(self, value):
        """Setter for the delay_before_drop property."""
        self._delay_before_drop = value

    @property
    def slow_motion_delay(self):
        """Getter for the slow_motion_delay property."""
        return self._slow_motion_delay

    @slow_motion_delay.setter
    def slow_motion_delay(self, value):
        """Setter for the slow_motion_delay property."""
        self._slow_motion_delay = value

    @property
    def observe_scan_rate(self):
        """Getter for the observe_scan_rate property."""
        return self._observe_scan_rate

    @observe_scan_rate.setter
    def observe_scan_rate(self, value):
        """Setter for the observe_scan_rate property."""
        self._observe_scan_rate = value

    @property
    def observe_min_changed_pixels(self):
        """Getter for the observe_min_changed_pixels property."""
        return self._observe_min_changed_pixels

    @observe_min_changed_pixels.setter
    def observe_min_changed_pixels(self, value):
        """Setter for the observe_min_changed_pixels property."""
        self._observe_min_changed_pixels = value

    @property
    def spotlight_duration(self):
        """Getter for the spotlight_duration property."""
        return self._spotlight_duration

    @spotlight_duration.setter
    def spotlight_duration(self, value):
        """Setter for the spotlight_duration property."""
        self._spotlight_duration = value

    @staticmethod
    def get_os():
        """Get the type of the operating system your script is running on."""
        return get_os()

    @staticmethod
    def get_os_version():
        """Get the version string of the operating system your script is running on."""
        return get_os_version()

    @staticmethod
    def is_linux():
        """Checks if we are running on a Linux system.

        :return: True if we are running on a Linux system, False otherwise.
        """
        return get_os() == Platform.LINUX

    @staticmethod
    def is_mac():
        """Checks if we are running on a Mac system.

        :return: True if we are running on a Mac system, False otherwise.
        """
        return get_os() == Platform.MAC

    @staticmethod
    def is_windows():
        """Checks if we are running on a Windows system.

        :return: True if we are running on a Windows system, False otherwise.
        """
        return get_os() == Platform.WINDOWS


Settings = _IrisSettings()

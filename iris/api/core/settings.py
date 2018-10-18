# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from platform import Platform
from util.color import Color
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
DEFAULT_HIGHLIGHT_DURATION = 2
DEFAULT_HIGHLIGHT_COLOR = Color.RED
DEFAULT_HIGHLIGHT_THICKNESS = 2
DEFAULT_FX_DELAY = 0.5
DEFAULT_UI_DELAY = 1
DEFAULT_UI_DELAY_LONG = 2.5
DEFAULT_SYSTEM_DELAY = 5
DEFAULT_FIREFOX_TIMEOUT = 10

BETA = 'beta'
RELEASE = 'release'
NIGHTLY = 'nightly'
ESR = 'esr'
DEV_EDITION = 'dev'


class _IrisSettings(object):

    def __init__(self):
        """Function assign values to multiple Settings properties."""

        """How often a search during the wait takes place."""
        self._wait_scan_rate = DEFAULT_WAIT_SCAN_RATE

        """The number of seconds between each keyboard press."""
        self._type_delay = DEFAULT_TYPE_DELAY

        """Speed of hovering from current location to target."""
        self._move_mouse_delay = DEFAULT_MOVE_MOUSE_DELAY

        """Speed of clicking on a target."""
        self._click_delay = DEFAULT_CLICK_DELAY

        """The minimum similarity to use in a find operation. The value should be between 0 and 1."""
        self._min_similarity = DEFAULT_MIN_SIMILARITY

        """The maximum waiting time for all subsequent find operations."""
        self._auto_wait_timeout = DEFAULT_AUTO_WAIT_TIMEOUT

        """Delay before the mouse is put in a held down state."""
        self._delay_before_mouse_down = DEFAULT_DELAY_BEFORE_MOUSE_DOWN

        """Delay before the drag operation takes place."""
        self._delay_before_drag = DEFAULT_DELAY_BEFORE_DRAG

        """Delay before the drop operation takes place."""
        self._delay_before_drop = DEFAULT_DELAY_BEFORE_DROP

        """Control the duration of the visual effect (seconds)."""
        self._slow_motion_delay = DEFAULT_SLOW_MOTION_DELAY

        """Specify the number of times actual search operations are performed per second while waiting for a pattern to 
        appear or vanish."""
        self._observe_scan_rate = DEFAULT_OBSERVE_SCAN_RATE

        """The minimum size in pixels of a change to trigger a change event."""
        self._observe_min_changed_pixels = DEFAULT_OBSERVE_MIN_CHANGED_PIXELS

        """Highlight the region for some period of time."""
        self._highlight_duration = DEFAULT_HIGHLIGHT_DURATION

        """Color used to highlight a region or a pattern."""
        self._highlight_color = DEFAULT_HIGHLIGHT_COLOR

        """Thickness highlight used."""
        self._highlight_thickness = DEFAULT_HIGHLIGHT_THICKNESS

        """This is a minimal pause like waiting for an element to become active for input or interaction."""
        self._fx_delay = DEFAULT_FX_DELAY

        """Similar to DEFAULT_FX_DELAY, but may have some underlying issue that makes for even longer time for an 
        element to become active."""
        self._ui_delay = DEFAULT_UI_DELAY

        """The delay here can be due to things like waiting on content to load from a page, but the UI under test 
        doesn't dynamically change as the content is served."""
        self._ui_delay_long = DEFAULT_UI_DELAY_LONG

        """Similar to DEFAULT_UI_DELAY_LONG, but covers a broader spectrum of wait situations from slow network to slow 
        system response times."""
        self._system_delay = DEFAULT_SYSTEM_DELAY

        """A list of channels supported by Iris."""
        self._channels = [BETA, RELEASE, NIGHTLY, ESR, DEV_EDITION]

        """A list of Firefox locales used by Iris."""
        self._locales = ['en-US', 'zh-CN', 'es-ES', 'de', 'fr', 'ru', 'ar', 'ko', 'pt-PT', 'vi', 'pl', 'tr', 'ro', 'ja']

        """Maximum time to wait until closing the Firefox."""
        self._firefox_timeout = DEFAULT_FIREFOX_TIMEOUT

    @property
    def FX_DELAY(self):
        """Getter for the _fx_delay property."""
        return self._fx_delay

    @property
    def UI_DELAY(self):
        """Getter for the _ui_delay property."""
        return self._ui_delay

    @property
    def UI_DELAY_LONG(self):
        """Getter for the _ui_delay_long property."""
        return self._ui_delay_long

    @property
    def SYSTEM_DELAY(self):
        """Getter for the _system_delay property."""
        return self._system_delay

    @property
    def CHANNELS(self):
        """Getter for the _channels property."""
        return self._channels

    @property
    def LOCALES(self):
        """Getter for the _locales property."""
        return self._locales

    @property
    def FIREFOX_TIMEOUT(self):
        """Getter for the _firefox_timeout property."""
        return self._firefox_timeout

    @property
    def wait_scan_rate(self):
        """Getter for the _wait_scan_rate property."""
        return self._wait_scan_rate

    @wait_scan_rate.setter
    def wait_scan_rate(self, value):
        """Setter for the _wait_scan_rate property."""
        self._wait_scan_rate = value

    @property
    def type_delay(self):
        """Getter for the _type_delay property."""
        return self._type_delay

    @type_delay.setter
    def type_delay(self, value):
        """Setter for the _type_delay property."""
        if value > 1:
            self._type_delay = 1
        else:
            self._type_delay = value

    @property
    def move_mouse_delay(self):
        """Getter for the _move_mouse_delay property."""
        return self._move_mouse_delay

    @move_mouse_delay.setter
    def move_mouse_delay(self, value):
        """Setter for the move_mouse_delay property."""
        self._move_mouse_delay = value

    @property
    def click_delay(self):
        """Getter for the _click_delay property."""
        return self._click_delay

    @click_delay.setter
    def click_delay(self, value):
        """Setter for the _click_delay property."""
        if value > 1:
            self._click_delay = 1
        else:
            self._click_delay = value

    @property
    def min_similarity(self):
        """Getter for the _min_similarity property."""
        return self._min_similarity

    @min_similarity.setter
    def min_similarity(self, value):
        """Setter for the _min_similarity property."""
        if value > 1:
            self._min_similarity = 1
        else:
            self._min_similarity = value

    @property
    def auto_wait_timeout(self):
        """Getter for the _auto_wait_timeout property."""
        return self._auto_wait_timeout

    @auto_wait_timeout.setter
    def auto_wait_timeout(self, value):
        """Setter for the _auto_wait_timeout property."""
        self._auto_wait_timeout = value

    @property
    def delay_before_mouse_down(self):
        """Getter for the _delay_before_mouse_down property."""
        return self._delay_before_mouse_down

    @delay_before_mouse_down.setter
    def delay_before_mouse_down(self, value):
        """Setter for the _delay_before_mouse_down property."""
        self._delay_before_mouse_down = value

    @property
    def delay_before_drag(self):
        """Getter for the _delay_before_drag property."""
        return self._delay_before_drag

    @delay_before_drag.setter
    def delay_before_drag(self, value):
        """Setter for the _delay_before_drag property."""
        self._delay_before_drag = value

    @property
    def delay_before_drop(self):
        """Getter for the _delay_before_drop property."""
        return self._delay_before_drop

    @delay_before_drop.setter
    def delay_before_drop(self, value):
        """Setter for the _delay_before_drop property."""
        self._delay_before_drop = value

    @property
    def slow_motion_delay(self):
        """Getter for the _slow_motion_delay property."""
        return self._slow_motion_delay

    @slow_motion_delay.setter
    def slow_motion_delay(self, value):
        """Setter for the _slow_motion_delay property."""
        self._slow_motion_delay = value

    @property
    def observe_scan_rate(self):
        """Getter for the observe_scan_rate property."""
        return self._observe_scan_rate

    @observe_scan_rate.setter
    def observe_scan_rate(self, value):
        """Setter for the _observe_scan_rate property."""
        self._observe_scan_rate = value

    @property
    def observe_min_changed_pixels(self):
        """Getter for the _observe_min_changed_pixels property."""
        return self._observe_min_changed_pixels

    @observe_min_changed_pixels.setter
    def observe_min_changed_pixels(self, value):
        """Setter for the _observe_min_changed_pixels property."""
        self._observe_min_changed_pixels = value

    @property
    def highlight_duration(self):
        """Getter for the highlight_duration property."""
        return self._highlight_duration

    @highlight_duration.setter
    def highlight_duration(self, value):
        """Setter for the _highlight_duration property."""
        self._highlight_duration = value

    @property
    def highlight_color(self):
        """Getter for the _highlight_color property."""
        return self._highlight_color

    @highlight_color.setter
    def highlight_color(self, value):
        """Setter for the _highlight_color property."""
        self._highlight_color = value

    @property
    def highlight_thickness(self):
        """Getter for the highlight_thickness property."""
        return self._highlight_thickness

    @highlight_thickness.setter
    def highlight_thickness(self, value):
        """Setter for the _highlight_thickness property."""
        self._highlight_thickness = value

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

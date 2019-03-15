# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from platform import Platform
from util.color import Color
from util.core_helper import get_os, get_os_version
from util.parse_args import parse_args

DEFAULT_MIN_SIMILARITY = 0.8
DEFAULT_SLOW_MOTION_DELAY = 2
DEFAULT_OBSERVE_MIN_CHANGED_PIXELS = 50
DEFAULT_TYPE_DELAY = 0
DEFAULT_MOVE_MOUSE_DELAY = parse_args().mouse
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
DEFAULT_TINY_FIREFOX_TIMEOUT = 3
DEFAULT_SHORT_FIREFOX_TIMEOUT = 5
DEFAULT_FIREFOX_TIMEOUT = 10
DEFAULT_SITE_LOAD_TIMEOUT = 30
DEFAULT_HEAVY_SITE_LOAD_TIMEOUT = 90


CHANNELS = ('beta', 'release', 'nightly', 'esr', 'dev')
LOCALES = ('en-US', 'zh-CN', 'es-ES', 'de', 'fr', 'ru', 'ar', 'ko', 'pt-PT', 'vi',
           'pl', 'tr', 'ro', 'ja' ,'it', 'pt-BR', 'in', 'en-GB', 'id', 'ca', 'be',
           'kk')


class _IrisSettings(object):
    """Class that holds general Iris settings.

    wait_scan_rate              -   The number of times actual pattern search operations are performed per second.
                                    (default - 3)
    type_delay                  -   The number of seconds between each keyboard press. (default - 0)
    move_mouse_delay            -   duration of mouse movement from current location to target location. (default - 0.5
                                    or value selected from Control Center)
    click_delay                 -   The number of seconds a click event is executed after the mouse moves to the target
                                    location. (default - 0)
    min_similarity              -   The default minimum similarity of find operations. While using a Region.find()
                                    operation. Iris searches the region using a default minimum similarity of 0.8.
    auto_wait_timeout           -   The maximum waiting time for all subsequent find operations. (default - 3)
    delay_before_mouse_down     -   Delay before the mouse is put in a held down state.
    delay_before_drag           -   Delay before the drag operation takes place.
    delay_before_drop           -   Delay before the drop operation takes place.
    slow_motion_delay           -   Controls the duration of the visual effect (seconds).
    observe_scan_rate           -   The number of times actual search operations are performed per second while waiting
                                    for a pattern to appear or vanish.
    observe_min_changed_pixels  -   The minimum size in pixels of a change to trigger a change event.
    highlight_duration          -   The duration of the highlight effect.
    highlight_color             -   The rectangle/circle border color for the highlight effect.
    highlight_thickness         -   The rectangle/circle border thickness for the highlight effect.
    fx_delay                    -   This is a minimal pause like waiting for an element to become active for input
                                    or interaction.
    ui_delay                    -   Similar to DEFAULT_FX_DELAY, but may have some underlying issue that makes for
                                    even longer time for an element to become active.
    ui_delay_long               -   The delay here can be due to things like waiting on content to load from a page,
                                    but the UI under test doesn't dynamically change as the content is served.
    system_delay                -   Similar to DEFAULT_UI_DELAY_LONG, but covers a broader spectrum of wait situations
                                    from slow network to slow system response times.
    channels                    -   A list of channels supported by Iris.
    locales                     -   A list of Firefox locales supported by Iris.
    firefox_timeout             -   Maximum time to wait until closing the Firefox.
    firefox_tiny_timeout        -   Minimum time to wait until closing the Firefox.
    firefox_short_timeout       -   Standard time to wait until closing the Firefox.
    site_load_timeout           -   Standard time to wait for web site loading.
    heavy_site_load_timeout     -   Maximum time to wait for web site loading.

    """

    def __init__(self, wait_scan_rate=DEFAULT_WAIT_SCAN_RATE, type_delay=DEFAULT_TYPE_DELAY,
                 move_mouse_delay=DEFAULT_MOVE_MOUSE_DELAY, click_delay=DEFAULT_CLICK_DELAY,
                 min_similarity=DEFAULT_MIN_SIMILARITY, auto_wait_timeout=DEFAULT_AUTO_WAIT_TIMEOUT,
                 delay_before_mouse_down=DEFAULT_DELAY_BEFORE_MOUSE_DOWN,
                 delay_before_drag=DEFAULT_DELAY_BEFORE_DRAG,
                 delay_before_drop=DEFAULT_DELAY_BEFORE_DROP,
                 slow_motion_delay=DEFAULT_SLOW_MOTION_DELAY,
                 observe_scan_rate=DEFAULT_OBSERVE_SCAN_RATE,
                 observe_min_changed_pixels=DEFAULT_OBSERVE_MIN_CHANGED_PIXELS,
                 highlight_duration=DEFAULT_HIGHLIGHT_DURATION,
                 highlight_color=DEFAULT_HIGHLIGHT_COLOR,
                 highlight_thickness=DEFAULT_HIGHLIGHT_THICKNESS,
                 fx_delay=DEFAULT_FX_DELAY, ui_delay=DEFAULT_UI_DELAY,
                 ui_delay_long=DEFAULT_UI_DELAY_LONG, system_delay=DEFAULT_SYSTEM_DELAY,
                 channels=CHANNELS, locales=LOCALES, firefox_timeout=DEFAULT_FIREFOX_TIMEOUT,
                 tiny_firefox_timeout=DEFAULT_TINY_FIREFOX_TIMEOUT,
                 short_firefox_timeout=DEFAULT_SHORT_FIREFOX_TIMEOUT,
                 site_load_timeout=DEFAULT_SITE_LOAD_TIMEOUT,
                 heavy_site_load_timeout=DEFAULT_HEAVY_SITE_LOAD_TIMEOUT):

        self.wait_scan_rate = wait_scan_rate
        self._type_delay = type_delay
        self.move_mouse_delay = move_mouse_delay
        self._click_delay = click_delay
        self._min_similarity = min_similarity
        self.auto_wait_timeout = auto_wait_timeout
        self.delay_before_mouse_down = delay_before_mouse_down
        self.delay_before_drag = delay_before_drag
        self.delay_before_drop = delay_before_drop
        self.slow_motion_delay = slow_motion_delay
        self.observe_scan_rate = observe_scan_rate
        self.observe_min_changed_pixels = observe_min_changed_pixels
        self.highlight_duration = highlight_duration
        self.highlight_color = highlight_color
        self.highlight_thickness = highlight_thickness
        self.fx_delay = fx_delay
        self.ui_delay = ui_delay
        self.ui_delay_long = ui_delay_long
        self.system_delay = system_delay
        self.channels = channels
        self.locales = locales
        self.firefox_timeout = firefox_timeout
        self.tiny_firefox_timeout = tiny_firefox_timeout
        self.short_firefox_timeout = short_firefox_timeout
        self.site_load_timeout = site_load_timeout
        self.heavy_site_load_timeout = heavy_site_load_timeout

    @property
    def FX_DELAY(self):
        return self.fx_delay

    @property
    def UI_DELAY(self):
        return self.ui_delay

    @property
    def UI_DELAY_LONG(self):
        return self.ui_delay_long

    @property
    def SYSTEM_DELAY(self):
        return self.system_delay

    @property
    def CHANNELS(self):
        return self.channels

    @property
    def LOCALES(self):
        return self.locales

    @property
    def FIREFOX_TIMEOUT(self):
        return self.firefox_timeout

    @property
    def TINY_FIREFOX_TIMEOUT(self):
        return self.tiny_firefox_timeout

    @property
    def SHORT_FIREFOX_TIMEOUT(self):
        return self.short_firefox_timeout

    @property
    def SITE_LOAD_TIMEOUT(self):
        return self.site_load_timeout

    @property
    def HEAVY_SITE_LOAD_TIMEOUT(self):
        return self.heavy_site_load_timeout

    @property
    def type_delay(self):
        return self._type_delay

    @type_delay.setter
    def type_delay(self, value):
        if value > 1:
            self._type_delay = 1
        else:
            self._type_delay = value

    @property
    def click_delay(self):
        return self._click_delay

    @click_delay.setter
    def click_delay(self, value):
        if value > 1:
            self._click_delay = 1
        else:
            self._click_delay = value

    @property
    def min_similarity(self):
        return self._min_similarity

    @min_similarity.setter
    def min_similarity(self, value):
        if value > 1:
            self._min_similarity = 1
        else:
            self._min_similarity = value

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

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from core_helper import get_os, get_os_version
from helpers.parse_args import parse_args
from platform_iris import Platform

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
DEFAULT_FX_DELAY = 0.5
DEFAULT_UI_DELAY = 1
DEFAULT_UI_DELAY_LONG = 2.5
DEFAULT_SYSTEM_DELAY = 5


class _IrisSettings(object):
    _wait_scan_rate = DEFAULT_WAIT_SCAN_RATE
    _type_delay = DEFAULT_TYPE_DELAY
    _move_mouse_delay = DEFAULT_MOVE_MOUSE_DELAY
    _click_delay = DEFAULT_CLICK_DELAY
    _min_similarity = DEFAULT_MIN_SIMILARITY
    _auto_wait_timeout = DEFAULT_AUTO_WAIT_TIMEOUT
    _delay_before_mouse_down = DEFAULT_DELAY_BEFORE_MOUSE_DOWN
    _delay_before_drag = DEFAULT_DELAY_BEFORE_DRAG
    _delay_before_drop = DEFAULT_DELAY_BEFORE_DROP
    _slow_motion_delay = DEFAULT_SLOW_MOTION_DELAY
    _observe_scan_rate = DEFAULT_OBSERVE_SCAN_RATE
    _observe_min_changed_pixels = DEFAULT_OBSERVE_MIN_CHANGED_PIXELS
    _fx_delay = DEFAULT_FX_DELAY
    _ui_delay = DEFAULT_UI_DELAY
    _ui_delay_long = DEFAULT_UI_DELAY_LONG
    _system_delay = DEFAULT_SYSTEM_DELAY

    def __init__(self):
        self._wait_scan_rate = self.WaitScanRate
        self._type_delay = self.TypeDelay
        self._move_mouse_delay = self.MoveMouseDelay
        self._click_delay = self.ClickDelay
        self._min_similarity = self.MinSimilarity
        self._auto_wait_timeout = self.AutoWaitTimeout
        self._delay_before_mouse_down = self.DelayBeforeMouseDown
        self._delay_before_drag = self.DelayBeforeDrag
        self._delay_before_drop = self.DelayBeforeDrop
        self._slow_motion_delay = self.SlowMotionDelay
        self._observe_scan_rate = self.ObserveScanRate
        self._observe_min_changed_pixels = self.ObserveMinChangedPixels
        self._fx_delay = self.FX_DELAY
        self._ui_delay = self.UI_DELAY
        self._ui_delay_long = self.UI_DELAY_LONG
        self._system_delay = self.SYSTEM_DELAY

    @property
    def FX_DELAY(self):
        return self._fx_delay

    @FX_DELAY.setter
    def FX_DELAY(self, value):
        self._fx_delay = value

    @property
    def UI_DELAY(self):
        return self._ui_delay

    @UI_DELAY.setter
    def UI_DELAY(self, value):
        self._ui_delay = value

    @property
    def UI_DELAY_LONG(self):
        return self._ui_delay_long

    @UI_DELAY_LONG.setter
    def UI_DELAY_LONG(self, value):
        self._ui_delay_long = value

    @property
    def SYSTEM_DELAY(self):
        return self._system_delay

    @SYSTEM_DELAY.setter
    def SYSTEM_DELAY(self, value):
        self._system_delay = value

    @property
    def WaitScanRate(self):
        return self._wait_scan_rate

    @WaitScanRate.setter
    def WaitScanRate(self, value):
        self._wait_scan_rate = value

    @property
    def TypeDelay(self):
        return self._type_delay

    @TypeDelay.setter
    def TypeDelay(self, value):
        if value > 1:
            self._type_delay = 1
        else:
            self._type_delay = value

    @property
    def MoveMouseDelay(self):
        return self._move_mouse_delay

    @MoveMouseDelay.setter
    def MoveMouseDelay(self, value):
        self._move_mouse_delay = value

    @property
    def ClickDelay(self):
        return self._click_delay

    @ClickDelay.setter
    def ClickDelay(self, value):
        if value > 1:
            self._click_delay = 1
        else:
            self._click_delay = value

    @property
    def MinSimilarity(self):
        return self._min_similarity

    @MinSimilarity.setter
    def MinSimilarity(self, value):
        if value > 1:
            self._min_similarity = 1
        else:
            self._min_similarity = value

    @property
    def AutoWaitTimeout(self):
        return self._auto_wait_timeout

    @AutoWaitTimeout.setter
    def AutoWaitTimeout(self, value):
        self._auto_wait_timeout = value

    @property
    def DelayBeforeMouseDown(self):
        return self._delay_before_mouse_down

    @DelayBeforeMouseDown.setter
    def DelayBeforeMouseDown(self, value):
        self._delay_before_mouse_down = value

    @property
    def DelayBeforeDrag(self):
        return self._delay_before_drag

    @DelayBeforeDrag.setter
    def DelayBeforeDrag(self, value):
        self._delay_before_drag = value

    @property
    def DelayBeforeDrop(self):
        return self._delay_before_drop

    @DelayBeforeDrop.setter
    def DelayBeforeDrop(self, value):
        self._delay_before_drop = value

    @property
    def SlowMotionDelay(self):
        return self._slow_motion_delay

    @SlowMotionDelay.setter
    def SlowMotionDelay(self, value):
        self._slow_motion_delay = value

    @property
    def ObserveScanRate(self):
        return self._observe_scan_rate

    @ObserveScanRate.setter
    def ObserveScanRate(self, value):
        self._observe_scan_rate = value

    @property
    def ObserveMinChangedPixels(self):
        return self._observe_min_changed_pixels

    @ObserveMinChangedPixels.setter
    def ObserveMinChangedPixels(self, value):
        self._observe_min_changed_pixels = value

    @staticmethod
    def getOS():
        """Get the type of the operating system your script is running on."""
        return get_os()

    @staticmethod
    def getOSVersion():
        """Get the version string of the operating system your script is running on."""
        return get_os_version()

    @staticmethod
    def isLinux():
        """Checks if we are running on a Linux system.

        :return: True if we are running on a Linux system, False otherwise
        """
        return get_os() == Platform.LINUX

    @staticmethod
    def isMac():
        """Checks if we are running on a Mac system.

        :return: True if we are running on a Mac system, False otherwise
        """
        return get_os() == Platform.MAC

    @staticmethod
    def isWindows():
        """Checks if we are running on a Windows system.

        :return: True if we are running on a Windows system, False otherwise
        """
        return get_os() == Platform.WINDOWS


Settings = _IrisSettings()

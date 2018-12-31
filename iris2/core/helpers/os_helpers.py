# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


import mozinfo
import mss
import multiprocessing

from iris2.core.enums import OSPlatform
from iris2.core.errors import APIHelperError

OS_NAME = mozinfo.os
OS_VERSION = mozinfo.os_version
MONITORS = mss.mss().monitors[1:]
MULTI_MONITOR_AREA = mss.mss().monitors[0]


class OSHelper:

    @staticmethod
    def is_high_def_display():
        """Checks if the primary display is high definition."""
        main_display = MONITORS[0]
        screenshot = mss.mss().grab(main_display)
        if screenshot.width > main_display['width'] or screenshot.height > main_display['height']:
            return True
        return False

    @staticmethod
    def get_display_factor():
        main_display = MONITORS[0]
        screenshot = mss.mss().grab(main_display)
        display_factor = screenshot.width / screenshot.height
        return display_factor

    @staticmethod
    def get_os():
        """Get the type of the operating system your script is running on."""
        if OS_NAME == 'win':
            return OSPlatform.WINDOWS
        elif OS_NAME == 'linux':
            return OSPlatform.LINUX
        elif OS_NAME == 'mac':
            return OSPlatform.MAC
        else:
            raise APIHelperError('Iris does not yet support your current environment: %s' % OS_NAME)

    @staticmethod
    def is_mac():
        """Checks if we are running on a Mac system.

        :return: True if we are running on a Mac system, False otherwise.
        """
        return OSHelper.get_os() is OSPlatform.MAC

    @staticmethod
    def is_windows():
        """Checks if we are running on a Windows system.

         :return: True if we are running on a Windows system, False otherwise.
        """
        return OSHelper.get_os() is OSPlatform.WINDOWS

    @staticmethod
    def is_linux():
        """Checks if we are running on a Linux system.

        :return: True if we are running on a Linux system, False otherwise.
        """
        return OSHelper.get_os() is OSPlatform.LINUX

    @staticmethod
    def get_os_version():
        """Get the version string of the operating system your script is running on."""
        current_os = OSHelper.get_os()
        if current_os is OSPlatform.WINDOWS and OS_VERSION == '6.1':
            return 'win7'
        elif current_os is OSPlatform.MAC:
            return 'osx_%s' % 'retina ' if OSHelper.is_high_def_display() else 'non_retina'
        else:
            return current_os

    @staticmethod
    def use_multiprocessing():
        return multiprocessing.cpu_count() >= 4 and OSHelper.get_os() != 'win'

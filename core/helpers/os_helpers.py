# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


import mozinfo
import mss

from core.enums import OSPlatform
from core.errors import APIHelperError

OS_NAME = mozinfo.os
OS_VERSION = mozinfo.os_version


class OSHelper:

    @staticmethod
    def is_high_def_display():
        """Checks if the primary display is high definition."""
        main_display = mss.mss().monitors[1]
        screenshot = mss.mss().grab(main_display)
        if screenshot.width > main_display['width'] or screenshot.height > main_display['height']:
            return True
        return False

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
    def get_os_version():
        """Get the version string of the operating system your script is running on."""
        current_os = OSHelper.get_os()
        if current_os is OSPlatform.WINDOWS and OS_VERSION == '6.1':
            return 'win7'
        elif current_os is OSPlatform.MAC:
            return 'osx_%s' % 'retina ' if OSHelper.is_high_def_display() else 'non_retina'
        else:
            return current_os

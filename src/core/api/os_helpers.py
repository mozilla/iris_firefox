# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


import multiprocessing

import mozinfo
import mss
import os
import time

from src.core.api.enums import OSPlatform
from src.core.api.errors import APIHelperError

OS_NAME = mozinfo.os
OS_VERSION = mozinfo.os_version
OS_BITS = mozinfo.bits
PROCESSOR = mozinfo.processor

MONITORS = mss.mss().monitors[1:]
MULTI_MONITOR_AREA = mss.mss().monitors[0]


class OSHelper:

    LOCALES = ['en-US', 'zh-CN', 'es-ES', 'de', 'fr', 'ru', 'ar', 'ko', 'pt-PT', 'vi',
               'pl', 'tr', 'ro', 'ja' ,'it', 'pt-BR', 'in', 'en-GB', 'id', 'ca', 'be', 'kk']

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
    def get_os_bits():
        return mozinfo.bits

    @staticmethod
    def get_processor():
        return mozinfo.processor

    @staticmethod
    def use_multiprocessing():
        return multiprocessing.cpu_count() >= 4 and OSHelper.get_os() != 'win'

    @staticmethod
    def _is_locked(filepath):
        """Checks if a file is locked by opening it in append mode.
        If no exception thrown, then the file is not locked.
        """
        locked = None
        file_object = None
        if os.path.exists(filepath):
            try:
                print ("Trying to open %s." % filepath)
                buffer_size = 8
                # Opening file in append mode and read the first 8 characters.
                file_object = open(filepath, 'a', buffer_size)
                if file_object:
                    print ("%s is not locked." % filepath)
                    locked = False
            except IOError as message:
                print( "File is locked (unable to open in append mode). %s." % \
                      message)
                locked = True
            finally:
                if file_object:
                    file_object.close()
                    print( "%s closed." % filepath)
        else:
            print( "%s not found." % filepath)
        return locked


    @staticmethod
    def wait_for_files(filepath):
        """Checks if the files are ready.

        For a file to be ready it must exist and can be opened in append
        mode.
        """
        wait_time = 5

        # If the file doesn't exist, wait wait_time seconds and try again
        # until it's found.
        while not os.path.exists(filepath):
            print ("%s hasn't arrived. Waiting %s seconds." % \
                (filepath, wait_time))
            time.sleep(wait_time)
            # If the file exists but locked, wait wait_time seconds and check
            # again until it's no longer locked by another process.
        while OSHelper._is_locked(filepath):
            print( "%s is currently in use. Waiting %s seconds." % \
                      (filepath, wait_time))
            time.sleep(wait_time)

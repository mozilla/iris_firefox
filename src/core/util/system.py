# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


import logging
import os
import subprocess
from distutils.spawn import find_executable

import pytesseract

from src.core.api.os_helpers import OSHelper

logger = logging.getLogger(__name__)
restore_terminal_encoding = None


def check_7zip():
    """Checks if 7zip is installed."""
    sz_bin = find_executable('7z')
    if sz_bin is None:
        logger.critical('Cannot find required library 7zip, aborting Iris.')
        logger.critical('Please consult wiki for complete setup instructions.')
        return False
    return True


def init_tesseract_path():
    """Initialize Tesseract path."""

    which_tesseract = subprocess.Popen('which tesseract', stdout=subprocess.PIPE, shell=True).communicate()[
        0].rstrip().decode("utf-8")
    path_not_found = False

    if OSHelper.is_windows():
        win_default_tesseract_path = 'C:\\Program Files (x86)\\Tesseract-OCR'

        if '/c/' in str(which_tesseract):
            win_which_tesseract_path = which_tesseract.replace('/c/', 'C:\\').replace('/', '\\') + '.exe'
        else:
            win_which_tesseract_path = which_tesseract.replace('\\', '\\\\')

        if _check_path(win_default_tesseract_path):
            pytesseract.pytesseract.tesseract_cmd = win_default_tesseract_path + '\\tesseract'
        elif _check_path(win_which_tesseract_path):
            pytesseract.pytesseract.tesseract_cmd = win_which_tesseract_path
        else:
            path_not_found = True

    elif OSHelper.is_linux() or OSHelper.is_mac():
        if _check_path(which_tesseract):
            pytesseract.pytesseract.tesseract_cmd = which_tesseract
        else:
            path_not_found = True
    else:
        path_not_found = True

    if path_not_found:
        logger.critical('Unable to find Tesseract.')
        logger.critical('Please consult wiki for complete setup instructions.')
        return False
    return True


def _check_path(dir_path):
    """Check if a path exists."""
    if not isinstance(dir_path, str):
        return False
    if not os.path.exists(dir_path):
        return False
    return True


def shutdown_process(process_name: str):
    """Checks if the process name exists in the process list and close it ."""

    if OSHelper.is_windows():
        command_str = 'taskkill /IM ' + process_name + '.exe'
        try:
            subprocess.Popen(command_str, shell=True, stdout=subprocess.PIPE)
        except subprocess.CalledProcessError:
            logger.error('Command  failed: "%s"' % command_str)
            raise Exception('Unable to run Command.')
    elif OSHelper.is_mac() or OSHelper.is_linux():
        command_str = 'pkill ' + process_name
        try:
            subprocess.Popen(command_str, shell=True, stdout=subprocess.PIPE)
        except subprocess.CalledProcessError:
            logger.error('Command  failed: "%s"' % command_str)
            raise Exception('Unable to run Command.')


def fix_terminal_encoding():
    """Helper function to set terminal to platform-specific UTF encoding."""
    global restore_terminal_encoding
    restore_terminal_encoding = get_terminal_encoding()
    if restore_terminal_encoding is None:
        return
    if os.path.exists('C:\\'):
        platform_utf_encoding = '65001'
    else:
        platform_utf_encoding = None
    if restore_terminal_encoding != platform_utf_encoding:
        set_terminal_encoding(platform_utf_encoding)


def reset_terminal_encoding():
    global restore_terminal_encoding
    if restore_terminal_encoding is not None:
        set_terminal_encoding(restore_terminal_encoding)


def get_terminal_encoding():
    """Helper function to get current terminal encoding."""
    if OSHelper.is_windows():
        logger.debug('Running "chcp" shell command')
        chcp_output = os.popen('chcp').read().strip()
        logger.debug('chcp output: "%s"' % chcp_output)
        if chcp_output.startswith('Active code page:'):
            codepage = chcp_output.split(': ')[1]
            logger.debug('Active codepage is "%s"' % codepage)
            return codepage
        else:
            logger.warning('There was an error detecting the active codepage')
            return None
    else:
        logger.debug('Platform does not require switching terminal encoding')
        return None


def set_terminal_encoding(encoding):
    """Helper function to set terminal encoding."""
    if os.path.exists('C:\\'):
        logger.debug('Running "chcp" shell command, setting codepage to "%s"', encoding)
        chcp_output = os.popen('chcp %s' % encoding).read().strip()
        logger.debug('chcp output: "%s"' % chcp_output)
        if chcp_output == 'Active code page: %s' % encoding:
            logger.debug('Successfully set codepage to "%s"' % encoding)
        else:
            logger.warning('Can\'t set codepage for terminal')


def get_python_version():
    version = ''
    try:
        py_version = 'python3 --version'
        version_string = subprocess.Popen(py_version, stdout=subprocess.PIPE, shell=True).communicate()[
            0].rstrip().decode("utf-8")
        version = version_string.split(' ')[1]
    except IndexError:
        py_version = 'python --version'
        version_string = subprocess.Popen(py_version, stdout=subprocess.PIPE, shell=True).communicate()[
            0].rstrip().decode("utf-8")
    return version

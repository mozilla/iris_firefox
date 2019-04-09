# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import logging
import time

from iris.api.core.errors import APIHelperError
from iris.api.core.mouse import click
from iris.api.core.region import exists, Pattern
from iris.api.core.util.core_helper import INVALID_GENERIC_INPUT
from iris.api.helpers.general import open_directory
from iris.api.core.settings import Settings
from iris.api.core.key import KeyModifier, type
from iris.api.core.platform import Platform

logger = logging.getLogger(__name__)


def select_file_in_folder(directory, filename_pattern, file_option, max_num_of_attempts=3):
    """
    Opens directory, selects file in opened directory, and provides action with it (e.g. copy, cut, delete),
    and closes opened directory.

    :param directory: Folder on hard drive to open.
    :param filename_pattern: File Pattern to select.
    :param file_option: File processing function. Appropriate methods are: edit_copy, edit_cut, edit_delete.
    :param max_num_of_attempts: Attempts to find pattern of file name. Default: 3
    """

    finder_list_view = '2'
    type_delay = 0.5

    if not isinstance(directory, str):
        raise ValueError(INVALID_GENERIC_INPUT)

    if not isinstance(filename_pattern, Pattern):
        raise ValueError(INVALID_GENERIC_INPUT)

    if not callable(file_option):
        raise ValueError(INVALID_GENERIC_INPUT)

    open_directory(directory)

    try:
        for attempt in range(1, max_num_of_attempts+1):
            file_located = exists(filename_pattern)

            if file_located:
                logger.debug('File {} in directory {} is available.'.format(filename_pattern, directory))
                break
            else:
                if attempt == max_num_of_attempts:
                    logger.debug('File {} is not available after {} attempt(s).'.format(filename_pattern, attempt))
                    raise Exception

                time.sleep(Settings.DEFAULT_UI_DELAY_LONG)
                if Settings.get_os() == Platform.MAC:
                    type(finder_list_view, KeyModifier.CMD, type_delay)

        click(filename_pattern)

        file_option()

    except Exception:
        raise APIHelperError('Could not find file {} in folder {}.'.format(filename_pattern, directory))
    finally:
        if Settings.is_windows():
            type('w', KeyModifier.CTRL)
        elif Settings.is_linux():
            type('q', KeyModifier.CTRL)
        elif Settings.is_mac():
            type('w', KeyModifier.CMD + KeyModifier.ALT)

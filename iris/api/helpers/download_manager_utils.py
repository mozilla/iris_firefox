# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import getpass

from iris.api.core.errors import FindError, APIHelperError
from iris.api.core.mouse import click
from iris.api.core.region import wait, exists, Pattern, logger, os, Settings, Platform
from iris.api.helpers.keyboard_shortcuts import scroll_down


class DownloadFiles(object):
    EXTRA_SMALL_FILE_5MB = Pattern('5MB.png')
    SMALL_FILE_10MB = Pattern('10MB.png').similar(0.95)
    SMALL_FILE_20MB = Pattern('20MB.png').similar(0.95)
    MEDIUM_FILE_50MB = Pattern('50MB.png')
    MEDIUM_FILE_100MB = Pattern('100MB.png')
    VERY_LARGE_FILE_1GB = Pattern('1GB.png')
    DOWNLOAD_NAME_1GB = Pattern('download_name_1GB.png')
    LIBRARY_DOWNLOADS_5MB = Pattern('5MB_library_downloads.png')
    LIBRARY_DOWNLOADS_10MB = Pattern('10MB_library_downloads.png')
    LIBRARY_DOWNLOADS_20MB = Pattern('20MB_library_downloads.png')
    LIBRARY_DOWNLOADS_50MB = Pattern('50MB_library_downloads.png')
    LIBRARY_DOWNLOADS_100MB = Pattern('100MB_library_downloads.png')
    DOWNLOADS_PANEL_5MB_COMPLETED = Pattern('5MB_completed_downloadsPanel.png')
    FOLDER_VIEW_5MB_HIGHLIGHTED = Pattern('5MB_folder_view_highlighted.png')
    ABOUT = Pattern('about.png')
    SAVE_FILE = Pattern('save_file.png')
    DOWNLOAD_CANCELED = Pattern('download_canceled.png')
    OK = Pattern('ok.png')


def download_file(file_to_download, accept_download):
    """
    :param file_to_download: File to be downloaded.
    :param accept_download: Accept download pattern.
    :return: None.
    """
    file_found = exists(file_to_download, 2)
    if file_found:
        click(file_to_download)
    else:
        while not file_found:
            scroll_down()
            try:
                click(file_to_download)
                file_found = True
            except FindError:
                file_found = False
            if exists(DownloadFiles.ABOUT, 1):
                raise APIHelperError('File to be downloaded not found.')

    try:
        wait(DownloadFiles.SAVE_FILE, 5)
        logger.debug('The \'Save file\' option is present in the page.')
        click(DownloadFiles.SAVE_FILE)
    except FindError:
        raise APIHelperError('The \'Save file\' option is not present in the page, aborting.')

    try:
        wait(accept_download, 5)
        logger.debug('The OK button found in the page.')
        click(accept_download)
    except FindError:
        raise APIHelperError('The OK button is not found in the page.')


def downloads_cleanup(filename):
    username = getpass.getuser()

    if Settings.get_os() == Platform.MAC:
        os.chdir('/Users/' + username + '/Downloads')
    elif Settings.get_os() == Platform.LINUX:
        os.chdir('/home/' + username + '/Downloads')
    else:
        if Settings.get_os() == Platform.WINDOWS:
            os.chdir('C:\\Users\\' + username + '\\Downloads')

    exist_file = os.path.isfile('%s/%s' % (os.getcwd(), filename))
    if exist_file:
        os.remove(filename)
        logger.debug('Removing the ' + filename + ' file.')
    else:
        raise APIHelperError(('The ' + filename + ' file does not exist.'))

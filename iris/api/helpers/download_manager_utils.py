# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import logging
import shutil

from iris.api.core.errors import FindError, APIHelperError
from iris.api.core.firefox_ui.download_manager import DownloadManager
from iris.api.core.firefox_ui.library import Library
from iris.api.core.firefox_ui.library_menu import LibraryMenu
from iris.api.core.firefox_ui.nav_bar import NavBar
from iris.api.core.mouse import click, scroll
from iris.api.core.region import wait, exists, Pattern
from iris.api.core.util.core_helper import IrisCore
from iris.api.helpers.keyboard_shortcuts import scroll_down, page_down
from iris.api.helpers.test_utils import access_and_check_pattern

logger = logging.getLogger(__name__)


class DownloadFiles(object):
    EXTRA_SMALL_FILE_5MB = Pattern('5MB.png')
    SMALL_FILE_10MB = Pattern('10MB.png').similar(0.95)
    SMALL_FILE_20MB = Pattern('20MB.png').similar(0.95)
    MEDIUM_FILE_50MB = Pattern('50MB.png')
    MEDIUM_FILE_100MB = Pattern('100MB.png')
    LARGE_FILE_200MB = Pattern('200MB.png')
    EXTRA_LARGE_FILE_512MB = Pattern('512MB.png')
    VERY_LARGE_FILE_1GB = Pattern('1GB.png')
    DOWNLOAD_FILE_NAME_1GB = Pattern('download_name_1GB.png')
    DOWNLOAD_FILE_NAME_512MB = Pattern('download_name_512MB.png')
    DOWNLOAD_FILE_NAME_20MB = Pattern('download_name_20MB.png')
    DOWNLOAD_FILE_NAME_10MB = Pattern('download_name_10MB.png')
    DOWNLOAD_FILE_NAME_5MB = Pattern('download_name_5MB.png')
    LIBRARY_DOWNLOADS_5MB = Pattern('5MB_library_downloads.png')
    LIBRARY_DOWNLOADS_10MB = Pattern('10MB_library_downloads.png')
    LIBRARY_DOWNLOADS_20MB = Pattern('20MB_library_downloads.png')
    LIBRARY_DOWNLOADS_50MB = Pattern('50MB_library_downloads.png')
    LIBRARY_DOWNLOADS_100MB = Pattern('100MB_library_downloads.png')
    LIBRARY_DOWNLOADS_200MB = Pattern('200MB_library_downloads.png')
    LIBRARY_DOWNLOADS_512MB = Pattern('512MB_library_downloads.png')
    TOTAL_DOWNLOAD_SIZE_1GB = Pattern('download_size_of_1GB.png')
    TOTAL_DOWNLOAD_SIZE_512MB = Pattern('download_size_of_512MB.png')
    TOTAL_DOWNLOAD_SIZE_200MB = Pattern('download_size_of_200MB.png')
    TOTAL_DOWNLOAD_SIZE_100MB = Pattern('download_size_of_100MB.png')
    TOTAL_DOWNLOAD_SIZE_50MB = Pattern('download_size_of_50MB.png')
    TOTAL_DOWNLOAD_SIZE_20MB = Pattern('download_size_of_20MB.png')
    DOWNLOADS_PANEL_5MB_COMPLETED = Pattern('5MB_completed_downloadsPanel.png')
    FOLDER_VIEW_5MB_HIGHLIGHTED = Pattern('5MB_folder_view_highlighted.png')

    ABOUT = Pattern('about.png')
    SAVE_FILE = Pattern('save_file.png')
    DOWNLOAD_CANCELED = Pattern('download_canceled.png')
    OK = Pattern('ok.png')
    CANCEL_ALL_DOWNLOADS_POP_UP = Pattern('cancel_all_downloads.png')


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
            scroll_down(5)
            try:
                click(file_to_download)
                file_found = True
            except FindError:
                file_found = False
            if exists(DownloadFiles.ABOUT, 2):
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


def downloads_cleanup():
    path = IrisCore.get_downloads_dir()
    shutil.rmtree(path)


def open_show_downloads_window_using_download_panel():
    return [
        access_and_check_pattern(NavBar.DOWNLOADS_BUTTON, '\"Downloads panel\"', DownloadManager.SHOW_ALL_DOWNLOADS,
                                 'click'),
        access_and_check_pattern(DownloadManager.SHOW_ALL_DOWNLOADS, '\"Show all downloads\"',
                                 Library.DOWNLOADS, 'click'),
        access_and_check_pattern(Library.DOWNLOADS, '\"Downloads library\"')]


def open_clear_recent_history_window_from_library_menu():
    return [
        access_and_check_pattern(NavBar.LIBRARY_MENU, '\"Library menu\"', LibraryMenu.DOWNLOADS, 'click'),
        access_and_check_pattern(LibraryMenu.DOWNLOADS, '\"Downloads menu\"',
                                 DownloadManager.Downloads.SHOW_ALL_DOWNLOADS, 'click'),
        access_and_check_pattern(DownloadManager.Downloads.SHOW_ALL_DOWNLOADS, '\"Downloads library\"',
                                 Library.DOWNLOADS, 'click')]


def show_all_downloads_from_library_menu_private_window():
    return [
        access_and_check_pattern(NavBar.LIBRARY_MENU, '\"Library menu\"', LibraryMenu.DOWNLOADS, 'click'),
        access_and_check_pattern(LibraryMenu.DOWNLOADS, '\"Downloads menu\"',
                                 DownloadManager.Downloads.SHOW_ALL_DOWNLOADS, 'click'),
        access_and_check_pattern(DownloadManager.Downloads.SHOW_ALL_DOWNLOADS, '\"Downloads library\"',
                                 DownloadManager.AboutDownloads.ABOUT_DOWNLOADS, 'click')]

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
from iris.api.core.key import *
from iris.api.core.mouse import click
from iris.api.core.region import wait, exists, Pattern, Region, find, SCREEN_HEIGHT, SCREEN_WIDTH
from iris.api.core.util.core_helper import IrisCore
from iris.api.helpers.general import click_window_control, close_tab
from iris.api.helpers.keyboard_shortcuts import scroll_down, open_web_console
from iris.api.helpers.test_utils import access_and_check_pattern, Step

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
    DOWNLOAD_TYPE_ICON = Pattern('download_Type_Icon.png').similar(0.7)
    DOWNLOAD_TYPE_ICON_ZIP = Pattern('download_type_zip_icon.png')
    DOWNLOAD_FILE_NAME_1GB = Pattern('download_name_1GB.png')
    DOWNLOAD_FILE_NAME_512MB = Pattern('download_name_512MB.png')
    DOWNLOAD_FILE_NAME_20MB = Pattern('download_name_20MB.png')
    DOWNLOAD_FILE_NAME_10MB = Pattern('download_name_10MB.png')
    DOWNLOAD_FILE_NAME_5MB = Pattern('download_name_5MB.png')
    LIBRARY_DOWNLOADS_5MB = Pattern('5MB_library_downloads.png')
    LIBRARY_DOWNLOADS_5MB_HIGHLIGHTED = Pattern('5MB_library_downloads_highlighted.png')
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
    DOWNLOADS_PANEL_5MB_COMPLETED = Pattern('completed_5mb_file.png')
    DOWNLOADS_PANEL_5MB_MISSING = Pattern('moved_missing_5mb_file.png')
    DOWNLOADS_PANEL_10MB_COMPLETED = Pattern('completed_10mb_file.png')
    DOWNLOADS_PANEL_10MB_MISSING = Pattern('moved_missing_10mb_file.png')
    DOWNLOADS_PANEL_20MB_MISSING = Pattern('moved_missing_20mb_file.png')
    DOWNLOADS_PANEL_FREETDS_PATCHED = Pattern('completed_freetds_patched.png')
    DOWNLOADS_PANEL_5MB_COMPLETED_RTL = Pattern('completed_5mb_file_rtl.png')
    DOWNLOADS_PANEL_10MB_COMPLETED_RTL = Pattern('completed_10mb_file_rtl.png')
    DOWNLOADS_PANEL_20MB_COMPLETED_RTL = Pattern('completed_20mb_file_rtl.png')
    FOLDER_VIEW_5MB_HIGHLIGHTED = Pattern('5MB_folder_view_highlighted.png').similar(0.79)
    FOLDER_VIEW_10MB_HIGHLIGHTED = Pattern('10MB_folder_view_highlighted.png').similar(0.79)
    FIREFOX_INSTALLER = Pattern('firefox_installer.png')
    FIREFOX_INSTALLER_HIGHLIGHTED = Pattern('firefox_installer_highlighted.png')
    STATUS_200 = Pattern('status_200.png')

    ABOUT = Pattern('about.png')
    SAVE_FILE = Pattern('save_file.png')
    DOWNLOAD_CANCELED = Pattern('download_canceled.png')
    OK = Pattern('ok.png')
    CANCEL_ALL_DOWNLOADS_POP_UP = Pattern('cancel_all_downloads.png')

    # Safe Browsing Testing patterns.
    MALICIOUS = Pattern('malicious.png')
    MALICIOUS_HTTPS = Pattern('malicious_https.png')
    DANGEROUS_HOST_WARNING = Pattern('dangerous_host_warning.png')
    UNCOMMON = Pattern('uncommon.png')
    UNCOMMON_HTTPS = Pattern('uncommon_https.png')
    POTENTIALLY_UNWANTED = Pattern('potentially_unwanted.png')
    DOWNLOADS_PANEL_CONTENT_COMPLETED = Pattern('completed_content.png').similar(0.7)
    DOWNLOADS_PANEL_CONTENT1_COMPLETED = Pattern('completed_content1.png').similar(0.6)
    DOWNLOADS_PANEL_BADREP_COMPLETED = Pattern('completed_badrep.png').similar(0.7)
    DOWNLOADS_PANEL_PUA_COMPLETED = Pattern('completed_pua.png').similar(0.7)
    DOWNLOADS_PANEL_UNKNOWN_COMPLETED = Pattern('completed_unknown.png').similar(0.7)
    DOWNLOADS_PANEL_UNKNOWN1_COMPLETED = Pattern('completed_unknown1.png').similar(0.7)
    LIBRARY_DOWNLOADS_CONTENT = Pattern('content_library_downloads.png').similar(0.7)
    LIBRARY_DOWNLOADS_CONTENT_RED = Pattern('content_library_downloads_red.png').similar(0.7)
    LIBRARY_DOWNLOADS_CONTENT1 = Pattern('content1_library_downloads.png').similar(0.7)
    LIBRARY_DOWNLOADS_CONTENT1_RED = Pattern('content1_library_downloads_red.png').similar(0.7)
    LIBRARY_DOWNLOADS_BADREP = Pattern('badrep_library_downloads.png').similar(0.7)
    LIBRARY_DOWNLOADS_BADREP_RED = Pattern('badrep_library_downloads_red.png').similar(0.7)


def cancel_and_clear_downloads(private_window=False):
    logger.info('>>>Downloads Cleanup steps<<<')
    for step in cancel_in_progress_downloads_from_the_library(private_window):
        logger.info('Step %s - passed? %s' % (step.message, step.resolution))


def cancel_in_progress_downloads_from_the_library(private_window=False):
    # Open the 'Show Downloads' window and cancel all 'in progress' downloads.
    global cancel_downloads
    if private_window:
        steps = show_all_downloads_from_library_menu_private_window()
        logger.debug('Creating a region for Private Library window.')
        try:
            find_back_button = find(NavBar.BACK_BUTTON)
        except FindError:
            raise FindError('Could not get the coordinates of the nav bar back button.')

        try:
            find_hamburger_menu = find(NavBar.HAMBURGER_MENU)
        except FindError:
            raise FindError('Could not get the coordinates of the hamburger menu.')

        region = Region(find_back_button.x - 10, find_back_button.y,
                        SCREEN_WIDTH, SCREEN_HEIGHT)
    else:
        steps = open_show_all_downloads_window_from_library_menu()
        logger.debug('Creating a region for Non-private Library window.')
        try:
            find_library = find(Library.TITLE)
        except FindError:
            raise FindError('Could not get the x-coordinate of the library window title.')

        try:
            find_clear_downloads = find(Library.DownloadLibrary.CLEAR_DOWNLOADS)
        except FindError:
            raise FindError('Could not get the x-coordinate of the clear_downloads button.')

        clear_downloads_width, clear_downloads_height = Library.DownloadLibrary.CLEAR_DOWNLOADS.get_size()
        region = Region(find_library.x - 10, find_library.y,
                        (find_clear_downloads.x + clear_downloads_width + 20) - find_library.x, 500)

    # Cancel all 'in progress' downloads.
    expected = region.exists(DownloadManager.DownloadsPanel.DOWNLOAD_CANCEL, 5)
    expected_highlighted = region.exists(Library.DownloadLibrary.DOWNLOAD_CANCEL_HIGHLIGHTED)
    if expected or expected_highlighted:
        steps.append(Step(expected, 'The Cancel Download button is displayed properly.'))
        cancel_downloads = True
        expected_cancel = True
    else:
        steps.append(Step(True, 'There are no downloads to be cancelled.'))
        cancel_downloads = False

    cancel_pattern = DownloadManager.DownloadsPanel.DOWNLOAD_CANCEL if expected else Library.DownloadLibrary.DOWNLOAD_CANCEL_HIGHLIGHTED

    if cancel_downloads:
        while expected_cancel:
            expected_cancel = region.exists(cancel_pattern, 10)
            if expected_cancel:
                click(cancel_pattern)
        steps.append(Step(True, 'All downloads were cancelled.'))

    if private_window:
        close_tab()
    else:
        click_window_control('close')

    return steps


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
        wait(DownloadFiles.SAVE_FILE, 90)
        logger.debug('The \'Save file\' option is present in the page.')
        click(DownloadFiles.SAVE_FILE)
    except FindError:
        raise APIHelperError('The \'Save file\' option is not present in the page, aborting.')

    try:
        ok_button = exists(accept_download, 5)
        if ok_button:
            logger.debug('The OK button found in the page.')
            click(accept_download)
    except FindError:
        raise APIHelperError('The OK button is not found in the page.')


def downloads_cleanup():
    path = IrisCore.get_downloads_dir()
    shutil.rmtree(path, ignore_errors=True)


def force_delete_folder(path):
    shutil.rmtree(path, ignore_errors=True)


def open_show_all_downloads_window_from_library_menu():
    return [
        access_and_check_pattern(NavBar.LIBRARY_MENU, '\"Library menu\"', LibraryMenu.DOWNLOADS, 'click'),
        access_and_check_pattern(LibraryMenu.DOWNLOADS, '\"Downloads menu\"',
                                 DownloadManager.Downloads.SHOW_ALL_DOWNLOADS, 'click'),
        access_and_check_pattern(DownloadManager.Downloads.SHOW_ALL_DOWNLOADS, '\"Downloads library\"',
                                 Library.DownloadLibrary.DOWNLOADS, 'click')]


def open_show_downloads_window_using_download_panel():
    return [
        access_and_check_pattern(NavBar.DOWNLOADS_BUTTON, '\"Downloads panel\"', DownloadManager.SHOW_ALL_DOWNLOADS,
                                 'click'),
        access_and_check_pattern(DownloadManager.SHOW_ALL_DOWNLOADS, '\"Show all downloads\"',
                                 Library.DownloadLibrary.DOWNLOADS, 'click'),
        access_and_check_pattern(Library.DownloadLibrary.DOWNLOADS, '\"Downloads library\"')]


def select_throttling(option):
    open_web_console()

    try:
        wait(Pattern('network.png'), 10)
        click(Pattern('network.png'))
    except FindError:
        raise APIHelperError('Can\'t find the network menu in the page, aborting test.')

    try:
        wait(Pattern('no_throttling.png'), 10)
        click(Pattern('no_throttling.png'))
    except FindError:
        raise APIHelperError('Can\'t find the throttling menu in the page, aborting test.')

    for i in range(option + 1):
        type(Key.DOWN)
    type(Key.ENTER)


def show_all_downloads_from_library_menu_private_window():
    return [
        access_and_check_pattern(NavBar.LIBRARY_MENU, '\"Library menu\"', LibraryMenu.DOWNLOADS, 'click'),
        access_and_check_pattern(LibraryMenu.DOWNLOADS, '\"Downloads menu\"',
                                 DownloadManager.Downloads.SHOW_ALL_DOWNLOADS, 'click'),
        access_and_check_pattern(DownloadManager.Downloads.SHOW_ALL_DOWNLOADS, '\"Downloads library\"',
                                 DownloadManager.AboutDownloads.ABOUT_DOWNLOADS, 'click')]


class NetworkOption(object):
    """Class with throttling options."""

    NO_THROTTLING = 0
    GPRS = 1
    REGULAR_2G = 2
    GOOD_2G = 3
    REGULAR_3G = 4
    GOOD_3G = 5
    REGULAR_4G = 6
    DSL = 7
    WIFI = 8

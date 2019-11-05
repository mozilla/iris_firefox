# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import logging
import shutil

from moziris.api.errors import FindError, APIHelperError
from moziris.api.finder.finder import find, exists, wait
from moziris.api.finder.pattern import Pattern
from moziris.api.keyboard.keyboard import *
from moziris.api.mouse.mouse import click, scroll_down, hover
from moziris.api.screen.region import Region
from moziris.api.screen.screen import Screen
from moziris.util.path_manager import PathManager
from targets.nightly.firefox_ui.download_manager import DownloadManager
from targets.nightly.firefox_ui.general_test_utils import Step, access_and_check_pattern
from targets.nightly.firefox_ui.helpers.general import click_window_control
from targets.nightly.firefox_ui.helpers.keyboard_shortcuts import (
    close_tab,
    open_web_console,
)
from targets.nightly.firefox_ui.library import Library
from targets.nightly.firefox_ui.library_menu import LibraryMenu
from targets.nightly.firefox_ui.nav_bar import NavBar
from targets.nightly.settings import FirefoxSettings

logger = logging.getLogger(__name__)


class DownloadFiles(object):
    EXTRA_SMALL_FILE_5MB = Pattern("5MB.png")
    SMALL_FILE_10MB = Pattern("10MB.png").similar(0.85)
    SMALL_FILE_20MB = Pattern("20MB.png").similar(0.9)
    MEDIUM_FILE_50MB = Pattern("50MB.png")
    MEDIUM_FILE_100MB = Pattern("100MB.png")
    LARGE_FILE_200MB = Pattern("200MB.png")
    EXTRA_LARGE_FILE_512MB = Pattern("512MB.png")
    VERY_LARGE_FILE_1GB = Pattern("1GB.png")
    DOWNLOAD_TYPE_ICON = Pattern("download_Type_Icon.png").similar(0.7)
    DOWNLOAD_TYPE_ICON_ZIP = Pattern("download_type_zip_icon.png")
    DOWNLOAD_FILE_NAME_1GB = Pattern("download_name_1GB.png")
    DOWNLOAD_FILE_NAME_512MB = Pattern("download_name_512MB.png")
    DOWNLOAD_FILE_NAME_20MB = Pattern("download_name_20MB.png")
    DOWNLOAD_FILE_NAME_10MB = Pattern("download_name_10MB.png")
    DOWNLOAD_FILE_NAME_5MB = Pattern("download_name_5MB.png")
    LIBRARY_DOWNLOADS_5MB = Pattern("5MB_library_downloads.png")
    LIBRARY_DOWNLOADS_5MB_HIGHLIGHTED = Pattern("5MB_library_downloads_highlighted.png")
    LIBRARY_DOWNLOADS_10MB = Pattern("10MB_library_downloads.png")
    LIBRARY_DOWNLOADS_20MB = Pattern("20MB_library_downloads.png")
    LIBRARY_DOWNLOADS_50MB = Pattern("50MB_library_downloads.png")
    LIBRARY_DOWNLOADS_100MB = Pattern("100MB_library_downloads.png")
    LIBRARY_DOWNLOADS_200MB = Pattern("200MB_library_downloads.png")
    LIBRARY_DOWNLOADS_512MB = Pattern("512MB_library_downloads.png")
    TOTAL_DOWNLOAD_SIZE_1GB = Pattern("download_size_of_1GB.png")
    TOTAL_DOWNLOAD_SIZE_512MB = Pattern("download_size_of_512MB.png")
    TOTAL_DOWNLOAD_SIZE_200MB = Pattern("download_size_of_200MB.png")
    TOTAL_DOWNLOAD_SIZE_100MB = Pattern("download_size_of_100MB.png")
    TOTAL_DOWNLOAD_SIZE_50MB = Pattern("download_size_of_50MB.png")
    TOTAL_DOWNLOAD_SIZE_20MB = Pattern("download_size_of_20MB.png")
    DOWNLOADS_PANEL_5MB_COMPLETED = Pattern("completed_5mb_file.png")
    DOWNLOADS_PANEL_5MB_MISSING = Pattern("moved_missing_5mb_file.png")
    DOWNLOADS_PANEL_10MB_COMPLETED = Pattern("completed_10mb_file.png")
    DOWNLOADS_PANEL_10MB_MISSING = Pattern("moved_missing_10mb_file.png")
    DOWNLOADS_PANEL_20MB_MISSING = Pattern("moved_missing_20mb_file.png")
    DOWNLOADS_PANEL_FREETDS_PATCHED = Pattern("completed_freetds_patched.png")
    DOWNLOADS_PANEL_5MB_COMPLETED_RTL = Pattern("completed_5mb_file_rtl.png")
    DOWNLOADS_PANEL_10MB_COMPLETED_RTL = Pattern("completed_10mb_file_rtl.png")
    DOWNLOADS_PANEL_20MB_COMPLETED_RTL = Pattern("completed_20mb_file_rtl.png")
    FOLDER_VIEW_5MB_HIGHLIGHTED = Pattern("5MB_folder_view_highlighted.png").similar(
        0.79
    )
    FOLDER_VIEW_10MB_HIGHLIGHTED = Pattern("10MB_folder_view_highlighted.png").similar(
        0.79
    )
    FIREFOX_INSTALLER = Pattern("firefox_installer.png")
    FIREFOX_INSTALLER_HIGHLIGHTED = Pattern("firefox_installer_highlighted.png")
    STATUS_200 = Pattern("status_200.png")

    ABOUT = Pattern("about.png")
    SAVE_FILE = Pattern("save_file.png")
    DOWNLOAD_CANCELLED = Pattern("download_cancelled.png")
    OK = Pattern("ok.png").similar(0.6)
    CANCEL_ALL_DOWNLOADS_POP_UP = Pattern("cancel_all_downloads.png")

    # Safe Browsing Testing patterns.
    MALICIOUS = Pattern("malicious.png")
    MALICIOUS_HTTPS = Pattern("malicious_https.png")
    DANGEROUS_HOST_WARNING = Pattern("dangerous_host_warning.png")
    UNCOMMON = Pattern("uncommon.png")
    UNCOMMON_HTTPS = Pattern("uncommon_https.png")
    POTENTIALLY_UNWANTED = Pattern("potentially_unwanted.png")
    DOWNLOADS_PANEL_CONTENT_COMPLETED = Pattern("completed_content.png")
    DOWNLOADS_PANEL_CONTENT1_COMPLETED = Pattern("completed_content1.png")
    DOWNLOADS_PANEL_BADREP_COMPLETED = Pattern("completed_badrep.png")
    DOWNLOADS_PANEL_PUA_COMPLETED = Pattern("completed_pua.png")
    DOWNLOADS_PANEL_UNKNOWN_COMPLETED = Pattern("completed_unknown.png")
    DOWNLOADS_PANEL_UNKNOWN1_COMPLETED = Pattern("completed_unknown1.png")
    LIBRARY_DOWNLOADS_CONTENT = Pattern("content_library_downloads.png")
    LIBRARY_DOWNLOADS_CONTENT_RED = Pattern("content_library_downloads_red.png")
    LIBRARY_DOWNLOADS_CONTENT1 = Pattern("content1_library_downloads.png")
    LIBRARY_DOWNLOADS_CONTENT1_RED = Pattern("content1_library_downloads_red.png")
    LIBRARY_DOWNLOADS_BADREP = Pattern("badrep_library_downloads.png")
    LIBRARY_DOWNLOADS_BADREP_RED = Pattern("badrep_library_downloads_red.png")


def cancel_and_clear_downloads(private_window=False):
    logger.info(">>>Downloads Cleanup steps<<<")
    for step in cancel_in_progress_downloads_from_the_library(private_window):
        logger.info("Step %s - passed? %s" % (step.message, step.resolution))


def cancel_in_progress_downloads_from_the_library(private_window=False):
    # Open the 'Show Downloads' window and cancel all 'in progress' downloads.
    global cancel_downloads
    if private_window:
        steps = show_all_downloads_from_library_menu_private_window()
        logger.debug("Creating a region for Private Library window.")
        try:
            find_back_button = find(NavBar.BACK_BUTTON)
        except FindError:
            raise FindError("Could not get the coordinates of the nav bar back button.")

        region = Region(
            find_back_button.x - 10,
            find_back_button.y,
            Screen.SCREEN_WIDTH,
            Screen.SCREEN_HEIGHT,
        )
    else:
        steps = open_show_all_downloads_window_from_library_menu()
        logger.debug("Creating a region for Non-private Library window.")
        expected = exists(Library.TITLE, 10)
        assert expected is True, "Library successfully opened."

        try:
            find_library = find(Library.TITLE)
        except FindError:
            raise FindError(
                "Could not get the x-coordinate of the library window title."
            )

        try:
            find_clear_downloads = find(Library.CLEAR_DOWNLOADS)
        except FindError:
            raise FindError(
                "Could not get the x-coordinate of the clear_downloads button."
            )

        clear_downloads_width, clear_downloads_height = (
            Library.CLEAR_DOWNLOADS.get_size()
        )
        region = Region(
            find_library.x - 10,
            find_library.y,
            (find_clear_downloads.x + clear_downloads_width + 20) - find_library.x,
            500,
        )

    # Cancel all 'in progress' downloads.
    expected = region.exists(DownloadManager.DownloadsPanel.DOWNLOAD_CANCEL, 5)
    expected_highlighted = region.exists(
        DownloadManager.DownloadsPanel.DOWNLOAD_CANCEL_HIGHLIGHTED
    )
    if expected or expected_highlighted:
        steps.append(
            Step(expected, "The Cancel Download button is displayed properly.")
        )
        cancel_downloads = True
        expected_cancel = True
    else:
        steps.append(Step(True, "There are no downloads to be cancelled."))
        cancel_downloads = False

    cancel_pattern = (
        DownloadManager.DownloadsPanel.DOWNLOAD_CANCEL
        if expected
        else DownloadManager.DownloadsPanel.DOWNLOAD_CANCEL_HIGHLIGHTED
    )

    if cancel_downloads:
        while expected_cancel:
            expected_cancel = region.exists(cancel_pattern, 10)
            if expected_cancel:
                click(cancel_pattern)
                if not private_window:
                    hover(Library.TITLE)
        steps.append(Step(True, "All downloads were cancelled."))

    if private_window:
        close_tab()
    else:
        click_window_control("close")

    return steps


def download_file(
    file_to_download,
    accept_download,
    max_number_of_attempts=20,
    expect_accept_download_available=True,
):
    """
    :param file_to_download: Pattern of file to be downloaded.
    :param accept_download: Accept download pattern.
    :param max_number_of_attempts: Max number of attempts to locate file_to_download pattern.
    :param expect_accept_download_available: True if we expect accept_download button, False - if we don't;
            (in Windows 7 download UI don't have extra accept button in certain cases)
    :return: None.
    """
    for _ in range(max_number_of_attempts):
        file_found = exists(file_to_download, FirefoxSettings.FIREFOX_TIMEOUT)

        if file_found:
            click(file_to_download)
            break

        type(Key.PAGE_DOWN)

        if exists(DownloadFiles.ABOUT, FirefoxSettings.FIREFOX_TIMEOUT):
            raise APIHelperError("File to be downloaded not found.")

    try:
        wait(DownloadFiles.SAVE_FILE, FirefoxSettings.HEAVY_SITE_LOAD_TIMEOUT)
        logger.debug("The 'Save file' option is present in the page.")

        time.sleep(
            FirefoxSettings.TINY_FIREFOX_TIMEOUT
        )  # prevent click on inactive button on windows

        click(DownloadFiles.SAVE_FILE)

    except FindError:
        raise APIHelperError(
            "The 'Save file' option is not present in the page, aborting."
        )

    if expect_accept_download_available:
        accept_download_button = exists(
            accept_download, FirefoxSettings.FIREFOX_TIMEOUT
        )
        if accept_download_button:
            logger.debug("The accept download button found in the page.")
            click(accept_download)
        else:
            raise APIHelperError(
                "The accept download button was not found in the page."
            )


def downloads_cleanup():
    path = PathManager.get_downloads_dir()
    logger.debug('Clean the downloads folder: "%s"' % path)
    PathManager.remove_dir_contents(path)


def force_delete_folder(path):
    shutil.rmtree(path, ignore_errors=True)


def open_show_all_downloads_window_from_library_menu():
    return [
        access_and_check_pattern(
            NavBar.LIBRARY_MENU, '"Library menu"', LibraryMenu.DOWNLOADS, "click"
        ),
        access_and_check_pattern(
            LibraryMenu.DOWNLOADS,
            '"Downloads menu"',
            DownloadManager.Downloads.SHOW_ALL_DOWNLOADS,
            "click",
        ),
        access_and_check_pattern(
            DownloadManager.Downloads.SHOW_ALL_DOWNLOADS,
            '"Downloads library"',
            Library.DOWNLOADS,
            "click",
        ),
    ]


def open_show_downloads_window_using_download_panel():
    return [
        access_and_check_pattern(
            NavBar.DOWNLOADS_BUTTON,
            '"Downloads panel"',
            DownloadManager.SHOW_ALL_DOWNLOADS,
            "click",
        ),
        access_and_check_pattern(
            DownloadManager.SHOW_ALL_DOWNLOADS,
            '"Show all downloads"',
            Library.DOWNLOADS,
            "click",
        ),
        access_and_check_pattern(Library.DOWNLOADS, '"Downloads library"'),
    ]


def select_throttling(option):
    open_web_console()

    try:
        wait(Pattern("network.png"), 10)
        click(Pattern("network.png"))
    except FindError:
        raise APIHelperError("Can't find the network menu in the page, aborting test.")

    try:
        wait(Pattern("no_throttling.png"), 10)
        click(Pattern("no_throttling.png"))
    except FindError:
        raise APIHelperError(
            "Can't find the throttling menu in the page, aborting test."
        )

    for i in range(option + 1):
        type(Key.DOWN)
    type(Key.ENTER)


def show_all_downloads_from_library_menu_private_window():
    return [
        access_and_check_pattern(
            NavBar.LIBRARY_MENU, '"Library menu"', LibraryMenu.DOWNLOADS, "click"
        ),
        access_and_check_pattern(
            LibraryMenu.DOWNLOADS,
            '"Downloads menu"',
            DownloadManager.SHOW_ALL_DOWNLOADS,
            "click",
        ),
        access_and_check_pattern(
            DownloadManager.SHOW_ALL_DOWNLOADS,
            '"Downloads library"',
            DownloadManager.AboutDownloads.ABOUT_DOWNLOADS,
            "click",
        ),
    ]


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

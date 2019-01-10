# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from iris.api.core.pattern import Pattern


class DownloadManager(object):
    SHOW_ALL_DOWNLOADS = Pattern('downloadsHistory_show_all_Downloads.png')
    DOWNLOADS_FOLDER = Pattern('downloads_folder.png')

    class DownloadsPanel(object):
        DOWNLOADS_BUTTON = Pattern('downloads_button_open.png').similar(0.95)
        DOWNLOAD_RETRY = Pattern('downloadRetry.png')
        DOWNLOAD_RETRY_HIGHLIGHTED = Pattern('downloadRetry_highlighted.png').similar(0.95)
        DOWNLOAD_CANCEL = Pattern('downloadCancel.png').similar(0.95)
        DOWNLOAD_CANCEL_HIGHLIGHTED = Pattern('downloadCancel_highlighted.png').similar(0.95)
        NO_DOWNLOADS_FOR_THIS_SESSION = Pattern('emptyDownloads.png')
        OPEN_DOWNLOAD_FOLDER = Pattern('download_button_open_containing_folder.png')
        OPEN_CONTAINING_FOLDER = Pattern('open_containing_folder.png')
        TIME_LEFT = Pattern('time_left.png')
        BYTES_SECOND = Pattern('bytes_second.png')
        OF_1GB = Pattern('of_1gb.png')
        OPEN_DOWNLOAD_FOLDER = Pattern('download_button_open_containing_folder.png')

    # Downloaded files statuses
    class DownloadState(object):
        COMPLETED = Pattern('download_details_completed.png')
        CANCELED = Pattern('download_details_canceled.png')
        PROGRESS = Pattern('download_details_left_size.png')
        PAUSED = Pattern('download_details_paused.png')
        RETRY_DOWNLOAD = Pattern('download_details_retry_download.png')
        OPEN_FILE = Pattern('download_details_open_file.png')
        SPEED_PER_SECOND = Pattern('download_details_speed_per_second.png')
        MISSING_FILE = Pattern('download_details_file_moved_or_missing.png')

    # Library Menu Downloads Submenu.
    class Downloads(object):
        SHOW_DOWNLOADS_FOLDER = Pattern('appMenu-library-downloads-show-button_show_downloads_folder.png')
        PANEL_HEADER_DOWNLOADS = Pattern('panel_header_downloads.png')
        SHOW_ALL_DOWNLOADS = Pattern('library_menu_downloads_more.png')
        FILE_MOVED_OR_MISSING = Pattern('file_moved_or_missing.png')
        EXTRA_SMALL_FILE_5MB_ZIP = Pattern('5MB_zip.png')

    class AboutDownloads(object):
        NO_DOWNLOADS = Pattern('there_are_no_downloads.png')
        ABOUT_DOWNLOADS = Pattern('about_downloads.png')

    # Downloaded files options
    class DownloadsContextMenu(object):
        OPEN_CONTAINING_FOLDER = Pattern('downloads_open_containing_folder.png')
        CLEAR_PREVIEW_PANEL = Pattern('downloads_clear_preview_panel.png')
        COPY_DOWNLOAD_LINK = Pattern('downloads_copy_download_link.png')
        GO_TO_DOWNLOAD_PAGE = Pattern('downloads_go_to_download_page.png')
        REMOVE_FROM_HISTORY = Pattern('downloads_remove_from_history.png')
        PAUSE = Pattern('downloads_pause.png')
        RESUME = Pattern('downloads_resume.png')

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from iris.api.core.pattern import Pattern


class DownloadManager(object):
    SHOW_ALL_DOWNLOADS = Pattern('downloads_history_show_all_downloads.png')
    SHOW_ALL_DOWNLOADS_DARK_THEME = Pattern('downloads_history_show_all_downloads_dark_theme.png')
    DOWNLOADS_FOLDER = Pattern('downloads_folder.png')
    DOWNLOADS_FOLDER_PATH = Pattern('downloads_folder_path.png')
    NEW_DOWNLOADS_FOLDER = Pattern('new_downloads_folder_path.png')

    class DownloadsPanel(object):
        DOWNLOADS_BUTTON = Pattern('downloads_button_open.png').similar(0.95)
        DOWNLOAD_RETRY = Pattern('download_retry.png')
        DOWNLOAD_RETRY_HIGHLIGHTED = Pattern('download_retry_highlighted.png').similar(0.95)
        DOWNLOAD_CANCEL = Pattern('download_cancel.png')
        DOWNLOAD_CANCEL_HIGHLIGHTED = Pattern('download_cancel_highlighted.png').similar(0.95)
        NO_DOWNLOADS_FOR_THIS_SESSION = Pattern('empty_downloads.png')
        OPEN_DOWNLOAD_FOLDER = Pattern('download_button_open_containing_folder.png')
        OPEN_CONTAINING_FOLDER = Pattern('open_containing_folder.png')
        TIME_LEFT = Pattern('time_left.png')
        BYTES_SECOND = Pattern('bytes_second.png')
        OF_1GB = Pattern('of_1gb.png')
        ADD_REMOVE_DOWNLOADS_ARROW = Pattern('download_add_remove_file_arrow.png')
        ADD_REMOVE_DOWNLOADS_RED_ARROW = Pattern('download_add_remove_file_red_arrow.png')
        ADD_REMOVE_DOWNLOADS_WHITE_ARROW = Pattern('download_add_remove_file_white_arrow.png')
        BLOCKED_DOWNLOAD_ICON = Pattern('download_blocked_badge.png')
        UNWANTED_DOWNLOAD_ICON = Pattern('download_unwanted_badge.png')
        UNCOMMON_DOWNLOAD_ICON = Pattern('download_uncommon_badge.png')
        VIRUS_OR_MALWARE_DOWNLOAD = Pattern('virus_or_malware_message.png')
        VIRUS_OR_MALWARE_DOWNLOAD_DARK_THEME = Pattern('virus_or_malware_message_dark_theme.png')
        UNWANTED_DOWNLOAD = Pattern('unwanted_message.png')
        UNCOMMON_DOWNLOAD = Pattern('uncommon_message.png')

        class DownloadDetails(object):
            HEADER = Pattern('download_details_header.png')
            BLOCKED_DOWNLOAD_TITLE = Pattern('downloads_panel_blocked_subview_title.png')
            UNWANTED_DOWNLOAD_TITLE = Pattern('downloads_panel_unwanted_subview_title.png')
            UNCOMMON_DOWNLOAD_TITLE = Pattern('downloads_panel_uncommon_subview_title.png')
            BLOCKED_BADGE = Pattern('downloads_panel_blocked_subview_blocked_badge.png')
            UNWANTED_BADGE = Pattern('downloads_panel_blocked_subview_unwanted_badge.png')
            BLOCKED_DETAILS_1 = Pattern('downloads_panel_blocked_subview_details_1.png')
            UNWANTED_DETAILS_1 = Pattern('downloads_panel_blocked_subview_unwanted_details_1.png')
            UNCOMMON_DETAILS_1 = Pattern('downloads_panel_blocked_subview_uncommon_details_1.png')
            BLOCKED_DETAILS_2 = Pattern('downloads_panel_blocked_subview_details_2.png')
            OPEN_FILE_BUTTON = Pattern('downloads_panel_blocked_subview_open_button.png')
            REMOVE_FILE_BUTTON = Pattern('downloads_panel_blocked_subview_delete_button.png')
            BLOCKED_DOWNLOAD = Pattern('download_details_temporary_blocked.png')
            DOWNLOADS_BACK_ARROW = Pattern('downloads_panel_blocked_subview_back_arrow.png')

    # Downloaded files statuses
    class DownloadState(object):
        COMPLETED = Pattern('download_details_completed.png')
        CANCELED = Pattern('download_details_canceled.png')
        FAILED = Pattern('download_details_failed.png')
        PROGRESS = Pattern('download_details_left_size.png')
        PAUSED = Pattern('download_details_paused.png')
        RETRY_DOWNLOAD = Pattern('download_details_retry_download.png')
        OPEN_FILE = Pattern('download_details_open_file.png')
        SPEED_PER_SECOND = Pattern('download_details_speed_per_second.png')
        MISSING_FILE = Pattern('download_details_file_moved_or_missing.png')
        TEMPORARY_BLOCKED = Pattern('download_details_temporary_blocked.png')

    # Library Menu Downloads Submenu.
    class Downloads(object):
        SHOW_DOWNLOADS_FOLDER = Pattern('appmenu_library_downloads_show_button_show_downloads_folder.png')
        PANEL_HEADER_DOWNLOADS = Pattern('panel_header_downloads.png')
        SHOW_ALL_DOWNLOADS = Pattern('library_menu_downloads_more.png')
        FILE_MOVED_OR_MISSING = Pattern('file_moved_or_missing.png')
        EXTRA_SMALL_FILE_5MB_ZIP = Pattern('5mb_zip.png')

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

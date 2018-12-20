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
        DOWNLOAD_CANCEL = Pattern('downloadCancel.png')
        DOWNLOAD_CANCEL_HIGHLIGHTED = Pattern('downloadCancel_highlighted.png').similar(0.95)
        NO_DOWNLOADS_FOR_THIS_SESSION = Pattern('emptyDownloads.png')
        OPEN_CONTAINING_FOLDER = Pattern('open_containing_folder.png')

    class Downloads(object):
        SHOW_DOWNLOADS_FOLDER = Pattern('appMenu-library-downloads-show-button_show_downloads_folder.png')
        PANEL_HEADER_DOWNLOADS = Pattern('panel_header_downloads.png')
        FILE_MOVED_OR_MISSING = Pattern('file_moved_or_missing.png')
        EXTRA_SMALL_FILE_5MB_ZIP = Pattern('5MB_zip.png')

    class AboutDownloads(object):
        NO_DOWNLOADS = Pattern('there_are_no_downloads.png')

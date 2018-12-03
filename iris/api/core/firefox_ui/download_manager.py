# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from iris.api.core.pattern import Pattern


class DownloadManager(object):
    SHOW_ALL_DOWNLOADS = Pattern('downloadsHistory_show_all_Downloads.png')

    class DownloadsPanel(object):
        DOWNLOADS_BUTTON = Pattern('downloads_button_open.png')
        DOWNLOAD_RETRY = Pattern('downloadRetry.png')
        DOWNLOAD_CANCEL = Pattern('downloadCancel.png')
        NO_DOWNLOADS_FOR_THIS_SESSION = Pattern('emptyDownloads.png')

    class Downloads(object):
        SHOW_DOWNLOADS_FOLDER = Pattern('appMenu-library-downloads-show-button_show_downloads_folder.png')
        PANEL_HEADER_DOWNLOADS = Pattern('panel_header_downloads.png')

    class PrivateDownloadManager(object):
        NO_DOWNLOADS = Pattern('there_are_no_downloads.png')

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from iris.api.core.pattern import Pattern
from iris.api.core.settings import *


class Library(object):
    TITLE = Pattern('title.png')
    BACK_BUTTON_DISABLED = Pattern('back_button_disabled.png')
    FORWARD_BUTTON_DISABLED = Pattern('forward_button_disabled.png')
    BACK_BUTTON_ENABLED = Pattern('back_button_enabled.png')
    FORWARD_BUTTON_ENABLED = Pattern('forward_button_enabled.png')
    ORGANIZE_BUTTON = Pattern('organizeButton.png')

    class Organize(object):
        NEW_BOOKMARK = Pattern('newbookmark.png')
        NEW_FOLDER = Pattern('newfolder.png')
        NEW_SEPARATOR = Pattern('newseparator.png')
        if Settings.get_os() != Platform.MAC:
            CLOSE = Pattern('orgClose.png')

    VIEWS_BUTTON = Pattern('viewMenu.png')

    class Views(object):
        SHOW_COLUMNS = Pattern('viewColumns.png')

        class ShowColumns(object):
            NAME = Pattern('menucol_placesContentTitle.png')
            TAGS = Pattern('menucol_placesContentTags.png')
            LOCATION = Pattern('menucol_placesContentUrl.png')
            MOST_RECENT_VISIT = Pattern('menucol_placesContentDate.png')
            VISIT_COUNT = Pattern('menucol_placesContentVisitCount.png')
            ADDED = Pattern('menucol_placesContentDateAdded.png')
            LAST_MODIFIED = Pattern('menucol_placesContentLastModified.png')

        SORT = Pattern('viewSort.png')

        class Sort(object):
            UNSORTED = Pattern('viewUnsorted.png')
            SORT_BY_NAME = Pattern('sort_by_menucol_placesContentTitle.png')
            SORT_BY_TAGS = Pattern('sort_by_menucol_placesContentTags.png')
            SORT_BY_LOCATION = Pattern('sort_by_menucol_placesContentUrl.png')
            SORT_BY_MOST_RECENT_VISIT = Pattern('sort_by_menucol_placesContentDate.png')
            SORT_BY_VISIT_COUNT = Pattern('sort_by_menucol_placesContentVisitCount.png')
            SORT_BY_ADDED = Pattern('sort_by_menucol_placesContentDateAdded.png')
            SORT_BY_LAST_MODIFIED = Pattern('sort_by_menucol_placesContentLastModified.png')
            AZ_SORT_ORDER = Pattern('viewSortAscending.png')
            ZA_SORT_ORDER = Pattern('viewSortDescending.png')

    IMPORT_AND_BACKUP_BUTTON = Pattern('maintenanceButton.png')

    class ImportAndBackup(object):
        BACKUP = Pattern('backupBookmarks.png')
        RESTORE = Pattern('fileRestoreMenu.png')

        class Restore(object):
            CHOOSE_FILE = Pattern('restoreFromFile.png')

        IMPORT_BOOKMARKS_FROM_HTML = Pattern('fileImport.png')
        EXPORT_BOOKMARKS_FROM_HTML = Pattern('fileExport.png')
        IMPORT_DATA_FROM_ANOTHER_BROWSER = Pattern('browserImport.png')

    class DownloadLibrary(object):
        DOWNLOAD_CANCEL_HIGHLIGHTED = Pattern('download_button_cancel_icon.png')
        DOWNLOADS = Pattern('downloads.png')
        SEARCH_DOWNLOADS = Pattern('searchFilter_downloads.png')
        CLEAR_DOWNLOADS = Pattern('clearDownloadsButton.png')

    HISTORY = Pattern('history.png')
    HISTORY_NAME = Pattern('history_name.png')
    HISTORY_TODAY = Pattern('library_history_today.png')
    TODAY_NAME = Pattern('today_name.png')
    HISTORY_OLDER_THAN_6_MONTHS = Pattern('history_older_than_6_months.png')
    OLDER_THAN_6_MONTHS_NAME = Pattern('older_than_6_months_name.png')
    SEARCH_HISTORY = Pattern('searchFilter_history.png')
    TAGS = Pattern('tags.png')
    TAGS_NAME = Pattern('tags_name.png')
    ALL_BOOKMARKS = Pattern('all_bookmarks.png')
    ALL_BOOKMARKS_NAME = Pattern('all_bookmarks_name.png')
    BOOKMARKS_TOOLBAR = Pattern('bookmarks_toolbar.png')
    BOOKMARKS_TOOLBAR_NAME = Pattern('bookmarks_toolbar_name.png')
    BOOKMARKS_MENU = Pattern('bookmarks_menu.png')
    BOOKMARKS_MENU_NAME = Pattern('bookmarks_menu_name.png')
    OTHER_BOOKMARKS = Pattern('other_bookmarks.png')
    OTHER_BOOKMARKS_NAME = Pattern('other_bookmarks_name.png')
    SEARCH_BOOKMARKS = Pattern('searchFilter_bookmarks.png')
    NAME_COLUMN = Pattern('placesContentTitle.png')
    TAGS_COLUMN = Pattern('placesContentTags.png')
    LOCATION_COLUMN = Pattern('placesContentUrl.png')

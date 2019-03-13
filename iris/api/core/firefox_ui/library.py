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
    ORGANIZE_BUTTON = Pattern('organizebutton.png')

    class Organize(object):
        NEW_BOOKMARK = Pattern('newbookmark.png')
        NEW_FOLDER = Pattern('newfolder.png')
        NEW_SEPARATOR = Pattern('newseparator.png')
        if Settings.get_os() != Platform.MAC:
            CLOSE = Pattern('orgclose.png')

    VIEWS_BUTTON = Pattern('viewmenu.png')

    class Views(object):
        SHOW_COLUMNS = Pattern('viewcolumns.png')

        class ShowColumns(object):
            NAME = Pattern('menucol_placescontenttitle.png')
            TAGS = Pattern('menucol_placescontenttags.png')
            LOCATION = Pattern('menucol_placescontenturl.png')
            MOST_RECENT_VISIT = Pattern('menucol_placescontentdate.png')
            VISIT_COUNT = Pattern('menucol_placescontentvisitcount.png')
            ADDED = Pattern('menucol_placescontentdateadded.png')
            LAST_MODIFIED = Pattern('menucol_placescontentlastmodified.png')

        SORT = Pattern('viewsort.png')

        class Sort(object):
            UNSORTED = Pattern('viewunsorted.png')
            SORT_BY_NAME = Pattern('sort_by_menucol_placescontenttitle.png')
            SORT_BY_TAGS = Pattern('sort_by_menucol_placescontenttags.png')
            SORT_BY_LOCATION = Pattern('sort_by_menucol_placescontenturl.png')
            SORT_BY_MOST_RECENT_VISIT = Pattern('sort_by_menucol_placescontentdate.png')
            SORT_BY_VISIT_COUNT = Pattern('sort_by_menucol_placescontentvisitcount.png')
            SORT_BY_ADDED = Pattern('sort_by_menucol_placescontentdateadded.png')
            SORT_BY_LAST_MODIFIED = Pattern('sort_by_menucol_placescontentlastmodified.png')
            AZ_SORT_ORDER = Pattern('viewsortascending.png')
            ZA_SORT_ORDER = Pattern('viewsortdescending.png')

    IMPORT_AND_BACKUP_BUTTON = Pattern('maintenancebutton.png')

    class ImportAndBackup(object):
        BACKUP = Pattern('backupbookmarks.png')
        RESTORE = Pattern('filerestoremenu.png')

        class Restore(object):
            CHOOSE_FILE = Pattern('restorefromfile.png')

        IMPORT_BOOKMARKS_FROM_HTML = Pattern('fileimport.png')
        EXPORT_BOOKMARKS_FROM_HTML = Pattern('fileexport.png')
        IMPORT_DATA_FROM_ANOTHER_BROWSER = Pattern('browserimport.png')

    class DownloadLibrary(object):
        DOWNLOAD_CANCEL_HIGHLIGHTED = Pattern('download_button_cancel_icon.png')
        DOWNLOADS = Pattern('downloads.png')
        SEARCH_DOWNLOADS = Pattern('searchfilter_downloads.png')
        CLEAR_DOWNLOADS = Pattern('cleardownloadsbutton.png')

    HISTORY = Pattern('history.png')
    HISTORY_NAME = Pattern('history_name.png')
    HISTORY_TODAY = Pattern('library_history_today.png')
    TODAY_NAME = Pattern('today_name.png')
    HISTORY_OLDER_THAN_6_MONTHS = Pattern('history_older_than_6_months.png')
    OLDER_THAN_6_MONTHS_NAME = Pattern('older_than_6_months_name.png')
    SEARCH_HISTORY = Pattern('searchfilter_history.png')
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
    SEARCH_BOOKMARKS = Pattern('searchfilter_bookmarks.png')
    NAME_COLUMN = Pattern('placescontenttitle.png')
    TAGS_COLUMN = Pattern('placescontenttags.png')
    LOCATION_COLUMN = Pattern('placescontenturl.png')

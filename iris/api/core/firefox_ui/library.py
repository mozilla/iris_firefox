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
    ORGANIZE_BUTTON = Pattern('organize_button.png')

    class Organize(object):
        NEW_BOOKMARK = Pattern('newbookmark.png')
        NEW_FOLDER = Pattern('newfolder.png')
        NEW_SEPARATOR = Pattern('newseparator.png')
        if Settings.get_os() != Platform.MAC:
            CLOSE = Pattern('org_close.png')

    VIEWS_BUTTON = Pattern('view_menu.png')

    class Views(object):
        SHOW_COLUMNS = Pattern('view_menu.png')

        class ShowColumns(object):
            NAME = Pattern('menucol_places_content_title.png')
            TAGS = Pattern('menucol_places_content_tags.png')
            LOCATION = Pattern('menucol_places_content_url.png')
            MOST_RECENT_VISIT = Pattern('menucol_places_content_date.png')
            VISIT_COUNT = Pattern('menucol_places_content_visit_count.png')
            ADDED = Pattern('menucol_places_content_date_added.png')
            LAST_MODIFIED = Pattern('menucol_places_content_last_modified.png')

        SORT = Pattern('view_sort.png')

        class Sort(object):
            UNSORTED = Pattern('view_unsorted.png')
            SORT_BY_NAME = Pattern('sort_by_menucol_places_content_title.png')
            SORT_BY_TAGS = Pattern('sort_by_menucol_places_content_tags.png')
            SORT_BY_LOCATION = Pattern('sort_by_menucol_places_content_url.png')
            SORT_BY_MOST_RECENT_VISIT = Pattern('sort_by_menucol_places_content_date.png')
            SORT_BY_VISIT_COUNT = Pattern('sort_by_menucol_places_content_visit_count.png')
            SORT_BY_ADDED = Pattern('sort_by_menucol_places_content_date_added.png')
            SORT_BY_LAST_MODIFIED = Pattern('sort_by_menucol_places_content_last_modified.png')
            AZ_SORT_ORDER = Pattern('view_sort_ascending.png')
            ZA_SORT_ORDER = Pattern('view_sort_descending.png')

    IMPORT_AND_BACKUP_BUTTON = Pattern('maintenance_button.png')

    class ImportAndBackup(object):
        BACKUP = Pattern('backup_bookmarks.png')
        RESTORE = Pattern('file_restore_menu.png')

        class Restore(object):
            CHOOSE_FILE = Pattern('restore_from_file.png')

        IMPORT_BOOKMARKS_FROM_HTML = Pattern('file_import.png')
        EXPORT_BOOKMARKS_FROM_HTML = Pattern('file_export.png')
        IMPORT_DATA_FROM_ANOTHER_BROWSER = Pattern('browser_import.png')

    class DownloadLibrary(object):
        DOWNLOAD_CANCEL_HIGHLIGHTED = Pattern('download_button_cancel_icon.png')
        DOWNLOADS = Pattern('downloads.png')
        SEARCH_DOWNLOADS = Pattern('searchfilter_downloads.png')
        CLEAR_DOWNLOADS = Pattern('clear_downloads_button.png')

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
    NAME_COLUMN = Pattern('places_content_title.png')
    TAGS_COLUMN = Pattern('places_content_tags.png')
    LOCATION_COLUMN = Pattern('places_content_url.png')

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from iris.api.core.pattern import Pattern


class Sidebar(object):
    class SidebarHeader(object):
        SIDEBAR_ARROW_SWITCHER = Pattern('sidebar_switcher_arrow.png')
        SIDEBAR_CLOSE = Pattern('sidebar_close.png')
        CLOSE_ARROW = Pattern('close_arrow.png')
        OPEN_ARROW = Pattern('open_arrow.png')
        CLEAR_SEARCH_BOX = Pattern('clear_textbox_search.png')

    class HistorySidebar(object):
        SIDEBAR_HISTORY_TITLE = Pattern('sidebar_history_title.png')
        SIDEBAR_HISTORY_ICON = Pattern('sidebar_history_icon.png')
        EXPLORED_HISTORY_ICON = Pattern('explored_history_icon.png')
        VIEW_BUTTON = Pattern('view_button.png')
        SEARCH_BOX = Pattern('history_search_box.png')
        SEARCH_BOX_FOCUSED = Pattern('history_search_box_focused.png')

        class ViewBy(object):
            VIEW_BY_SITE = Pattern('by_site.png')
            VIEW_BY_LAST_VISITED = Pattern('by_last_visited.png')
            VIEW_BY_DATE_AND_SITE = Pattern('by_date_and_site.png')
            VIEW_BY_DATE = Pattern('by_date.png')
            VIEW_BY_MOST_VISITED = Pattern('by_most_visited.png')

            # Checked view menu items
            VIEW_BY_SITE_CHECKED = Pattern('by_site_checked.png')
            VIEW_BY_LAST_VISITED_CHECKED = Pattern('by_last_visited_checked.png')
            VIEW_BY_DATE_AND_SITE_CHECKED = Pattern('by_date_and_site_checked.png')
            VIEW_BY_DATE_CHECKED = Pattern('by_date_checked.png')
            VIEW_BY_MOST_VISITED_CHECKED = Pattern('by_most_visited_checked.png')

        class Timeline(object):
            TODAY = Pattern('history_today.png')
            YESTERDAY = Pattern('history_yesterday.png')
            LAST_7_DAYS = Pattern('history_last_7_days.png')
            JANUARY = Pattern('history_january.png')
            FEBRUARY = Pattern('history_february.png')
            MARCH = Pattern('history_march.png')
            APRIL = Pattern('history_april.png')
            MAY = Pattern('history_may.png')
            JUNE = Pattern('history_june.png')
            JULY = Pattern('history_july.png')
            AUGUST = Pattern('history_august.png')
            SEPTEMBER = Pattern('history_september.png')
            OCTOBER = Pattern('history_october.png')
            NOVEMBER = Pattern('history_november.png')
            DECEMBER = Pattern('history_december.png')

    class BookmarksSidebar(object):
        SIDEBAR_BOOKMARKS_TITLE = Pattern('sidebar_bookmarks_title.png')
        SIDEBAR_BOOKMARKS_ICON = Pattern('sidebar_bookmarks_icon.png')

    class SyncedTabsSidebar(object):
        SIDEBAR_SYNCED_TABS_TITLE = Pattern('sidebar_synced_tabs_title.png')
        SIDEBAR_SYNCED_TABS_ICON = Pattern('sidebar_synced_tabs_icon.png')

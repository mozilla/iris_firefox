# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from iris.api.core.pattern import Pattern


class LibraryMenu(object):
    BOOKMARKS_OPTION = Pattern('library_menu_bookmarks_option.png')

    class BookmarksOption(object):
        BOOKMARKING_TOOLS = Pattern('bookmarking_tools.png')
        SEARCH_BOOKMARKS = Pattern('search_bookmarks.png')

        class BookmarkingTools(object):
            VIEW_BOOKMARKS_TOOLBAR = Pattern('view_bookmarks_toolbar.png')
            VIEW_BOOKMARKS_SIDEBAR = Pattern('view_bookmarks_sidebar.png')


class SidebarBookmarks(object):
    BOOKMARKS_HEADER = Pattern('bookmarks_header.png')
    BOOKMARKS_MENU = Pattern('sidebar_bookmarks_menu.png')
    BOOKMARKS_MENU_SELECTED = Pattern('sidebar_bookmarks_menu_selected.png')
    OTHER_BOOKMARKS = Pattern('sidebar_other_bookmarks.png')

    class BookmarksToolbar(object):
        MOST_VISITED = Pattern('bookmarks_toolbar_most_visited.png')

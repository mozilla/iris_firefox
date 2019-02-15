# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):
    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Change the files order in the Bookmarks Toolbar section from Firefox menu'
        self.test_case_id = '163482'
        self.test_suite_id = '2525'
        self.locales = ['en-US']
        self.exclude = [Platform.MAC, Platform.LINUX]

    def run(self):
        library_bookmarks_pattern = Library.BOOKMARKS_TOOLBAR
        bookmarks_most_visited = SidebarBookmarks.BookmarksToolbar.MOST_VISITED
        mozilla_bookmark_icon_pattern = Pattern('mozilla_bookmark_icon.png')
        bookmarks_top_menu_pattern = Pattern('bookmarks_top_menu.png')
        bookmark_after_drag_and_drop_pattern = Pattern('bookmark_after_drag_and_drop.png')

        #  open Bookmark toolbar from bookmark section of Firefox menu
        if Settings.is_linux():
            key_down(Key.ALT)
            time.sleep(DEFAULT_FX_DELAY)
            key_up(Key.ALT)
        else:
            type(Key.ALT)

        bookmarks_top_menu = exists(bookmarks_top_menu_pattern)
        assert_true(self, bookmarks_top_menu, 'Bookmarks top menu displayed')

        click(bookmarks_top_menu_pattern)
        library_bookmarks = exists(library_bookmarks_pattern)
        assert_true(self, library_bookmarks, 'Library bookmarks button displayed')
        library_location_x = find(library_bookmarks_pattern).x
        find_drop_region = Region(library_location_x, 0, width=SCREEN_WIDTH/2, height=SCREEN_HEIGHT)

        click(library_bookmarks_pattern)
        mozilla_bookmark_icon = exists(mozilla_bookmark_icon_pattern)
        assert_true(self, mozilla_bookmark_icon, 'Mozilla bookmark icon displayed.')

        bookmarks_most_visited_exists = exists(bookmarks_most_visited)
        assert_true(self, bookmarks_most_visited_exists,
                    'Most Visited section and the Folders and websites from the Bookmark Toolbar are displayed')

        drop_from_location = find(mozilla_bookmark_icon_pattern)
        drop_to_location = find(bookmarks_most_visited, find_drop_region)

        drag_drop(drop_from_location, drop_to_location)

        bookmark_dropped = exists(bookmark_after_drag_and_drop_pattern)
        assert_true(self, bookmark_dropped, 'The order of files is changed successfully.')

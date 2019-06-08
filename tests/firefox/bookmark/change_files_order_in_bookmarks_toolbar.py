# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Change the files order in the Bookmarks Toolbar section from Firefox menu',
        locale=['en-US'],
        test_case_id='163482',
        test_suite_id='2525',
        profile=Profiles.TEN_BOOKMARKS,
        exclude=[OSPlatform.MAC, OSPlatform.LINUX]
    )
    def run(self, firefox):
        library_bookmarks_pattern = Library.BOOKMARKS_TOOLBAR
        bookmarks_most_visited = SidebarBookmarks.BookmarksToolbar.MOST_VISITED
        mozilla_bookmark_icon_pattern = Pattern('mozilla_bookmark_icon.png')
        bookmarks_top_menu_pattern = Pattern('bookmarks_top_menu.png')
        bookmark_after_drag_and_drop_pattern = Pattern('bookmark_after_drag_and_drop.png')

        open_firefox_menu()

        click(bookmarks_top_menu_pattern)
        library_bookmarks = exists(library_bookmarks_pattern)
        assert library_bookmarks is True, 'Library bookmarks button displayed'

        library_location_x = find(library_bookmarks_pattern).x
        find_drop_region = Region(library_location_x, 0, width=Screen.SCREEN_WIDTH/2, height=Screen.SCREEN_HEIGHT)

        click(library_bookmarks_pattern)
        mozilla_bookmark_icon = exists(mozilla_bookmark_icon_pattern)
        assert mozilla_bookmark_icon is True, 'Mozilla bookmark icon displayed.'

        bookmarks_most_visited_exists = exists(bookmarks_most_visited)
        assert bookmarks_most_visited_exists is True, 'Most Visited section and the Folders and websites from the ' \
                                                      'Bookmark Toolbar are displayed'

        drop_from_location = find(mozilla_bookmark_icon_pattern)
        drop_to_location = find(bookmarks_most_visited, find_drop_region)

        drag_drop(drop_from_location, drop_to_location)

        bookmark_dropped = exists(bookmark_after_drag_and_drop_pattern)
        assert bookmark_dropped is True, 'The order of files is changed successfully.'

        restore_firefox_focus()

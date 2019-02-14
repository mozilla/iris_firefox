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

    def setup(self):
        BaseTest.setup(self)
        self.profile = Profile.TEN_BOOKMARKS
        return

    def run(self):
        bookmarks_most_visited_pattern = SidebarBookmarks.BookmarksToolbar.MOST_VISITED
        add_new_bookmark_pattern = Library.Organize.NEW_BOOKMARK
        add_bookmark_panel_name_pattern = Bookmarks.StarDialog.NAME_FIELD
        if Settings.is_linux():
            library_bookmarks_pattern = Pattern('bookmarks_toolbar_top_menu.png')
        else:
            library_bookmarks_pattern = Library.BOOKMARKS_TOOLBAR
        mozilla_bookmark_icon_pattern = Pattern('mozilla_bookmark_icon.png')
        bookmarks_top_menu_pattern = Pattern('bookmarks_top_menu.png')
        bookmark_after_drag_and_drop_pattern = Pattern('bookmark_after_drag_and_drop.png')
        context_menu_bookmarks_toolbar_pattern = Pattern('bookmarks_toolbar_navbar_context_menu.png')
        add_bookmark_location_field_pattern = Pattern('add_bookmark_location_field.png')
        add_bookmark_popup_button_pattern = Pattern('add_button.png')

        #  add Bookmark via Bookmark toolbar
        home_button_displayed = exists(NavBar.HOME_BUTTON, DEFAULT_UI_DELAY)
        assert_true(self, home_button_displayed, 'Home button displayed')

        home_button = NavBar.HOME_BUTTON
        w, h = home_button.get_size()
        horizontal_offset = w * 1.7
        vertical_offset = h * 2.1
        navbar_context_menu = home_button.target_offset(horizontal_offset, 0)
        navbar_add_bookmark_context_menu = home_button.target_offset(0, vertical_offset)

        right_click(navbar_context_menu)

        context_menu_bookmarks_toolbar = exists(context_menu_bookmarks_toolbar_pattern)
        assert_true(self, context_menu_bookmarks_toolbar, 'Context menu bookmarks toolbar option exists')
        click(context_menu_bookmarks_toolbar_pattern)

        right_click(navbar_add_bookmark_context_menu)

        add_new_bookmark = exists(add_new_bookmark_pattern)
        assert_true(self, add_new_bookmark, '"Add new bookmark" option exists')

        click(add_new_bookmark_pattern)

        add_bookmark_popup = exists(add_bookmark_panel_name_pattern)
        assert_true(self, add_bookmark_popup, 'Add bookmark popup loaded')

        add_bookmark_location_field = exists(add_bookmark_location_field_pattern)
        assert_true(self, add_bookmark_location_field, '"Add bookmark" popup loaded, and location field available')

        click(add_bookmark_location_field_pattern)
        paste('https://www.mozilla.org/en-US/firefox/central/')

        add_bookmark_popup_button = exists(add_bookmark_popup_button_pattern)
        assert_true(self, add_bookmark_popup_button, '"Add" button available')
        click(add_bookmark_popup_button_pattern)

        #  dragging of bookmark
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

        bookmarks_most_visited_exists = exists(bookmarks_most_visited_pattern)
        assert_true(self, bookmarks_most_visited_exists,
                    'Most Visited section and the Folders and websites from the Bookmark Toolbar are displayed')

        drop_from_location = find(mozilla_bookmark_icon_pattern)
        drop_to_location = find(bookmarks_most_visited_pattern, find_drop_region)

        drag_drop(drop_from_location, drop_to_location)

        bookmark_dropped = exists(bookmark_after_drag_and_drop_pattern)
        assert_true(self, bookmark_dropped, 'The order of files is changed successfully.')

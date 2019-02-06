# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Tags can be added to bookmarks using the star-shaped button.'
        self.test_case_id = '171637'
        self.test_suite_id = '2525'
        self.locales = ['en-US']

    def run(self):
        if Settings.is_linux:
            library_bookmarks_pattern = Pattern('bookmarks_toolbar_top_menu.png')
        else:
            library_bookmarks_pattern = Library.BOOKMARKS_TOOLBAR
        mozilla_bookmark_icon_pattern = Pattern('mozilla_bookmark_icon.png')
        folder_added_to_bookmarks_icons_pattern = Pattern('folder_added_to_bookmarks_icons.png')
        bookmarks_top_menu_pattern = Pattern('bookmarks_top_menu.png')

        if Settings.is_linux:
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
        click(library_bookmarks_pattern)

        mozilla_bookmark_icon = exists(mozilla_bookmark_icon_pattern)
        assert_true(self, mozilla_bookmark_icon, 'Mozilla bookmark icon displayed')

        right_click(mozilla_bookmark_icon_pattern)
        type('f', interval=DEFAULT_FX_DELAY)

        type(Key.ENTER)

        if Settings.is_linux:
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
        click(library_bookmarks_pattern)

        folder_added = exists(folder_added_to_bookmarks_icons_pattern)
        assert_true(self, folder_added, 'A new folder is correctly created in the Bookmarks Toolbar,' \
                            ' in front of the selected file.')


# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Bookmark a page from the \'Most Visited\' section using the option from the contextual menu'
        self.test_case_id = '163202'
        self.test_suite_id = '2525'
        self.locale = ['en-US']
        self.exclude = [Platform.MAC]

    def setup(self):
        BaseTest.setup(self)
        self.profile = Profile.TEN_BOOKMARKS
        return

    def run(self):
        firefox_menu_bookmarks_pattern = Pattern('firefox_menu_bookmarks.png')
        firefox_menu_bookmarks_toolbar_pattern = Pattern('firefox_menu_bookmarks_toolbar.png')
        firefox_menu_most_visited_pattern = Pattern('firefox_menu_most_visited.png')
        firefox_pocket_bookmark_pattern = Pattern('pocket_most_visited.png')
        bookmark_page_option_pattern = Pattern('context_menu_bookmark_page_option.png')

        open_firefox_menu()

        firefox_menu_bookmarks_exists = exists(firefox_menu_bookmarks_pattern, Settings.SHORT_FIREFOX_TIMEOUT)
        assert_true(self, firefox_menu_bookmarks_exists, 'Firefox menu > Bookmarks exists')

        click(firefox_menu_bookmarks_pattern)

        bookmarks_toolbar_folder_exists = exists(firefox_menu_bookmarks_toolbar_pattern, Settings.SHORT_FIREFOX_TIMEOUT)
        assert_true(self, bookmarks_toolbar_folder_exists, 'Firefox menu > Bookmarks > Bookmarks Toolbar folder exists')

        click(firefox_menu_bookmarks_toolbar_pattern)

        most_visited_folder_exists = exists(firefox_menu_most_visited_pattern, Settings.SHORT_FIREFOX_TIMEOUT)
        assert_true(self, most_visited_folder_exists, 'Firefox menu > Bookmarks > Bookmarks Toolbar > Most Visited '
                                                      'folder exists')

        click(firefox_menu_most_visited_pattern)

        firefox_pocket_bookmark_exists = exists(firefox_pocket_bookmark_pattern, Settings.SHORT_FIREFOX_TIMEOUT)
        assert_true(self, firefox_pocket_bookmark_exists, 'Most visited websites are displayed.')

        right_click(firefox_pocket_bookmark_pattern, 0)

        bookmark_page_option_exists = exists(bookmark_page_option_pattern, DEFAULT_SHORT_FIREFOX_TIMEOUT)
        assert_true(self, bookmark_page_option_exists, 'Bookmark page option exists')

        click(bookmark_page_option_pattern)

        new_bookmark_window_exists = exists(Bookmarks.StarDialog.NAME_FIELD, Settings.FIREFOX_TIMEOUT)
        assert_true(self, new_bookmark_window_exists, 'New Bookmark window is displayed')

        paste('Focus')

        folders_expander_exists = exists(Bookmarks.StarDialog.PANEL_FOLDERS_EXPANDER.similar(.6),
                                         Settings.FIREFOX_TIMEOUT)
        assert_true(self, folders_expander_exists, 'Folders expander is displayed')

        click(Bookmarks.StarDialog.PANEL_FOLDERS_EXPANDER)

        bookmarks_toolbar_option_exists = exists(Library.BOOKMARKS_TOOLBAR,
                                                 Settings.FIREFOX_TIMEOUT)
        assert_true(self, bookmarks_toolbar_option_exists, 'Bookmark toolbar folder option is displayed')

        click(Library.BOOKMARKS_TOOLBAR)

        tags_field_exists = exists(Bookmarks.StarDialog.TAGS_FIELD, Settings.SHORT_FIREFOX_TIMEOUT)
        assert_true(self, tags_field_exists, 'Tags field exists')

        click(Bookmarks.StarDialog.TAGS_FIELD)

        paste('tag')

        type(Key.ENTER)

        bookmark_added_to_toolbar = exists(LocalWeb.FOCUS_BOOKMARK_SMALL, Settings.SHORT_FIREFOX_TIMEOUT)
        assert_true(self, bookmark_added_to_toolbar, 'The bookmark is correctly added to Bookmarks Toolbar.')

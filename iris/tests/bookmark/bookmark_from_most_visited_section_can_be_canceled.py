# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Bookmark a page from the \'Most Visited\' section using the option from the contextual menu can ' \
                    'be canceled'
        self.test_case_id = '163397'
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
        if Settings.is_linux():
            new_window_pattern = Pattern('new_bookmark_popup.png')
        else:
            new_window_pattern = Bookmarks.StarDialog.NEW_BOOKMARK

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

        bookmark_page_option_exists = exists(bookmark_page_option_pattern, Settings.SHORT_FIREFOX_TIMEOUT)
        assert_true(self, bookmark_page_option_exists, 'Open in a New Private Window option exists')

        click(bookmark_page_option_pattern)

        new_bookmark_window_exists = exists(new_window_pattern, Settings.SITE_LOAD_TIMEOUT)
        assert_true(self, new_bookmark_window_exists, 'New Bookmark window is displayed')

        click_cancel_button()

        try:
            new_bookmark_window_dismissed = wait_vanish(new_window_pattern)
            assert_true(self, new_bookmark_window_dismissed, 'The popup is dismissed')
        except FindError:
            raise FindError('The popup is not dismissed.')

        bookmarks_sidebar('open')

        bookmark_menu_folder_exists = exists(SidebarBookmarks.BOOKMARKS_MENU, Settings.FIREFOX_TIMEOUT)
        assert_true(self, bookmark_menu_folder_exists, 'Bookmarks Menu folder exists')

        click(SidebarBookmarks.BOOKMARKS_MENU)

        bookmark_menu_folder_opened = exists(SidebarBookmarks.BOOKMARKS_MENU_SELECTED)
        assert_true(self, bookmark_menu_folder_opened, 'Bookmarks Menu folder exists')

        bookmark_not_added = exists(LocalWeb.POCKET_BOOKMARK_SMALL)
        assert_false(self, bookmark_not_added, 'The page is not bookmarked.')




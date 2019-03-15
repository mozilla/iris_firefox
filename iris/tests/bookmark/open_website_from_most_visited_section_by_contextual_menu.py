# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Open a website from \'Most Visited\' section using contextual menu'
        self.test_case_id = '163198'
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
        context_menu_open_pattern = Pattern('open_option.png')

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

        open_option_exists = exists(context_menu_open_pattern, Settings.SHORT_FIREFOX_TIMEOUT)
        assert_true(self, open_option_exists, 'Open option exists')

        click(context_menu_open_pattern)

        firefox_pocket_site_opened = exists(LocalWeb.POCKET_LOGO, Settings.SITE_LOAD_TIMEOUT)
        assert_true(self, firefox_pocket_site_opened, 'The website is opened')

        site_opened_in_current_tab = exists(LocalWeb.IRIS_LOGO_INACTIVE_TAB)
        assert_false(self, site_opened_in_current_tab, 'The selected website is opened in the current tab.')

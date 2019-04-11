# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Open all bookmarks from \'Most Visited\' section'
        self.test_case_id = '163381'
        self.test_suite_id = '2525'
        self.locale = ['en-US']

    def setup(self):
        BaseTest.setup(self)
        self.profile = Profile.TEN_BOOKMARKS
        return

    def run(self):
        firefox_menu_bookmarks_pattern = Pattern('firefox_menu_bookmarks.png')
        firefox_menu_bookmarks_toolbar_pattern = Pattern('firefox_menu_bookmarks_toolbar.png')
        firefox_menu_most_visited_pattern = Pattern('firefox_menu_most_visited.png')
        firefox_pocket_bookmark_pattern = Pattern('pocket_most_visited.png')
        open_all_in_tabs_option_pattern = Pattern('open_all_in_tabs.png')
        yahoo_logo_pattern = Pattern('yahoo_logo.png')
        google_logo_pattern = Pattern('google_logo.png')
        el_pais_logo_pattern = Pattern('el_pais_logo.png')

        tabs = [google_logo_pattern, LocalWeb.IRIS_LOGO_ACTIVE_TAB, LocalWeb.POCKET_LOGO,
                LocalWeb.MOZILLA_LOGO, LocalWeb.FOCUS_LOGO, LocalWeb.FIREFOX_LOGO, LocalWeb.IRIS_LOGO_ACTIVE_TAB,
                el_pais_logo_pattern, el_pais_logo_pattern, yahoo_logo_pattern]

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

        open_all_in_tabs_option_exists = exists(open_all_in_tabs_option_pattern, Settings.SHORT_FIREFOX_TIMEOUT)
        assert_true(self, open_all_in_tabs_option_exists, 'Open All in Tabs option exists')

        click(open_all_in_tabs_option_pattern, 0)

        select_tab(2)

        num = 0

        for tab in tabs:
            num += 1
            site_from_list_opened = exists(tab, Settings.HEAVY_SITE_LOAD_TIMEOUT)
            assert_true(self, site_from_list_opened, 'The website #' + str(num) + ' from \'Most Visited\' '
                                                                                  'section is opened')
            next_tab()

        all_websites_are_opened = exists(LocalWeb.IRIS_LOGO)
        assert_true(self, all_websites_are_opened, 'All the websites from the Most visited section are opened in '
                                                   'separate tabs, in the same window.')

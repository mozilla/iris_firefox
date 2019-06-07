# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Open all bookmarks from \'Most Visited\' section',
        locale=['en-US'],
        test_case_id='163381',
        test_suite_id='2525',
        profile=Profiles.TEN_BOOKMARKS
    )
    def run(self, firefox):
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

        firefox_menu_bookmarks_exists = exists(firefox_menu_bookmarks_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert firefox_menu_bookmarks_exists is True, 'Firefox menu > Bookmarks exists'

        click(firefox_menu_bookmarks_pattern)

        bookmarks_toolbar_folder_exists = exists(firefox_menu_bookmarks_toolbar_pattern,
                                                 FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert bookmarks_toolbar_folder_exists is True, 'Firefox menu > Bookmarks > Bookmarks Toolbar folder exists'

        click(firefox_menu_bookmarks_toolbar_pattern)

        most_visited_folder_exists = exists(firefox_menu_most_visited_pattern,
                                            FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert most_visited_folder_exists is True, 'Firefox menu > Bookmarks > Bookmarks Toolbar > Most Visited ' \
                                                   'folder exists'

        click(firefox_menu_most_visited_pattern)

        firefox_pocket_bookmark_exists = exists(firefox_pocket_bookmark_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert firefox_pocket_bookmark_exists is True, 'Most visited websites are displayed.'

        open_all_in_tabs_option_exists = exists(open_all_in_tabs_option_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert open_all_in_tabs_option_exists is True, 'Open All in Tabs option exists'

        click(open_all_in_tabs_option_pattern, 0)

        select_tab("2")

        num = 0

        for tab in tabs:
            num += 1
            site_from_list_opened = exists(tab, FirefoxSettings.HEAVY_SITE_LOAD_TIMEOUT)
            assert site_from_list_opened is True, 'The website #' + str(num) + ' from \'Most Visited\' section ' \
                                                                               'is opened'
            next_tab()

        all_websites_are_opened = exists(LocalWeb.IRIS_LOGO)
        assert all_websites_are_opened is True, 'All the websites from the Most visited section are opened in ' \
                                                'separate tabs, in the same window.'

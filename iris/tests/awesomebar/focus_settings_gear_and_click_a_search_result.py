# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'This test case clicks on a search result while the settings gear is focused.'
        self.test_case_id = '108264'
        self.test_suite_id = '1902'
        self.locales = ['en-US']

    def run(self):
        search_settings_pattern = Pattern('search_settings.png')
        page_bookmarked_pattern = Bookmarks.StarDialog.NEW_BOOKMARK
        settings_gear_highlighted_pattern = Pattern('settings_gear_highlighted.png')
        search_suggestion_history_pattern = Pattern('search_suggestion_history.png')

        region = Region(0, 0, SCREEN_WIDTH, 2 * SCREEN_HEIGHT / 3)

        # Open some pages to create some history.
        navigate(LocalWeb.MOZILLA_TEST_SITE)
        expected = region.exists(LocalWeb.MOZILLA_LOGO, 10)
        assert_true(self, expected, 'Mozilla page loaded successfully.')

        bookmark_page()

        expected = region.exists(page_bookmarked_pattern, 10)
        assert_true(self, expected, 'Page was bookmarked.')

        new_tab()
        navigate(LocalWeb.FIREFOX_TEST_SITE)
        expected = region.exists(LocalWeb.FIREFOX_LOGO, 10)
        assert_true(self, expected, 'Firefox page loaded successfully.')

        new_tab()
        navigate(LocalWeb.FOCUS_TEST_SITE)
        expected = region.exists(LocalWeb.FOCUS_LOGO, 10)
        assert_true(self, expected, 'Focus page loaded successfully.')

        restart_firefox(self,
                        self.browser.path,
                        self.profile_path,
                        LocalWeb.FIREFOX_TEST_SITE,
                        image=LocalWeb.FIREFOX_LOGO)

        new_tab()

        select_location_bar()
        paste('fo')

        expected = region.exists(search_settings_pattern, 10)
        assert_true(self, expected, 'The \'Search settings\' button is displayed in the awesomebar.')

        # Wait a moment for the suggests list to fully populate before stepping down through it.
        time.sleep(Settings.UI_DELAY)

        repeat_key_down(16)
        key_to_one_off_search(settings_gear_highlighted_pattern, "right")

        expected = region.exists(settings_gear_highlighted_pattern, 5)
        assert_true(self, expected, 'The \'Search settings\' button has focus.')

        expected = region.exists(search_suggestion_history_pattern, 10)
        assert_true(self, expected, 'Web pages from personal browsing history found between search suggestions.')

        # Find the coordinates of the above search suggestion.
        coord = find(search_suggestion_history_pattern)

        click(coord)

        # The page corresponding to the search result is opened and NOT the about:preferences#search page.
        expected = region.exists(LocalWeb.FOCUS_LOGO, 10)
        assert_true(self, expected, 'Focus page loaded successfully.')

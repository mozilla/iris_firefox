# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='This test case clicks on a search result while the settings gear is focused.',
        locale=['en-US'],
        test_case_id='108264',
        test_suite_id='1902'
    )
    def run(self, firefox):
        search_settings_pattern = Pattern('search_settings.png')
        page_bookmarked_pattern = Bookmarks.StarDialog.NEW_BOOKMARK
        settings_gear_highlighted_pattern = Pattern('settings_gear_highlighted.png')
        search_suggestion_history_pattern = Pattern('search_suggestion_history.png').similar(.7)

        region = Screen().new_region(0, 0, Screen.SCREEN_WIDTH, 2 * Screen.SCREEN_HEIGHT / 3)

        navigate(LocalWeb.MOZILLA_TEST_SITE)

        expected = region.exists(LocalWeb.MOZILLA_LOGO, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, 'Mozilla page loaded successfully.'

        bookmark_page()

        expected = region.exists(page_bookmarked_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, 'Page was bookmarked.'

        new_tab()
        navigate(LocalWeb.FIREFOX_TEST_SITE)

        expected = region.exists(LocalWeb.FIREFOX_LOGO, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, 'Firefox page loaded successfully.'

        new_tab()
        navigate(LocalWeb.FOCUS_TEST_SITE)

        expected = region.exists(LocalWeb.FOCUS_LOGO, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, 'Focus page loaded successfully.'

        firefox.restart(url=LocalWeb.FIREFOX_TEST_SITE, image=LocalWeb.FIREFOX_LOGO)

        new_tab()

        select_location_bar()
        paste('fo')

        expected = region.exists(search_settings_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, 'The \'Search settings\' button is displayed in the awesomebar.'

        # Wait a moment for the suggests list to fully populate before stepping down through it.
        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)

        repeat_key_down(16)
        key_to_one_off_search(settings_gear_highlighted_pattern, "right")

        expected = region.exists(settings_gear_highlighted_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert expected, 'The \'Search settings\' button has focus.'

        expected = region.exists(search_suggestion_history_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, 'Web pages from personal browsing history found between search suggestions.'

        # Find the coordinates of the above search suggestion.

        click(search_suggestion_history_pattern)

        # The page corresponding to the search result is opened and NOT the about:preferences#search page.
        expected = region.exists(LocalWeb.FOCUS_LOGO, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, 'Focus page loaded successfully.'

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='This test case perform a search using an one-off focusing on the autocomplete drop-down.',
        locale=[Locales.ENGLISH],
        test_case_id='108249',
        test_suite_id='1902',
        # blocked_by='issue_84'
    )
    def run(self, firefox):
        page_bookmarked_pattern = Bookmarks.StarDialog.NEW_BOOKMARK
        search_suggestion_bookmarked_tab_pattern = Pattern('search_suggestion_bookmarked_tab.png')
        search_suggestion_opened_tab_pattern = Pattern('search_suggestion_opened_tab.png')
        search_suggestion_history_pattern = Pattern('search_suggestion_history.png')
        popular_search_suggestion_pattern = Pattern('popular_search_suggestion.png')
        google_one_off_button_pattern = Pattern('google_one_off_button.png')
        google_search_results_pattern = Pattern('google_search_results.png')

        region = Screen().new_region(0, 0, Screen.SCREEN_WIDTH, 2 * Screen.SCREEN_HEIGHT / 3)
        navigate(LocalWeb.MOZILLA_TEST_SITE)

        expected = region.exists(LocalWeb.MOZILLA_LOGO, 10)
        assert expected, 'Mozilla page loaded successfully.'

        bookmark_page()

        expected = region.exists(page_bookmarked_pattern, 10)
        assert expected, 'Page was bookmarked.'

        new_tab()
        navigate(LocalWeb.FIREFOX_TEST_SITE)

        expected = region.exists(LocalWeb.FIREFOX_LOGO, 10)
        assert expected, 'Firefox page loaded successfully.'

        new_tab()
        navigate(LocalWeb.FOCUS_TEST_SITE)

        expected = region.exists(LocalWeb.FOCUS_LOGO, 10)
        assert expected, 'Focus page loaded successfully.'

        firefox.restart(LocalWeb.FIREFOX_TEST_SITE, image=LocalWeb.FIREFOX_LOGO)

        new_tab()

        select_location_bar()
        paste('m')

        expected = region.exists(search_suggestion_bookmarked_tab_pattern, 10)
        assert expected, 'Bookmarked page found between search suggestions.'

        select_location_bar()
        paste('o')

        expected = region.exists(search_suggestion_opened_tab_pattern, 10)
        assert expected, 'Opened tab found between search suggestions.'

        select_location_bar()
        paste('f')

        expected = region.exists(search_suggestion_history_pattern, 10)
        assert expected, 'Web pages from personal browsing history found between search suggestions.'

        expected = region.exists(popular_search_suggestion_pattern, 10)
        assert expected, 'Popular search suggestions from the default search engine found between search suggestions.'

        expected = region.exists(google_one_off_button_pattern, 10)
        assert expected, 'The \'Google\' one-off button found.'

        click(google_one_off_button_pattern)
        time.sleep(Settings.DEFAULT_UI_DELAY_LONG)

        expected = exists(google_search_results_pattern, 10)
        assert expected, 'Google search results are displayed.'

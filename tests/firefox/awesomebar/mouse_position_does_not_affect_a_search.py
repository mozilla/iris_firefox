# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='This test case checks that mouse position does not affect a search from awesomebar.',
        locale=['en-US'],
        test_case_id='108256',
        test_suite_id='1902'
    )
    def run(self, firefox):
        local_url = LocalWeb.FIREFOX_TEST_SITE
        duck_duck_go_one_off_button = Pattern('duck_duck_go_one_off_button.png')
        search_results_listed_pattern = Pattern('search_results_listed.png')
        result_is_focused_pattern = Pattern('result_is_focused.png')

        top_two_third_screen_region = Region(0, 0, Screen.SCREEN_WIDTH, 2 * Screen.SCREEN_HEIGHT // 3)

        change_preference('browser.urlbar.suggest.searches', 'false')

        navigate(local_url)

        local_url_loaded = exists(LocalWeb.FIREFOX_LOGO, Settings.FIREFOX_TIMEOUT)
        assert local_url_loaded, 'Page successfully loaded, firefox logo found.'

        select_location_bar()
        paste('moz')

        search_engine_logo_icon = exists(duck_duck_go_one_off_button.similar(0.7), Settings.FIREFOX_TIMEOUT,
                                         region=top_two_third_screen_region)
        assert search_engine_logo_icon, 'The \'DuckDuckGo\' one-off button found.'

        # Find the coordinates of the one-off button.
        search_engine_location = find(duck_duck_go_one_off_button)

        # In a new tab place the mouse cursor at a position that will later match position of a search
        # engine(e.g 'DuckDuckGo') icon in the awesomebar autocomplete area.
        new_tab()

        Mouse().move(search_engine_location)

        select_location_bar()

        # Type a partial part of the above address.
        type('127')

        # Type "bug" in the awesomebar to search for the page from step 2 (bookmarked page).
        # Search results are listed.

        search_results_listed = exists(search_results_listed_pattern.similar(0.7), FirefoxSettings.FIREFOX_TIMEOUT)
        assert search_results_listed, 'Search results are listed.'

        # 5. Check the mouse cursor is over any of the search provider icons at the bottom of the results.

        duck_duck_go = exists(duck_duck_go_one_off_button, FirefoxSettings.FIREFOX_TIMEOUT,
                              region=top_two_third_screen_region)
        assert duck_duck_go, 'The \'DuckDuckGo\' one-off button found.'

        # Mouse is over a search engine icon.
        Mouse().move(Location(search_engine_location.x+1, search_engine_location.y+1), duration=0)

        # Press the "↓" key to focus a page result/search suggestion. (e.g. "bugzilla.mozilla.org")

        type(Key.DOWN)

        # The result is focused.
        result_is_focused = exists(result_is_focused_pattern.similar(0.7), FirefoxSettings.FIREFOX_TIMEOUT)
        assert result_is_focused, 'The result is focused.'

        # Press Enter to perform the load of the page.

        type(Key.ENTER)

        # The "bugzilla.mozilla.org" page is loaded.
        # The browser does NOT search for "bug" with the search engine that had the mouse over it.

        firefox_local_page_loaded = exists(LocalWeb.FIREFOX_LOGO, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        iris_local_page_loaded = exists(LocalWeb.IRIS_LOGO, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)

        assert firefox_local_page_loaded or iris_local_page_loaded,\
            'Page successfully is loaded. The browser does NOT search for "bug" with the search engine that had ' \
            'the mouse over it.'

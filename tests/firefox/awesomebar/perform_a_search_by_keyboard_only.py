# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='This test case perform a search by keyboard only.',
        locale=['en-US'],
        test_case_id='108268',
        test_suite_id='1902',
        profile_preferences={'browser.contentblocking.enabled': False}
    )
    def run(self, firefox):
        search_with_google_one_off_string_pattern = Pattern('search_with_Google_one_off_string.png')
        search_with_duckduckgo_one_off_string_pattern = Pattern('search_with_DuckDuckGo_one_off_string.png')
        search_with_amazon_one_off_string_pattern = Pattern('search_with_Amazon_one_off_string.png')
        search_with_bing_one_off_string_pattern = Pattern('search_with_Bing_one_off_string.png')
        search_with_twitter_one_off_string_pattern = Pattern('search_with_Twitter_one_off_string.png')
        search_with_wikipedia_one_off_string_pattern = Pattern('search_with_Wikipedia_one_off_string.png')
        new_tab_twitter_search_results_pattern = Pattern('new_tab_twitter_search_results.png')
        new_tab_twitter_search_results_pattern2 = Pattern('new_tab_twitter_search_results_2.png')
        wikipedia_search_results_moz_pattern = Pattern('wikipedia_search_results_moz.png')
        google_search_results_moz_pattern_pattern = Pattern('google_search_results_moz.png')
        bing_search_results_moz_pattern = Pattern('bing_search_results_moz.png')
        amazon_search_results_moz_pattern = Pattern('amazon_search_results_moz.png')
        duckduckgo_search_results_pattern = Pattern('duckduckgo_search_results.png')
        moz_search_duckduckgo_pattern = Pattern('moz_search_duckduckgo.png')
        moz_search_pattern = Pattern('moz_search.png')

        region = Screen().new_region(0, 0, Screen.SCREEN_WIDTH, 2 * Screen.SCREEN_HEIGHT / 3)

        navigate(LocalWeb.FIREFOX_TEST_SITE)

        expected = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert expected, 'Page successfully loaded, firefox logo found.'

        # Perform a search by keyboard only with 'Google' search engine.
        select_location_bar()

        paste('moz')

        # Wait a moment for the suggests list to fully populate before stepping down through it.
        time.sleep(Settings.DEFAULT_UI_DELAY)

        repeat_key_up(7)
        key_to_one_off_search(search_with_google_one_off_string_pattern)

        expected = region.exists(search_with_google_one_off_string_pattern, 10)
        assert expected, 'The search engine in focus is \'Google\'.'

        type(Key.ENTER)
        time.sleep(Settings.DEFAULT_UI_DELAY_LONG)

        expected = region.exists(google_search_results_moz_pattern_pattern, 10)
        assert expected, 'Search results performed with \'Google\' search engine.'

        close_content_blocking_pop_up()

        expected = region.exists(moz_search_pattern, 10)
        assert expected, 'Searched text successfully found in the loaded page.'

        # Perform a search by keyboard only with 'Bing' search engine.
        new_tab()

        select_location_bar()
        paste('moz')

        # Wait a moment for the suggests list to fully populate before stepping down through it.
        time.sleep(Settings.DEFAULT_UI_DELAY)

        repeat_key_up(6)
        key_to_one_off_search(search_with_bing_one_off_string_pattern)

        expected = exists(search_with_bing_one_off_string_pattern, 5)
        assert expected, 'The search engine in focus is \'Bing\'.'

        type(Key.ENTER)
        time.sleep(Settings.DEFAULT_UI_DELAY_LONG)

        expected = region.exists(bing_search_results_moz_pattern, 10)
        assert expected, 'Search results performed with \'Bing\' search engine.'

        # Perform a search by keyboard only with 'Amazon' search engine.
        new_tab()

        select_location_bar()
        paste('moz')

        # Wait a moment for the suggests list to fully populate before stepping down through it.
        time.sleep(Settings.DEFAULT_UI_DELAY)

        repeat_key_up(5)
        key_to_one_off_search(search_with_amazon_one_off_string_pattern)

        expected = region.exists(search_with_amazon_one_off_string_pattern, 10)
        assert expected, 'The search engine in focus is \'Amazon\'.'

        type(Key.ENTER)
        time.sleep(Settings.DEFAULT_UI_DELAY_LONG)

        expected = region.exists(amazon_search_results_moz_pattern, 10)
        assert expected, 'Search results performed with \'Amazon\' search engine.'

        # Perform a search by keyboard only with 'DuckDuckGo' search engine.
        new_tab()

        select_location_bar()
        paste('moz')

        # Wait a moment for the suggests list to fully populate before stepping down through it.
        time.sleep(Settings.DEFAULT_UI_DELAY)

        repeat_key_up(4)
        key_to_one_off_search(search_with_duckduckgo_one_off_string_pattern)

        expected = region.exists(search_with_duckduckgo_one_off_string_pattern, 10)
        assert expected, 'The search engine in focus is \'DuckDuckGo\'.'

        type(Key.ENTER)
        time.sleep(Settings.DEFAULT_UI_DELAY_LONG)

        expected = region.exists(duckduckgo_search_results_pattern.similar(0.5), 10)
        assert expected, 'Search results performed with \'DuckDuckGo\' search engine.'

        expected = region.exists(moz_search_duckduckgo_pattern, 10)
        assert expected, 'Searched text successfully found in the loaded page.'

        # Perform a search by keyboard only with 'eBay' search engine.
        new_tab()

        select_location_bar()
        paste('moz')

        # Perform a search by keyboard only with 'Twitter' search engine.
        new_tab()

        select_location_bar()
        paste('moz')

        # Wait a moment for the suggests list to fully populate before stepping down through it.
        time.sleep(Settings.DEFAULT_UI_DELAY)

        repeat_key_up(3)
        key_to_one_off_search(search_with_twitter_one_off_string_pattern)

        expected = region.exists(search_with_twitter_one_off_string_pattern, 10)
        assert expected, 'The search engine in focus is \'Twitter\'.'

        type(Key.ENTER)
        time.sleep(Settings.DEFAULT_UI_DELAY_LONG)

        expected = region.exists(new_tab_twitter_search_results_pattern, 10) \
            or exists(new_tab_twitter_search_results_pattern2, 5)
        assert expected, 'Search results performed with \'Twitter\' search engine.'

        # Perform a search by keyboard only with 'Wikipedia' search engine.
        new_tab()

        select_location_bar()
        paste('moz')

        # Wait a moment for the suggests list to fully populate before stepping down through it.
        time.sleep(Settings.DEFAULT_UI_DELAY)

        repeat_key_up(2)
        key_to_one_off_search(search_with_wikipedia_one_off_string_pattern)

        expected = region.exists(search_with_wikipedia_one_off_string_pattern, 10)
        assert expected, 'The search engine in focus is \'Wikipedia\'.'

        type(Key.ENTER)
        time.sleep(Settings.DEFAULT_UI_DELAY_LONG)

        expected = region.exists(wikipedia_search_results_moz_pattern.similar(0.7), 10)
        assert expected, 'Search results performed with \'Wikipedia\' search engine.'

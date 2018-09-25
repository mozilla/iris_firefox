# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This test case perform a search by keyboard only.'
        self.test_case_id = '108268'
        self.test_suite_id = '1902'

    def run(self):
        url = LocalWeb.FIREFOX_TEST_SITE
        search_with_google_one_off_string_pattern = Pattern('search_with_Google_one_off_string.png')
        search_with_duckduckgo_one_off_string_pattern = Pattern('search_with_DuckDuckGo_one_off_string.png')
        search_with_amazon_one_off_string_pattern = Pattern('search_with_Amazon_one_off_string.png')
        search_with_bing_one_off_string_pattern = Pattern('search_with_Bing_one_off_string.png')
        search_with_ebay_one_off_string_pattern = Pattern('search_with_eBay_one_off_string.png')
        search_with_twitter_one_off_string_pattern = Pattern('search_with_Twitter_one_off_string.png')
        search_with_wikipedia_one_off_string_pattern = Pattern('search_with_Wikipedia_one_off_string.png')
        new_tab_twitter_search_results_pattern = Pattern('new_tab_twitter_search_results.png')
        wikipedia_search_results_moz_pattern = Pattern('wikipedia_search_results_moz.png')
        google_search_results_moz_pattern_pattern = Pattern('google_search_results_moz.png')
        bing_search_results_moz_pattern = Pattern('bing_search_results_moz.png')
        amazon_search_results_moz_pattern = Pattern('amazon_search_results_moz.png')
        duckduckgo_search_results_pattern = Pattern('duckduckgo_search_results.png')
        ebay_search_results_moz_pattern = Pattern('ebay_search_results_moz.png')
        moz_search_duckduckgo_pattern = Pattern('moz_search_duckduckgo.png')
        moz_search_pattern = Pattern('moz_search.png')

        region = Region(0, 0, SCREEN_WIDTH, 2 * SCREEN_HEIGHT / 3)

        navigate(url)
        expected = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert_true(self, expected, 'Page successfully loaded, firefox logo found.')

        # Perform a search by keyboard only with 'Google' search engine.
        select_location_bar()

        paste('moz')

        # Wait a moment for the suggests list to fully populate before stepping down through it.
        time.sleep(Settings.UI_DELAY)

        # The search suggestion list has 10 suggestions by default.
        for i in range(10):
            type(Key.DOWN)

        expected = region.exists(search_with_google_one_off_string_pattern, 10)
        assert_true(self, expected, 'The search engine in focus is \'Google\'.')

        type(Key.ENTER)
        time.sleep(DEFAULT_UI_DELAY_LONG)

        expected = region.exists(google_search_results_moz_pattern_pattern, 10)
        assert_true(self, expected, 'Search results performed with \'Google\' search engine.')

        expected = region.exists(moz_search_pattern, 10)
        assert_true(self, expected, 'Searched text successfully found in the loaded page.')

        # Perform a search by keyboard only with 'Bing' search engine.
        new_tab()

        select_location_bar()
        paste('moz')

        # Wait a moment for the suggests list to fully populate before stepping down through it.
        time.sleep(Settings.UI_DELAY)

        # The search suggestion list has 10 suggestions by default.
        for i in range(11):
            type(Key.DOWN)

        expected = region.exists(search_with_bing_one_off_string_pattern, 10)
        assert_true(self, expected, 'The search engine in focus is \'Bing\'.')

        type(Key.ENTER)
        time.sleep(DEFAULT_UI_DELAY_LONG)

        expected = region.exists(bing_search_results_moz_pattern, 10)
        assert_true(self, expected, 'Search results performed with \'Bing\' search engine.')

        # Perform a search by keyboard only with 'Amazon' search engine.
        new_tab()

        select_location_bar()
        paste('moz')

        # Wait a moment for the suggests list to fully populate before stepping down through it.
        time.sleep(Settings.UI_DELAY)

        # The search suggestion list has 10 suggestions by default.
        for i in range(12):
            type(Key.DOWN)

        expected = region.exists(search_with_amazon_one_off_string_pattern, 10)
        assert_true(self, expected, 'The search engine in focus is \'Amazon\'.')

        type(Key.ENTER)
        time.sleep(DEFAULT_UI_DELAY_LONG)

        expected = region.exists(amazon_search_results_moz_pattern, 10)
        assert_true(self, expected, 'Search results performed with \'Amazon\' search engine.')

        # Perform a search by keyboard only with 'DuckDuckGo' search engine.
        new_tab()

        select_location_bar()
        paste('moz')

        # Wait a moment for the suggests list to fully populate before stepping down through it.
        time.sleep(Settings.UI_DELAY)

        # The search suggestion list has 10 suggestions by default.
        for i in range(13):
            type(Key.DOWN)

        expected = region.exists(search_with_duckduckgo_one_off_string_pattern, 10)
        assert_true(self, expected, 'The search engine in focus is \'DuckDuckGo\'.')

        type(Key.ENTER)
        time.sleep(DEFAULT_UI_DELAY_LONG)

        expected = region.exists(duckduckgo_search_results_pattern.similar(0.6), 10)
        assert_true(self, expected, 'Search results performed with \'DuckDuckGo\' search engine.')

        expected = region.exists(moz_search_duckduckgo_pattern, 10)
        assert_true(self, expected, 'Searched text successfully found in the loaded page.')

        # Perform a search by keyboard only with 'eBay' search engine.
        new_tab()

        select_location_bar()
        paste('moz')

        # Wait a moment for the suggests list to fully populate before stepping down through it.
        time.sleep(Settings.UI_DELAY)

        # The search suggestion list has 10 suggestions by default.
        for i in range(14):
            type(Key.DOWN)

        expected = region.exists(search_with_ebay_one_off_string_pattern, 10)
        assert_true(self, expected, 'The search engine in focus is \'eBay\'.')

        type(Key.ENTER)
        time.sleep(DEFAULT_UI_DELAY_LONG)

        expected = region.exists(ebay_search_results_moz_pattern, 10)
        assert_true(self, expected, 'Search results performed with \'eBay\' search engine.')

        # Perform a search by keyboard only with 'Twitter' search engine.
        new_tab()

        select_location_bar()
        paste('moz')

        # Wait a moment for the suggests list to fully populate before stepping down through it.
        time.sleep(Settings.UI_DELAY)

        # The search suggestion list has 10 suggestions by default.
        for i in range(15):
            type(Key.DOWN)

        expected = region.exists(search_with_twitter_one_off_string_pattern, 10)
        assert_true(self, expected, 'The search engine in focus is \'Twitter\'.')

        type(Key.ENTER)
        time.sleep(DEFAULT_UI_DELAY_LONG)

        expected = region.exists(new_tab_twitter_search_results_pattern, 10)
        assert_true(self, expected, 'Search results performed with \'Twitter\' search engine.')

        # Perform a search by keyboard only with 'Wikipedia' search engine.
        new_tab()

        select_location_bar()
        paste('moz')

        # Wait a moment for the suggests list to fully populate before stepping down through it.
        time.sleep(Settings.UI_DELAY)

        # The search suggestion list has 10 suggestions by default.
        for i in range(16):
            type(Key.DOWN)

        expected = region.exists(search_with_wikipedia_one_off_string_pattern, 10)
        assert_true(self, expected, 'The search engine in focus is \'Wikipedia\'.')

        type(Key.ENTER)
        time.sleep(DEFAULT_UI_DELAY_LONG)

        expected = region.exists(wikipedia_search_results_moz_pattern.similar(0.7), 10)
        assert_true(self, expected, 'Search results performed with \'Wikipedia\' search engine.')

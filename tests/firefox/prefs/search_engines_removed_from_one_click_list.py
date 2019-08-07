# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Search Engines can be successfully removed from the "One-Click Search Engines" list',
        test_case_id='143595',
        test_suite_id='2241',
        locale=['en-US'],
    )
    def run(self, firefox):
        preferences_search_pattern = AboutPreferences.ABOUT_PREFERENCE_SEARCH_PAGE_PATTERN
        find_more_search_engines_pattern = Pattern('find_more_search_engines.png')
        google_one_click_search_pattern = Pattern('google_one_click_search.png')
        bing_one_click_search_pattern = Pattern('bing_one_click_search.png')
        amazon_one_click_search_pattern = Pattern('amazon_one_click_search.png')
        duck_one_click_search_pattern = Pattern('duck_one_click_search.png')
        ebay_one_click_search_pattern = Pattern('ebay_one_click_search.png')
        twitter_one_click_search_pattern = Pattern('twitter_one_click_search.png')
        wiki_one_click_search_pattern = Pattern('wiki_one_click_search.png')

        navigate('about:preferences#search')

        assert exists(preferences_search_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT), \
            'The about:preferences page is successfully loaded.'

        hover(Location(Screen.SCREEN_WIDTH // 2, Screen.SCREEN_HEIGHT // 2))

        search_engines_list = scroll_until_pattern_found(find_more_search_engines_pattern, scroll, (-25,), 20, 1)

        assert search_engines_list, 'The "One-click Search Engines" is available.'

        # All the search engines are displayed with their corresponding icon.
        assert exists(google_one_click_search_pattern, region=Screen.LEFT_HALF), \
            'Google is in the "One-click Search Engines" list'
        assert exists(bing_one_click_search_pattern, region=Screen.LEFT_HALF), \
            'Bing is in the "One-click Search Engines" list'
        assert exists(amazon_one_click_search_pattern, region=Screen.LEFT_HALF), \
            'Amazon is in the "One-click Search Engines" list'
        assert exists(duck_one_click_search_pattern, region=Screen.LEFT_HALF), \
            'DuckDuckGo is in the "One-click Search Engines" list'
        assert exists(ebay_one_click_search_pattern, region=Screen.LEFT_HALF), \
            'Ebay is in the "One-click Search Engines" list'
        assert exists(twitter_one_click_search_pattern, region=Screen.LEFT_HALF), \
            'Twitter is in the "One-click Search Engines" list'
        assert exists(wiki_one_click_search_pattern, region=Screen.LEFT_HALF), \
            'Wikipedia is in the "One-click Search Engines" list'

        click(bing_one_click_search_pattern, 1)

        assert exists('Remove', FirefoxSettings.FIREFOX_TIMEOUT, Screen.BOTTOM_THIRD), 'Remove button available.'

        click('Remove', region=Screen.BOTTOM_THIRD)

        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)  # wait until Bing removes

        # The selected search engines are not displayed anymore.
        assert not exists(bing_one_click_search_pattern, region=Screen.LEFT_HALF), \
            'Bing is not displayed anymore in the "One-click Search Engines" list'

        # At the bottom of the dropdown, the deleted search engine is not listed among the others.
        new_tab()

        select_search_bar()

        paste('test search')

        # Wait for correct pattern to search
        time.sleep(FirefoxSettings.SHORT_FIREFOX_TIMEOUT)

        assert not exists(bing_one_click_search_pattern, FirefoxSettings.FIREFOX_TIMEOUT, region=Screen.LEFT_HALF), \
            'At the bottom of the dropdown, the deleted search engine is not listed among the others.'

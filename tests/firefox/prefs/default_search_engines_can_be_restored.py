# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Default Search Engines can be successfully restored',
        test_case_id='143596',
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
        remove_search_system_pattern = Pattern('remove_search_system.png')
        time.sleep(5)

        navigate('about:preferences#search')

        preferences_search = exists(preferences_search_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert preferences_search, 'The about:preferences page is successfully loaded.'

        hover(Location(Screen.SCREEN_WIDTH // 2, Screen.SCREEN_HEIGHT // 2))

        search_engines_list = scroll_until_pattern_found(find_more_search_engines_pattern, scroll, (-25,), 20, 1)

        assert search_engines_list, 'The "One-click Search Engines" is available.'

        # All the search engines are displayed with their corresponding icon.
        google_one_click_search = exists(google_one_click_search_pattern, region=Screen.LEFT_HALF)
        assert google_one_click_search, 'Google is in the "One-click Search Engines" list'

        bing_one_click_search = exists(bing_one_click_search_pattern, region=Screen.LEFT_HALF)
        assert bing_one_click_search, 'Bing is in the "One-click Search Engines" list'

        amazon_one_click_search = exists(amazon_one_click_search_pattern, region=Screen.LEFT_HALF)
        assert amazon_one_click_search, 'Amazon is in the "One-click Search Engines" list'

        duck_one_click_search = exists(duck_one_click_search_pattern, region=Screen.LEFT_HALF)
        assert duck_one_click_search, 'DuckDuckGo is in the "One-click Search Engines" list'

        ebay_one_click_search = exists(ebay_one_click_search_pattern, region=Screen.LEFT_HALF)
        assert ebay_one_click_search, 'Ebay is in the "One-click Search Engines" list'

        twitter_one_click_search = exists(twitter_one_click_search_pattern, region=Screen.LEFT_HALF)
        assert twitter_one_click_search, 'Twitter is in the "One-click Search Engines" list'

        wiki_one_click_search = exists(wiki_one_click_search_pattern, region=Screen.LEFT_HALF)
        assert wiki_one_click_search, 'Wikipedia is in the "One-click Search Engines" list'

        click(bing_one_click_search_pattern, 1)

        time.sleep(FirefoxSettings.SHORT_FIREFOX_TIMEOUT)  # wait for load of active button Remove

        bottom_region = Screen.BOTTOM_HALF

        remove_available = exists(remove_search_system_pattern, FirefoxSettings.FIREFOX_TIMEOUT, bottom_region)
        assert remove_available, 'Remove button available.'

        click(remove_search_system_pattern, region=bottom_region)

        time.sleep(FirefoxSettings.SHORT_FIREFOX_TIMEOUT)  # wait until search engine actually removes

        # The selected search engines are not displayed anymore.
        bing_one_click_search = exists(bing_one_click_search_pattern, region=Screen.LEFT_HALF)
        assert not bing_one_click_search, 'Bing is not displayed anymore in the "One-click Search Engines" list'

        # The "Restore Default Search Engines" button is enabled.
        restore_default = exists('Restore Default Search Engines', FirefoxSettings.FIREFOX_TIMEOUT, Screen.BOTTOM_THIRD)
        assert restore_default,'"Restore Default Search Engines" remove button available.'

        click('Restore Default Search Engines', region=Screen.BOTTOM_THIRD)

        # The previously deleted search engines are listed again.
        bing_one_click_search = exists(bing_one_click_search_pattern, region=Screen.LEFT_HALF)
        assert bing_one_click_search, 'Bing is not displayed anymore in the "One-click Search Engines" list'

        # The previously deleted search engines are listed on the bottom of the doorhanger.
        new_tab()

        select_search_bar()

        paste('test search')

        # Wait for correct pattern to search
        time.sleep(FirefoxSettings.SHORT_FIREFOX_TIMEOUT)

        bing_one_click_search = exists(bing_one_click_search_pattern, FirefoxSettings.FIREFOX_TIMEOUT,
                                       region=Screen.LEFT_HALF)
        assert bing_one_click_search, 'At the bottom of the dropdown, the deleted search engine is not listed ' \
                                      'among the others.'

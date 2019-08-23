# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='All the keyboard shortcuts available for the Search Bar are working properly.',
        locale=['en-US'],
        test_case_id='4278',
        test_suite_id='83',
    )
    def run(self, firefox):
        search_using_google_pattern = Pattern('search_using_google.png')
        duckduckgo_search_bar_pattern = Pattern('duckduckgo_search_bar.png').similar(.6)
        search_duckduckgo_pattern = Pattern('search_duckduckgo.png')
        bing_search_engine_pattern = Pattern('bing_search_engine.png')
        google_search_engine_pattern = Pattern('google_search_engine.png')

        # Enable the search bar.
        change_preference('browser.search.widget.inNavBar', True)

        search_bar_displayed = exists(LocationBar.SEARCH_BAR_MAGNIFYING_GLASS, FirefoxSettings.FIREFOX_TIMEOUT)
        assert search_bar_displayed, 'Search bar is displayed'

        search_bar_location = find(LocationBar.SEARCH_BAR_MAGNIFYING_GLASS)
        search_bar_width, search_bar_height = LocationBar.SEARCH_BAR_MAGNIFYING_GLASS.get_size()
        search_bar_region = Region(search_bar_location.x, search_bar_location.y, search_bar_width * 3,
                                   search_bar_height * 10)

        # Press ctrl/cmd + k keys.
        select_search_bar()

        # Hover the mouse over the Search Bar.
        Mouse().move(search_bar_location.offset(search_bar_width, search_bar_height//2))

        search_using_google = exists(search_using_google_pattern, FirefoxSettings.FIREFOX_TIMEOUT, search_bar_region)
        assert search_using_google is True, '\'Search using Google\' is shown as tooltip.'

        # Start typing inside the Search Bar.
        type('mozilla')

        # Hover the mouse over the one-click search engines.
        duckduckgo_search_bar = exists(duckduckgo_search_bar_pattern, FirefoxSettings.FIREFOX_TIMEOUT,
                                       search_bar_region)
        assert duckduckgo_search_bar is True, 'Search engine is visible.'

        hover(duckduckgo_search_bar_pattern)

        search_duckduckgo = exists(search_duckduckgo_pattern, FirefoxSettings.FIREFOX_TIMEOUT, search_bar_region)
        assert search_duckduckgo is True, 'Search engine is highlighted.'

        # While the cursor is on the search toolbar, select the arrow DOWN and then the arrow UP keys.
        type(Key.DOWN)

        searchbar_text = copy_to_clipboard()
        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT/2)
        assert searchbar_text == 'mozilla', 'Pressing the arrow DOWN key will slide in the search menu.'

        type(Key.DOWN)

        searchbar_text = copy_to_clipboard()
        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT/2)
        assert searchbar_text != 'mozilla', 'Pressing the arrow DOWN key will slide in the search menu.'

        type(Key.UP)

        searchbar_text = copy_to_clipboard()
        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT/2)
        assert searchbar_text == 'mozilla', 'Pressing the arrow UP key will slide in the search menu.'

        # Use the tab key to navigate.
        select_search_bar()

        for _ in range(3):
            type(Key.TAB)

        search_duckduckgo = exists(search_duckduckgo_pattern, FirefoxSettings.FIREFOX_TIMEOUT, search_bar_region)
        assert search_duckduckgo is True, 'Pressing tab selects the one-click search engines while the search ' \
                                          'suggestions are skipped.'

        # Select ctrl/cmd + arrow UP and arrow DOWN keys.
        change_search_next()

        bing_search_engine = exists(bing_search_engine_pattern, FirefoxSettings.FIREFOX_TIMEOUT, search_bar_region)
        assert bing_search_engine is True, 'The default search engine becomes the next one from the list.'

        change_search_previous()

        google_search_engine = exists(google_search_engine_pattern, FirefoxSettings.FIREFOX_TIMEOUT, search_bar_region)
        assert google_search_engine is True, 'The default search engine becomes the previous one from the list.'

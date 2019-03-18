# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'All the keyboard shortcuts available for the Search Bar are working properly.'
        self.test_case_id = '4278'
        self.test_suite_id = '83'
        self.locale = ['en-US']

    def run(self):
        search_bar_pattern = Pattern('search_bar.png').similar(0.6)
        search_using_google_pattern = Pattern('search_using_google.png')
        duckduckgo_search_bar_pattern = Pattern('duckduckgo_search_bar.png')
        search_duckduckgo_pattern = Pattern('search_duckduckgo.png')
        bing_search_engine_pattern = Pattern('bing_search_engine.png')
        google_search_engine_pattern = Pattern('google_search_engine.png')

        # Enable the search bar.
        change_preference('browser.search.widget.inNavBar', True)

        # Press ctrl/cmd + k keys.
        select_search_bar()

        # Hover the mouse over the Search Bar.
        hover(search_bar_pattern)
        expected = exists(search_using_google_pattern, 10)
        assert_true(self, expected, '\'Search using Google\' is shown as tooltip.')

        # Start typing inside the Search Bar.
        type('mozilla')

        # Hover the mouse over the one-click search engines.
        expected = exists(duckduckgo_search_bar_pattern, 10)
        assert_true(self, expected, 'Search engine is visible.')

        hover(duckduckgo_search_bar_pattern)
        expected = exists(search_duckduckgo_pattern, 10)
        assert_true(self, expected, 'Search engine is highlighted.')

        # While the cursor is on the search toolbar, select the arrow DOWN and then the arrow UP keys.
        type(Key.DOWN)
        searchbar_text = copy_to_clipboard()
        assert_equal(self, searchbar_text, 'mozilla', 'Pressing the arrow DOWN key will slide in the search menu.')

        type(Key.DOWN)
        searchbar_text = copy_to_clipboard()
        assert_not_equal(self, searchbar_text, 'mozilla', 'Pressing the arrow DOWN key will slide in the search menu.')

        type(Key.UP)
        searchbar_text = copy_to_clipboard()
        assert_equal(self, searchbar_text, 'mozilla', 'Pressing the arrow UP key will slide in the search menu.')

        # Use the tab key to navigate.
        select_search_bar()

        for i in range(3):
            type(Key.TAB)

        expected = exists(search_duckduckgo_pattern, 10)
        assert_true(self, expected,
                    'Pressing tab selects the one-click search engines while the search suggestions are skipped.')

        # Select ctrl/cmd + arrow UP and arrow DOWN keys.
        change_search_next()
        expected = exists(bing_search_engine_pattern, 10)
        assert_true(self, expected, 'The default search engine becomes the next one from the list.')

        change_search_previous()
        expected = exists(google_search_engine_pattern, 10)
        assert_true(self, expected, 'The default search engine becomes the previous one from the list.')

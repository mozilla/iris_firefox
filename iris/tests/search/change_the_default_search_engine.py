# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Changing the default search engine from Search bar does not work first time.'
        self.test_case_id = '111384'
        self.test_suite_id = '83'
        self.locale = ['en-US']

    def run(self):
        bing_search_bar_pattern = Pattern('bing_search_bar.png')
        search_in_new_tab_pattern = Pattern('search_in_new_tab.png')
        set_as_default_search_engine_pattern = Pattern('set_as_default_search_engine.png')
        bing_search_engine_pattern = Pattern('bing_search_engine.png')
        test_search_bing_pattern = Pattern('test_search_bing.png')

        # Enable the search bar.
        change_preference('browser.search.widget.inNavBar', True)

        select_search_bar()
        paste('test')

        expected = exists(bing_search_bar_pattern, 10)
        assert_true(self, expected, 'Wikipedia search engine is successfully displayed.')

        right_click(bing_search_bar_pattern)

        expected = exists(search_in_new_tab_pattern, 10)
        assert_true(self, expected, 'The \'Search in New Tab\' option found.')

        expected = exists(set_as_default_search_engine_pattern, 10)
        assert_true(self, expected, 'The \'Set As Default Search Engine\' option found.')

        click(set_as_default_search_engine_pattern)
        time.sleep(DEFAULT_UI_DELAY_LONG)

        expected = exists(bing_search_engine_pattern, 10)
        assert_true(self, expected, 'The selected search engine is properly set as a new default search engine.')

        type(Key.ENTER)

        expected = exists(test_search_bing_pattern, 10)
        assert_true(self, expected, 'The search is performed using the newly added search engine.')

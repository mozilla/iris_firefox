# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Search Code Testing: DuckDuckGo - US.'
        self.test_case_id = '218335'
        self.test_suite_id = '83'
        self.locale = ['en-US']

    def run(self):
        default_search_engine_google_pattern = Pattern('default_search_engine_google.png')
        default_search_engine_dropdown_pattern = Pattern('default_search_engine_dropdown.png')
        test_search_duckduckgo_pattern = Pattern('test_search_duckduckgo.png')

        change_preference('browser.search.widget.inNavBar', True)

        navigate('about:preferences#search')
        expected = exists(default_search_engine_google_pattern, 10)
        assert_true(self, expected, 'Google is the default search engine.')

        # Change the default search engine to DuckDuckGo.
        click(default_search_engine_dropdown_pattern)
        repeat_key_down(3)
        type(Key.ENTER)

        select_location_bar()
        paste('test')
        type(Key.ENTER)

        expected = exists(test_search_duckduckgo_pattern, 10)
        assert_true(self, expected, 'The search is performed with the DuckDuckGo engine.')
        time.sleep(DEFAULT_UI_DELAY_LONG)

        select_location_bar()
        url_text = copy_to_clipboard()

        assert_contains(self, url_text, 't=ffab', 'The resulted URL contains the \'t=ffab\' string.')

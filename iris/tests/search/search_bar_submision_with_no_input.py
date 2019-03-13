# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'The Search Bar accepts submission with no input.'
        self.test_case_id = '4263'
        self.test_suite_id = '83'
        self.locale = ['en-US']

    def run(self):
        add_search_bar_in_toolbar_pattern = Pattern('add_search_bar_in_toolbar.png')
        search_bar_pattern = Pattern('search_bar.png')
        google_search_no_input_pattern = Pattern('google_search_no_input.png')

        navigate('about:preferences#search')
        expected = exists(add_search_bar_in_toolbar_pattern, 10)
        assert_true(self, expected, 'Option found in the page.')

        click(add_search_bar_in_toolbar_pattern)

        expected = exists(search_bar_pattern, 10)
        assert_true(self, expected, 'Search bar successfully enabled in the page.')

        click(search_bar_pattern)
        time.sleep(DEFAULT_UI_DELAY)

        type(Key.ENTER)
        expected = exists(google_search_no_input_pattern, 10)
        assert_true(self, expected, 'The search engine page is opened with no searches performed.')

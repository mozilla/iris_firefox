# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'The Search Bar provides valid results for specific search terms.'
        self.test_case_id = '4264'
        self.test_suite_id = '83'
        self.locale = ['en-US']

    def run(self):
        search_button_pattern = Pattern('search_button.png')
        test_pattern = Pattern('test.png')

        change_preference('browser.search.widget.inNavBar', True)

        select_search_bar()
        paste('test')

        region = Screen.UPPER_RIGHT_CORNER
        expected = region.exists(search_button_pattern, 10)
        assert_true(self, expected, 'Search button found in the page.')

        region.click(search_button_pattern)

        region = Screen.UPPER_LEFT_CORNER
        expected = region.exists(test_pattern, 10)
        assert_true(self, expected, 'The search engine page is opened with the search results for that term.')

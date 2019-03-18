# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Awesomebar results don\'t show the correct search engine when searching with search engine ' \
                    'keywords.'
        self.test_case_id = '111378'
        self.test_suite_id = '83'
        self.locale = ['en-US']

    def run(self):
        about_preferences_search_page_pattern = Pattern('about_preferences_search_page.png')
        keyword_field_pattern = Pattern('keyword_field.png')
        moz_search_bing_pattern = Pattern('moz_search_bing.png')

        navigate('about:preferences#search')

        expected = exists(about_preferences_search_page_pattern, 10)
        assert_true(self, expected, 'The \'about:preferences#search\' page successfully loaded.')

        paste('keyword')

        expected = exists(keyword_field_pattern, 10)
        assert_true(self, expected, 'The keyword field is visible.')

        double_click(keyword_field_pattern)
        paste('bn')
        time.sleep(DEFAULT_UI_DELAY_LONG)
        select_location_bar()
        paste('bn moz')

        expected = exists(moz_search_bing_pattern, 10)
        assert_true(self, expected, 'Results from URL bar state that the search will be performed with \'Bing\'.')

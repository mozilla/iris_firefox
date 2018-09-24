# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This test case checks that telemetry data is collected for one-offs from new tab.'
        self.test_case_id = '108274'
        self.test_suite_id = '1902'

    def run(self):
        url = LocalWeb.FIREFOX_TEST_SITE
        bing_search_results_moz_pattern = Pattern('bing_search_results_moz.png')

        navigate(url)
        expected = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert_true(self, expected, 'Page successfully loaded, firefox logo found.')

        new_tab()
        select_location_bar()

        # Tab 3 times to move focus on the search bar in the center of the page.
        type(Key.TAB)
        type(Key.TAB)
        type(Key.TAB)

        paste('moz')

        # Wait a moment for the suggests list to fully populate before stepping down through it.
        time.sleep(Settings.UI_DELAY)

        for i in range(7):
            scroll_down()
        type(Key.ENTER)

        time.sleep(DEFAULT_UI_DELAY_LONG)

        expected = exists(bing_search_results_moz_pattern, 10)
        assert_true(self, expected, 'Search results performed with \'Bing\' search engine.')

        info = get_telemetry_info()['payload']['keyedHistograms']['SEARCH_COUNTS']

        assert_equal(self, str(info['bing.newtab']['range']), '[1, 2]', 'Range is correct.')
        assert_equal(self, str(info['bing.newtab']['bucket_count']), '3', 'Bucket count is correct.')
        assert_equal(self, str(info['bing.newtab']['histogram_type']), '4', 'Histogram type is correct.')
        assert_equal(self, str(info['bing.newtab']['values']), "{u'1': 0, u'0': 1}", 'Values are correct.')
        assert_equal(self, str(info['bing.newtab']['sum']), '1', 'Sum is correct.')

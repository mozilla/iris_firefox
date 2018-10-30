# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'This test case disables one-off searches from the awesomebar.'
        self.test_case_id = '108258'
        self.test_suite_id = '1902'
        self.locales = ['en-US']

    def run(self):
        default_status_pattern = Pattern('default_status.png')
        modified_status_pattern = Pattern('modified_status.png')
        true_value_pattern = Pattern('true_value.png')
        false_value_pattern = Pattern('false_value.png')
        accept_risk_pattern = Pattern('accept_risk.png')
        search_settings_pattern = Pattern('search_settings.png')
        amazon_one_off_button_pattern = Pattern('amazon_one_off_button.png')
        bing_one_off_button_pattern = Pattern('bing_one_off_button.png')
        duck_duck_go_one_off_button_pattern = Pattern('duck_duck_go_one_off_button.png')
        ebay_one_off_button_pattern = Pattern('ebay_one_off_button.png')
        google_one_off_button_pattern = Pattern('google_one_off_button.png')
        twitter_one_off_button_pattern = Pattern('twitter_one_off_button.png')
        wikipedia_one_off_button_pattern = Pattern('wikipedia_one_off_button.png')
        google_search_results_pattern = Pattern('google_search_results.png')
        moz_pattern = Pattern('moz.png')

        region = Region(0, 0, SCREEN_WIDTH, 2 * SCREEN_HEIGHT / 3)

        navigate('about:config')
        click(accept_risk_pattern)

        expected = region.exists(default_status_pattern, 10)
        assert_true(self, expected, 'The \'about:config\' page successfully loaded and default status is correct.')

        paste('browser.urlbar.oneOffSearches')
        type(Key.ENTER)

        expected = region.exists(default_status_pattern, 10)
        assert_true(self, expected,
                    'The \'browser.urlbar.oneOffSearches\' preference has status \'default\' by default.')

        expected = region.exists(true_value_pattern, 10)
        assert_true(self, expected, 'The \'browser.urlbar.oneOffSearches\' preference has value \'true\' by default.')

        double_click(default_status_pattern)

        expected = region.exists(modified_status_pattern, 10)
        assert_true(self, expected, 'The \'browser.urlbar.oneOffSearches\' preference has status \'modified\' after '
                                    'the preference has changed.')

        expected = region.exists(false_value_pattern, 10)
        assert_true(self, expected, 'The \'browser.urlbar.oneOffSearches\' preference has value \'false\' after the '
                                    'preference has changed.')

        select_location_bar()
        paste('moz')

        pattern_list = [moz_pattern, search_settings_pattern, amazon_one_off_button_pattern,
                        bing_one_off_button_pattern, duck_duck_go_one_off_button_pattern, ebay_one_off_button_pattern,
                        google_one_off_button_pattern, twitter_one_off_button_pattern, wikipedia_one_off_button_pattern]

        # Check that the one-off list is not displayed in the awesomebar after the 'browser.urlbar.oneOffSearches'
        # preference is set to 'false'.
        for i in range(pattern_list.__len__()):
            try:
                expected = wait_vanish(pattern_list[i].similar(0.9), 10)
                assert_true(self, expected, 'Element found at position ' + i.__str__() + ' in the list not found.')
            except FindError:
                raise FindError('Element found at position ' + i.__str__() + ' in the list found.')

        select_location_bar()
        paste('moz')
        type(Key.ENTER)

        time.sleep(DEFAULT_UI_DELAY_LONG)

        expected = region.exists(google_search_results_pattern, 10)
        assert_true(self, expected, 'The search is made using the default search engine which is Google.')

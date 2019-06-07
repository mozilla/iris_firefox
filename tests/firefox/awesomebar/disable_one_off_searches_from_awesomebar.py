# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='This test case disables one-off searches from the awesomebar.',
        locale=['en-US'],
        test_case_id='108258',
        test_suite_id='1902'
    )
    def run(self, firefox):
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

        region = Screen().new_region(0, 0, Screen.SCREEN_WIDTH, 2 * Screen.SCREEN_HEIGHT / 3)

        navigate('about:config')
        click(accept_risk_pattern)

        expected = region.exists(default_status_pattern, 10)
        assert expected, 'The \'about:config\' page successfully loaded and default status is correct.'

        paste('browser.urlbar.oneOffSearches')
        type(Key.ENTER)

        expected = region.exists(default_status_pattern, 10)
        assert expected, 'The \'browser.urlbar.oneOffSearches\' preference has status \'default\' by default.'

        expected = region.exists(true_value_pattern, 10)
        assert expected, 'The \'browser.urlbar.oneOffSearches\' preference has value \'true\' by default.'

        double_click(default_status_pattern)

        expected = region.exists(modified_status_pattern, 10)
        assert expected, 'The \'browser.urlbar.oneOffSearches\' preference has status \'modified\' after ' \
                         'the preference has changed.'

        expected = region.exists(false_value_pattern, 10)
        assert expected, 'The \'browser.urlbar.oneOffSearches\' preference has value \'false\' after the ' \
                         'preference has changed.'

        select_location_bar()
        paste('moz')

        pattern_list = [moz_pattern, search_settings_pattern, amazon_one_off_button_pattern,
                        bing_one_off_button_pattern, duck_duck_go_one_off_button_pattern, ebay_one_off_button_pattern,
                        google_one_off_button_pattern, twitter_one_off_button_pattern, wikipedia_one_off_button_pattern]

        for index, pattern in enumerate(pattern_list):
            try:
                expected = wait_vanish(pattern.similar(0.9), 2)
                assert expected, 'Element found at position {} in the list not found.'.format(index)
            except FindError:
                raise FindError('Element found at position {} in the list found.'.format(index))

        select_location_bar()
        paste('moz')
        type(Key.ENTER)

        time.sleep(Settings.DEFAULT_UI_DELAY_LONG)

        expected = region.exists(google_search_results_pattern, 10)
        assert expected, 'The search is made using the default search engine which is Google.'

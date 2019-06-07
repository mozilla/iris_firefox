# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='This test case checks the one-off search bar and the Settings gear after removing checks for ' 
                    'each search engine from the Search Settings.',
        locale=['en-US'],
        test_case_id='108259',
        test_suite_id='1902'
    )
    def run(self, firefox):
        moz_pattern = Pattern('moz.png')
        search_engine_pattern = Pattern('search_engine.png')
        check_engine_pattern = Pattern('check_engine.png')
        search_settings_pattern = Pattern('search_settings.png')
        amazon_one_off_button_pattern = Pattern('amazon_one_off_button.png')
        bing_one_off_button_pattern = Pattern('bing_one_off_button.png')
        duck_duck_go_one_off_button_pattern = Pattern('duck_duck_go_one_off_button.png')
        google_one_off_button_pattern = Pattern('google_one_off_button.png')
        twitter_one_off_button_pattern = Pattern('twitter_one_off_button.png')
        wikipedia_one_off_button_pattern = Pattern('wikipedia_one_off_button.png')
        about_preferences_search_page_pattern = Pattern('about_preferences_search_page.png')

        region = Screen().new_region(0, 0, Screen.SCREEN_WIDTH, 2 * Screen.SCREEN_HEIGHT / 3)

        navigate(LocalWeb.FIREFOX_TEST_SITE)

        expected = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert expected, 'Page successfully loaded, firefox logo found.'

        select_location_bar()
        paste('moz')

        pattern_list = [moz_pattern, search_settings_pattern, amazon_one_off_button_pattern,
                        bing_one_off_button_pattern, duck_duck_go_one_off_button_pattern, google_one_off_button_pattern,
                        twitter_one_off_button_pattern, wikipedia_one_off_button_pattern]

        for index, pattern in enumerate(pattern_list):
            if OSHelper.is_mac():
                expected = region.exists(pattern.similar(0.7), 10)
                assert expected, 'Element found at position {} in the list found.'.format(index)
            else:
                expected = region.exists(pattern.similar(0.8), 10)
                assert expected, 'Element found at position {} in the list found.'.format(index)

        click(search_settings_pattern)
        time.sleep(Settings.DEFAULT_UI_DELAY)

        expected = exists(about_preferences_search_page_pattern, 10)
        assert expected, 'The \'about:preferences#search\' page successfully loaded.'

        paste('one-click')

        expected = exists(search_engine_pattern, 10)
        assert expected, 'One-Click Search Engines section found.'

        # Uncheck all the search engines from the list.
        while exists(check_engine_pattern, 2):
            click(check_engine_pattern)
            time.sleep(Settings.DEFAULT_UI_DELAY)

        expected = region.exists(check_engine_pattern.similar(0.9), 5)
        assert not expected, 'Each search engine is unchecked.'

        new_tab()

        select_location_bar()
        paste('moz')

        # Check that the one-off list is not displayed in the awesomebar after each search engine was unchecked.
        for index, pattern in enumerate(pattern_list):
            expected = exists(pattern.similar(0.9), 1)
            assert not expected, 'Element found at position {} in the list not found.'.format(index)

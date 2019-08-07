# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='This test case disables search suggestions in awesomebar.',
        locale=['en-US'],
        test_case_id='108263',
        test_suite_id='1902'
    )
    def run(self, firefox):
        url = LocalWeb.FIREFOX_TEST_SITE
        search_settings_pattern = Pattern('search_settings.png')
        about_preferences_search_page_pattern = Pattern('about_preferences_search_page.png')
        show_search_suggestions_in_address_bar_results_checked_pattern = Pattern(
            'show_search_suggestions_in_address_bar_results_checked.png').similar(0.6)
        show_search_suggestions_in_address_bar_results_unchecked_pattern = Pattern(
            'show_search_suggestions_in_address_bar_results_unchecked.png').similar(0.6)
        search_with_google_one_off_string_pattern = Pattern('search_with_Google_one_off_string.png')

        region = Screen().new_region(0, 0, Screen.SCREEN_WIDTH, 2 * Screen.SCREEN_HEIGHT / 3)

        navigate(url)

        expected = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert expected, 'Page successfully loaded, firefox logo found.'

        select_location_bar()
        paste('abc')

        time.sleep(Settings.DEFAULT_UI_DELAY)
        for i in range(10):
            type(Key.DOWN)

        expected = region.exists(search_with_google_one_off_string_pattern, 10)
        assert expected, 'With default value for the \'Show search suggestions in address bar results\' ' \
                         'option the \'Google\' search engine is found after 10 scrolls through the ' \
                         'suggestions list.'

        expected = region.exists(search_settings_pattern, 10)
        assert expected, 'The \'Search settings\' button is displayed in the awesomebar.'

        click(search_settings_pattern)
        time.sleep(Settings.DEFAULT_UI_DELAY)

        expected = exists(about_preferences_search_page_pattern, 10)
        assert expected, 'The \'about:preferences#search\' page successfully loaded.'

        expected = exists(show_search_suggestions_in_address_bar_results_checked_pattern, 10)
        assert expected, 'Checkbox displayed in front of the \'Show search suggestions in address bar ' \
                         'results\' text is checked by default.'

        click(show_search_suggestions_in_address_bar_results_checked_pattern)
        click(show_search_suggestions_in_address_bar_results_checked_pattern.target_offset(-100, 15),
              align=Alignment.TOP_LEFT)

        expected = exists(show_search_suggestions_in_address_bar_results_unchecked_pattern, 10)
        assert expected, 'Checkbox displayed in front of the \'Show search suggestions in address bar ' \
                         'results\' text is unchecked.'

        previous_tab()

        select_location_bar()
        type(Key.DELETE)
        paste('abc')

        time.sleep(Settings.DEFAULT_UI_DELAY)

        type(Key.DOWN)

        expected = region.exists(search_with_google_one_off_string_pattern, 10)
        assert expected, 'With modified value for the \'Show search suggestions in address bar results\' ' \
                         'option the \'Google\' search engine is found after 1 scroll through the ' \
                         'suggestions list.'

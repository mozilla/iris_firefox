# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='This test case disables search suggestions in awesomebar.',
        locale='[en-US]',
        test_case_id='108263',
        test_suite_id='1902',
        blocked_by='issue_77'
    )
    def test_run(self, firefox):
        url = LocalWeb.FIREFOX_TEST_SITE
        search_settings_pattern = Pattern('search_settings.png')
        about_preferences_search_page_pattern = Pattern('about_preferences_search_page.png')
        show_search_suggestions_in_address_bar_results_checked_pattern = Pattern(
            'show_search_suggestions_in_address_bar_results_checked.png')
        show_search_suggestions_in_address_bar_results_unchecked_pattern = Pattern(
            'show_search_suggestions_in_address_bar_results_unchecked.png')
        search_with_google_one_off_string_pattern = Pattern('search_with_Google_one_off_string.png')

        region = Screen().new_region(0, 0, Screen.SCREEN_WIDTH, 2 * Screen.SCREEN_HEIGHT / 3)

        # Perform a search with the 'Show search suggestions in address bar results' option checked(default state).

        navigate(url)

        expected = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert expected, 'Page successfully loaded, firefox logo found.'

        select_location_bar()
        paste('abc')

        # Wait a moment for the suggests list to fully populate before stepping down through it.
        time.sleep(Settings.DEFAULT_UI_DELAY)

        # The search suggestion list has 10 suggestions by default.
        for i in range(10):
            scroll_down()

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

        expected = exists(show_search_suggestions_in_address_bar_results_checked_pattern.similar(0.9), 10)
        assert expected, 'Checkbox displayed in front of the \'Show search suggestions in address bar ' \
                         'results\' text is checked by default.'

        # Perform a search with the 'Show search suggestions in address bar results' option unchecked(modified state).

        click(show_search_suggestions_in_address_bar_results_checked_pattern)

        # Move focus away from the clicked option.
        click(show_search_suggestions_in_address_bar_results_checked_pattern.target_offset(-100, 15))

        expected = exists(show_search_suggestions_in_address_bar_results_unchecked_pattern.similar(0.9), 10)
        assert expected, 'Checkbox displayed in front of the \'Show search suggestions in address bar ' \
                         'results\' text is unchecked.'

        previous_tab()

        select_location_bar()
        type(Key.DELETE)
        paste('abc')

        # Wait a moment for the suggests list to fully populate before stepping down through it.
        time.sleep(Settings.DEFAULT_UI_DELAY)

        # Check that the search suggestion list has now no suggestion.
        for i in range(1):
            scroll_down()

        expected = region.exists(search_with_google_one_off_string_pattern, 10)
        assert expected, 'With modified value for the \'Show search suggestions in address bar results\' ' \
                         'option the \'Google\' search engine is found after 1 scroll through the ' \
                         'suggestions list.'

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'This test case disables search suggestions in awesomebar.'
        self.test_case_id = '108263'
        self.test_suite_id = '1902'
        self.locales = ['en-US']

    def run(self):
        search_settings_pattern = Pattern('search_settings.png')
        about_preferences_search_page_pattern = Pattern('about_preferences_search_page.png')
        show_search_suggestions_in_address_bar_results_checked_pattern = \
            Pattern('show_search_suggestions_in_address_bar_results_checked.png')
        show_search_suggestions_in_address_bar_results_unchecked_pattern = \
            Pattern('show_search_suggestions_in_address_bar_results_unchecked.png')
        search_with_google_one_off_string_pattern = Pattern('search_with_Google_one_off_string.png')
        firefox_test_url = LocalWeb.FIREFOX_TEST_SITE

        top_part_of_screen_region = Region(0, 0, SCREEN_WIDTH, 2 * SCREEN_HEIGHT / 3)

        # Perform a search with the 'Show search suggestions in address bar results' option checked(default state).

        navigate(firefox_test_url)

        firefox_logo = exists(LocalWeb.FIREFOX_LOGO, Settings.FIREFOX_TIMEOUT)
        assert_true(self, firefox_logo, 'Page successfully loaded, firefox logo found.')

        select_location_bar()

        paste('abc')

        # Wait a moment for the suggests list to fully populate before stepping down through it.
        time.sleep(Settings.UI_DELAY)

        # The search suggestion list has 10 suggestions by default.
        for i in range(10):
            scroll_down()

        search_with_google_one_off = top_part_of_screen_region.exists(search_with_google_one_off_string_pattern,
                                                                      Settings.FIREFOX_TIMEOUT)
        assert_true(self, search_with_google_one_off, 'With default value for the \'Show search suggestions in address '
                                                      'bar results\' option the \'Google\' search engine is found after'
                                                      ' 10 scrolls through the suggestions list.')

        search_settings = top_part_of_screen_region.exists(search_settings_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, search_settings, 'The \'Search settings\' button is displayed in the awesomebar.')

        click(search_settings_pattern)

        time.sleep(Settings.UI_DELAY)

        about_preferences_search_page = exists(about_preferences_search_page_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, about_preferences_search_page, 'The \'about:preferences#search\' page successfully loaded.')

        suggestions_in_address_bar_checked = exists(show_search_suggestions_in_address_bar_results_checked_pattern,
                                                    Settings.FIREFOX_TIMEOUT)
        assert_true(self, suggestions_in_address_bar_checked, 'Checkbox displayed in front of the \'Show search '
                                                              'suggestions in address bar results\' text is checked '
                                                              'by default.')

        # Perform a search with the 'Show search suggestions in address bar results' option unchecked(modified state).

        click(show_search_suggestions_in_address_bar_results_checked_pattern)

        # Move focus away from the clicked option.
        type(Key.TAB)

        suggestions_in_address_bar_unchecked = exists(show_search_suggestions_in_address_bar_results_unchecked_pattern,
                                                      Settings.FIREFOX_TIMEOUT)
        assert_true(self, suggestions_in_address_bar_unchecked, 'Checkbox displayed in front of the \'Show search '
                                                                'suggestions in address bar results\' text is '
                                                                'unchecked.')

        previous_tab()

        select_location_bar()

        type(Key.DELETE)
        paste('abc')

        # Wait a moment for the suggests list to fully populate before stepping down through it.
        time.sleep(Settings.UI_DELAY)

        # Check that the search suggestion list has now no suggestion.
        for i in range(1):
            scroll_down()

        search_with_google_one_off = top_part_of_screen_region.exists(search_with_google_one_off_string_pattern,
                                                                      Settings.FIREFOX_TIMEOUT)
        assert_true(self, search_with_google_one_off, 'With modified value for the \'Show search suggestions in address'
                                                      ' bar results\' option the \'Google\' search engine is found '
                                                      'after 1 scroll through the suggestions list.')

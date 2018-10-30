# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'This test case verifies that changing the search engines positions the change is applied in ' \
                    'awesome bar too.'
        self.test_case_id = '108262'
        self.test_suite_id = '1902'
        self.locales = ['en-US']

    def run(self):
        search_engine_pattern = Pattern('search_engine.png')
        search_settings_pattern = Pattern('search_settings.png')
        amazon_one_off_button_pattern = Pattern('amazon_one_off_button.png')
        bing_one_off_button_pattern = Pattern('bing_one_off_button.png')
        duck_duck_go_one_off_button_pattern = Pattern('duck_duck_go_one_off_button.png')
        google_one_off_button_pattern = Pattern('google_one_off_button.png')
        twitter_one_off_button_pattern = Pattern('twitter_one_off_button.png')
        wikipedia_one_off_button_pattern = Pattern('wikipedia_one_off_button.png')
        about_preferences_search_page_pattern = Pattern('about_preferences_search_page.png')
        google_search_engine_pattern = Pattern('google_search_engine.png')
        duckduckgo_search_engine_pattern = Pattern('duckduckgo_search_engine.png')
        search_with_google_one_off_string_pattern = Pattern('search_with_Google_one_off_string.png')
        search_with_duckduckgo_one_off_string_pattern = Pattern('search_with_DuckDuckGo_one_off_string.png')
        search_with_bing_one_off_string_pattern = Pattern('search_with_Bing_one_off_string.png')

        region = Region(0, 0, SCREEN_WIDTH, 2 * SCREEN_HEIGHT / 3)

        select_location_bar()
        paste('moz')

        pattern_list = [google_one_off_button_pattern, bing_one_off_button_pattern, amazon_one_off_button_pattern,
                        duck_duck_go_one_off_button_pattern, twitter_one_off_button_pattern,
                        wikipedia_one_off_button_pattern]

        # Deleted assert for ebay because we no longer have the ebay search engine in place in some locations.

        # Check that the one-off list is displayed in the awesomebar.
        for i in range(pattern_list.__len__()):
            try:
                if Settings.get_os() == Platform.MAC:
                    expected = region.exists(pattern_list[i].similar(0.7), 10)
                    assert_true(self, expected, 'Element found at position ' + i.__str__() + ' in the list found.')
                else:
                    expected = region.exists(pattern_list[i].similar(0.9), 10)
                    assert_true(self, expected, 'Element found at position ' + i.__str__() + ' in the list found.')
            except FindError:
                raise FindError('Element found at position ' + i.__str__() + ' in the list not found.')

        # Wait a moment for the suggests list to fully populate before stepping down through it.
        time.sleep(Settings.UI_DELAY)

        repeat_key_down(10)
        key_to_one_off_search(search_with_google_one_off_string_pattern)

        expected = region.exists(search_with_google_one_off_string_pattern, 10)
        assert_true(self, expected, 'The \'Google\' one-off search engine holds the first position in the one-offs '
                                    'list by default.')

        type(Key.DOWN)

        expected = region.exists(search_with_bing_one_off_string_pattern, 10)
        assert_true(self, expected, 'The \'Bing\' one-off search engine holds the second position in the one-offs '
                                    'list by default.')

        # Navigate to the about:preferences#search page and reorder the search engines.
        click(search_settings_pattern)
        time.sleep(DEFAULT_UI_DELAY)

        expected = exists(about_preferences_search_page_pattern, 10)
        assert_true(self, expected, 'The \'about:preferences#search\' page successfully loaded.')

        paste('one-click')

        expected = exists(search_engine_pattern, 10)
        assert_true(self, expected, 'One-Click Search Engines section found.')

        drag_drop(duckduckgo_search_engine_pattern, google_search_engine_pattern, 0.5)

        # Make sure that the one-off buttons are reordered in the awesomebar.
        previous_tab()

        select_location_bar()
        type(Key.DELETE)
        type('moz')

        # Wait a moment for the suggests list to fully populate before stepping down through it.
        time.sleep(Settings.UI_DELAY)

        # Declare a variable which can close the while loop if the pattern is not found

        repeat_key_down(10)
        key_to_one_off_search(search_with_google_one_off_string_pattern)

        expected = region.exists(search_with_google_one_off_string_pattern, 10)
        assert_true(self, expected, 'The \'Google\' one-off search engine still holds the first position in the '
                                    'one-offs list after reorder.')

        type(Key.DOWN)

        expected = region.exists(search_with_duckduckgo_one_off_string_pattern, 10)
        assert_true(self, expected, 'The \'DuckDuckGo\' one-off search engine holds the second position in the'
                                    ' one-offs list after reorder.')

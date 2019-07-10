# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Alt+UP/DOWN Keys - in the Awesome Bar.',
        locale=['en-US'],
        test_case_id='108278',
        test_suite_id='1902',
        blocked_by={'id': '1488708', 'platform': OSPlatform.ALL}
    )
    def run(self, firefox):
        search_with_google_one_off_string_pattern = Pattern('search_with_Google_one_off_string.png')
        search_with_wikipedia_one_off_string_pattern = Pattern('search_with_Wikipedia_one_off_string.png')
        settings_gear_highlighted_pattern = Pattern('settings_gear_highlighted.png')
        moz_search_wikipedia_pattern = Pattern('moz_search_wikipedia.png')

        region = Region(0, 0, Screen().width / 2, Screen().height / 2)

        new_tab()
        select_location_bar()
        paste('moz')

        # Wait a moment for the suggests list to fully populate before stepping down through it.
        time.sleep(Settings.DEFAULT_UI_DELAY)

        # Navigate through the one-offs list with ALT + arrow UP keys. List has 6 elements but we will navigate 7 times
        # through the one-offs list to make sure that the settings gear button is not included in the cycle.

        key_down(Key.ALT)
        type(Key.UP)
        key_up(Key.ALT)

        expected = region.exists(search_with_wikipedia_one_off_string_pattern, 10)
        assert expected, "Wikipedia is the first one-off in focus when navigating with 'ALT and arrow UP keys."

        expected = not region.exists(settings_gear_highlighted_pattern, 5)
        assert expected, 'Settings gear icon is not in focus.'

        max_attempts = 10

        while max_attempts > 0:
            if region.exists(search_with_wikipedia_one_off_string_pattern, 1):
                assert expected, '\'Wikipedia\' is the one-off in focus.'
                max_attempts = 0
            else:
                key_down(Key.ALT)
                type(Key.UP)
                key_up(Key.ALT)
                max_attempts += 1

        new_tab()
        select_location_bar()
        paste('moz')

        # Wait a moment for the suggests list to fully populate before stepping down through it.
        time.sleep(Settings.DEFAULT_UI_DELAY)

        # Navigate through the one-offs list with ALT + arrow DOWN keys. List has 6 elements but we will navigate 7
        # times through the one-offs list to make sure that the settings gear button is not included in the cycle.

        key_down(Key.ALT)
        type(Key.DOWN)
        key_up(Key.ALT)

        expected = region.exists(search_with_google_one_off_string_pattern, 10)
        assert expected, 'Google is the first one-off in focus when navigating with ALT and arrow DOWN keys.'

        expected = not region.exists(settings_gear_highlighted_pattern, 5)
        assert expected, 'Settings gear icon is not in focus.'

        max_attempts = 10

        while max_attempts > 0:
            if region.exists(search_with_google_one_off_string_pattern, 1):
                assert expected, '\'Google\' is the one-off in focus.'
                max_attempts = 0
            else:
                key_down(Key.ALT)
                type(Key.DOWN)
                key_up(Key.ALT)
                max_attempts += 1

        select_location_bar()
        paste('moz')

        # Wait a moment for the suggests list to fully populate before stepping down through it.
        time.sleep(Settings.DEFAULT_UI_DELAY)

        # # Start cycling trough the autocomplete results. After this step the first suggestion is highlighted.
        repeat_key_down(1)
        repeat_key_up(1)

        # Start cycling through the one-offs list. We want to make sure that the suggestion previously highlighted is
        # still highlighted after navigating back and forth using the \'ALT\' and arrow UP/DOWN keys.

        key_down(Key.ALT)
        type(Key.DOWN)
        key_up(Key.ALT)

        expected = region.exists(search_with_google_one_off_string_pattern, 10)
        assert expected, 'Google\' is the first one-off in focus when navigating with \'ALT\' and arrow ''DOWN keys.'

        max_attempts = 10

        while max_attempts > 0:
            if region.exists(search_with_google_one_off_string_pattern, 1):
                assert expected, '\'Google\' is the one-off in focus.'
                max_attempts = 0
            else:
                key_down(Key.ALT)
                type(Key.DOWN)
                key_up(Key.ALT)
                max_attempts += 1

        # Start cycling through the one-off buttons in reverse order than above; 2 times to get the wikipedia one-off
        # in focus.

        for i in range(2):
            key_down(Key.ALT)
            type(Key.UP)
            key_up(Key.ALT)

        expected = region.exists(search_with_wikipedia_one_off_string_pattern, 10)
        assert expected, '\'Wikipedia\' is the one-off in focus.'

        expected = region.exists(moz_search_wikipedia_pattern, 10)
        assert expected, 'Previously autocomplete result in focus is still highlighted after navigating back ' \
                         'and forth using the \'ALT\' and arrow UP/DOWN keys.'

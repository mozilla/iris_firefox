# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='This test case navigates through one-off searches using the keyboard keys',
        locale=['en-US'],
        test_case_id='108267',
        test_suite_id='1902',
        blocked_by={'id': '1488708', 'platform': OSPlatform.ALL}
    )
    def run(self, firefox):
        url = LocalWeb.FIREFOX_TEST_SITE
        search_with_google_one_off_string_pattern = Pattern('search_with_Google_one_off_string.png')
        settings_gear_highlighted_pattern = Pattern('settings_gear_highlighted.png')

        region = Region(0, 0, Screen().width, 2 * Screen().height / 3)

        navigate(url)

        expected = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert expected, 'Page successfully loaded, firefox logo found.'

        # Navigate through suggests list using the arrow DOWN and arrow UP keys. Navigation is allowed on suggests
        # list on one-offs and setting gear icon.

        select_location_bar()
        paste('moz')

        # Wait a moment for the suggests list to fully populate before stepping down through it.
        time.sleep(Settings.DEFAULT_UI_DELAY)

        # The search suggestion list has 10 suggestions by default.
        for i in range(10):
            type(Key.DOWN)

        # First element in the one-offs list is \'Google\'.
        expected = region.exists(search_with_google_one_off_string_pattern, 10)
        assert expected, 'Navigation with arrow DOWN key works as expected.'

        for i in range(11):
            type(Key.UP)

        expected = region.exists(settings_gear_highlighted_pattern, 10)
        assert expected, 'Navigation with arrow UP key works as expected.'

        # Navigate through suggests list using the TAB key. Navigation is allowed only on suggests list. User can't
        # navigate to one-offs using "TAB" key.

        new_tab()

        select_location_bar()
        paste('moz')

        # Wait a moment for the suggests list to fully populate before stepping down through it.
        time.sleep(Settings.DEFAULT_UI_DELAY)

        # The search suggestion list has 10 suggestions by default.
        for i in range(10):
            type(Key.TAB)

        expected = not exists(search_with_google_one_off_string_pattern, 10)
        assert expected, 'Navigation through search suggestions list 10 times does not get in focus the ' \
                         '\'Google\' search engine. TAB navigation works only in search suggestions list.'

        # Navigate through suggests list using ALT and arrow DOWN/UP keys. The focus jumps directly to one-off
        # searches bar and the user navigates only inside the one-off search bar (the search gear is not included in
        # the cycle).

        new_tab()

        select_location_bar()
        paste('moz')

        # Wait a moment for the suggests list to fully populate before stepping down through it.
        time.sleep(Settings.DEFAULT_UI_DELAY)

        # Navigate through the one-offs list. List has 7 elements by default.

        key_down(Key.ALT)
        type(Key.DOWN)
        key_up(Key.ALT)

        expected = region.exists(search_with_google_one_off_string_pattern, 10)
        assert expected, '\'Google\' is the first one-off in focus.'

        for i in range(7):
            key_down(Key.ALT)
            type(Key.DOWN)
            key_up(Key.ALT)

        expected = not region.exists(settings_gear_highlighted_pattern, 10)
        assert expected, 'Settings gear icon is not in focus.'

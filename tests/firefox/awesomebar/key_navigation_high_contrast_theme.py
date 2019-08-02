# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
            description='Bug 1363692 - Key navigation in the URL drop-down in high contrast theme',
            locale=['en-US'],
            test_case_id='120136',
            test_suite_id='1902',
            blocked_by={'id': 'issue_2771', 'platform': OSPlatform.ALL}
    )
    def run(self, firefox):
        themes_pattern = Pattern('themes.png')
        dark_theme_pattern = AboutAddons.Themes.DARK_THEME
        moz_search_highlight_dark_theme_pattern = Pattern('moz_search_highlight_dark_theme.png').similar(.6)
        google_one_off_button_pattern = Pattern('google_one_off_button.png')
        url = LocalWeb.FIREFOX_TEST_SITE
        top_two_thirds_region = Region(0, 0, Screen.SCREEN_WIDTH, 2 * Screen.SCREEN_HEIGHT / 3)

        max_attempts = 0

        navigate(url)

        expected = exists(LocalWeb.FIREFOX_LOGO, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, 'Page successfully loaded, firefox logo found.'

        # The OS must have a high contrast theme activated.
        open_addons()

        expected = exists(themes_pattern, FirefoxSettings.FIREFOX_TIMEOUT, region=top_two_thirds_region)
        assert expected, 'Add-ons page successfully loaded.'

        click(themes_pattern)

        expected = exists(dark_theme_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, 'Dark theme option found in the page.'

        click(dark_theme_pattern)

        action_can_be_performed = exists(AboutAddons.Themes.ACTION_BUTTON)
        assert action_can_be_performed, 'Theme can be enabled/disabled.'

        click(AboutAddons.Themes.ACTION_BUTTON)

        expected = exists(AboutAddons.Themes.ENABLE_BUTTON, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, 'ENABLE button found in the page.'

        click(AboutAddons.Themes.ENABLE_BUTTON)

        type(Key.ESC)

        #  Start typing in the Awesome Bar.

        select_location_bar()
        paste('moz')
        type(Key.SPACE)

        expected = exists(moz_search_highlight_dark_theme_pattern, FirefoxSettings.FIREFOX_TIMEOUT,
                          region=top_two_thirds_region)
        assert expected, 'The autocomplete drop-down is opened.'

        # Using the "Up/Down" arrow keys navigate through the suggestion list.

        awesomebar_opened = exists(google_one_off_button_pattern, FirefoxSettings.FIREFOX_TIMEOUT,
                                   region=top_two_thirds_region)
        assert awesomebar_opened, 'Awesomebar available.'

        # The website in focus is highlighted.

        for max_attempts in range(20):
            type(Key.UP)
            if exists(moz_search_highlight_dark_theme_pattern, 1):
                break

        expected = exists(moz_search_highlight_dark_theme_pattern, FirefoxSettings.FIREFOX_TIMEOUT,
                          region=top_two_thirds_region)
        assert expected, 'The website in focus is highlighted.'

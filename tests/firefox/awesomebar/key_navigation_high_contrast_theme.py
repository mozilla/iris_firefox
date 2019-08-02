# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
            description='This test case performs key navigation in the URL drop-down in high contrast theme.',
            locale=['en-US'],
            test_case_id='120136',
            test_suite_id='1902'
        )
    def run(self, firefox):
        url = LocalWeb.FIREFOX_TEST_SITE
        themes_pattern = Pattern('themes.png')
        dark_theme_pattern = AboutAddons.Themes.DARK_THEME
        wear_theme_pattern = Pattern('wear_theme.png')
        moz_search_highlight_dark_theme_pattern = Pattern('moz_search_highlight_dark_theme.png')
        google_one_off_button_pattern = Pattern('google_one_off_button.png')
        search_wikipedia_dark_theme_pattern = Pattern('search_wikipedia_dark_theme.png')

        top_two_thirds_region = Region(0, 0, Screen.SCREEN_WIDTH, 2 * Screen.SCREEN_HEIGHT / 3)

        navigate(url)

        expected = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert expected, 'Page successfully loaded, firefox logo found.'

        # The OS must have a high contrast theme activated.
        open_addons()

        expected = region.exists(themes_pattern, 10)
        assert expected, 'Add-ons page successfully loaded.'

        click(themes_pattern)

        expected = exists(dark_theme_pattern, 10)
        assert expected, 'Dark theme option found in the page.'

        click(dark_theme_pattern)

        action_can_be_performed = exists(AboutAddons.Themes.ACTION_BUTTON)
        assert action_can_be_performed, 'Theme can be enabled/disabled.'

        click(AboutAddons.Themes.ACTION_BUTTON)

        expected = exists(AboutAddons.Themes.ENABLE_BUTTON, 10)
        assert expected, 'ENABLE button found in the page.'

        click(AboutAddons.Themes.ENABLE_BUTTON)

        type(Key.ESC)

        #  Start typing in the Awesome Bar.

        select_location_bar()
        paste('moz')
        type(Key.SPACE)

        expected = region.exists(moz_search_highlight_dark_theme_pattern, 10)
        assert expected, 'The autocomplete drop-down is opened.'

        # Using the "Up/Down" arrow keys navigate through the suggestion list.

        awesomebar_opened = exists(google_one_off_button_pattern, 10, region=top_two_thirds_region)
        assert awesomebar_opened, 'Awesomebar available.'

        # The website in focus is highlighted.

        max_attempts = 20

        while max_attempts > 0:
            type(Key.UP)
            if exists(moz_search_highlight_dark_theme_pattern, 1):
                max_attempts = 0
            max_attempts -= 1

        expected = region.exists(moz_search_highlight_dark_theme_pattern, 10)
        assert expected, 'The searched string is highlighted.'

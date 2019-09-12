# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='There are no glitches in tab layout.',
        locale=['en-US'],
        test_case_id='15268',
        test_suite_id='494'
    )
    def run(self, firefox):
        mozilla_tab_not_focused = Pattern('mozilla_tab_not_focused.png').similar(0.7)
        mozilla_tab_not_focused_light_theme = Pattern('mozilla_tab_not_focused_light_theme.png').similar(0.7)
        mozilla_hover = Pattern('mozilla_hover.png').similar(0.7)
        mozilla_hover_dark_theme = Pattern('mozilla_hover_dark_theme.png').similar(0.7)
        close_tab_button = Pattern('close_tab_button.png').similar(0.7)
        close_tab_button_dark_theme = Pattern('close_tab_button_dark_theme.png').similar(0.7)
        close_tab_hover = Pattern('close_tab_hover.png').similar(0.7)
        close_tab_hover_dark_theme = Pattern('close_tab_hover_dark_theme.png')

        open_addons()
        previous_tab()
        close_tab()

        expected = exists(AboutAddons.THEMES, 10)
        assert expected, 'Add-ons page successfully loaded.'

        click(AboutAddons.THEMES)

        expected = exists(AboutAddons.Themes.DARK_THEME, 10)
        assert expected, 'Dark theme option found in the page.'

        expected = exists(AboutAddons.Themes.LIGHT_THEME, 10)
        assert expected, 'Light theme option found in the page.'

        expected = exists(AboutAddons.Themes.DEFAULT_THEME, 10)
        assert expected, 'Default theme option found in the page.'

        # DEFAULT theme.
        click(AboutAddons.Themes.DEFAULT_THEME)

        expected = not exists(AboutAddons.Themes.ENABLE_BUTTON, 5)
        assert expected, 'ENABLE button NOT found in the page.'

        # Open at least 10 tabs and load pages in each one.
        for i in range(10):
            new_tab()
            navigate(LocalWeb.MOZILLA_TEST_SITE)
            expected = exists(LocalWeb.MOZILLA_LOGO, 120)
            assert expected, 'Mozilla page loaded successfully.'

        max_attempts = 9

        while max_attempts > 0:
            expected = exists(mozilla_tab_not_focused, 3)

            if expected:
                inactive_tab_location = find(mozilla_tab_not_focused)

                tab_title_width, tab_title_height = mozilla_tab_not_focused.get_size()

                active_tab_region = Region(inactive_tab_location.x - 5, inactive_tab_location.y - tab_title_height,
                                           tab_title_width * 4, tab_title_height * 10)

                hover(inactive_tab_location)

                expected = exists(mozilla_hover, 10, region=active_tab_region)
                assert expected, 'Mozilla page is hovered.'

                click(inactive_tab_location)

                expected = exists(close_tab_button, 10, region=active_tab_region)
                assert expected, 'Close tab button is visible.'

                close_width, close_height = close_tab_button.get_size()

                close_tab_button_location = find(close_tab_button, active_tab_region)
                close_click_location = Location(close_tab_button_location.x + close_width / 2,
                                                close_tab_button_location.y + close_width / 2)

                close_tab_hover_text_region = Region(close_tab_button_location.x-close_width,
                                                     close_tab_button_location.y,
                                                     close_width * 10, close_height*10)

                hover(close_click_location)

                expected = exists(close_tab_hover, 10, close_tab_hover_text_region)
                assert expected, 'Close button is hovered.'

                click(close_click_location)

                time.sleep(Settings.DEFAULT_UI_DELAY)

                max_attempts -= 1
            else:
                max_attempts = 0

        close_tab()

        # LIGHT theme.
        expected = exists(AboutAddons.THEMES, 10)
        assert expected, 'Add-ons page is in focus.'

        click(AboutAddons.THEMES)

        click(AboutAddons.Themes.LIGHT_THEME)

        action_can_be_performed = exists(AboutAddons.Themes.ACTION_BUTTON)
        assert action_can_be_performed, 'Theme can be enabled/disabled.'
        click(AboutAddons.Themes.ACTION_BUTTON)

        expected = exists(AboutAddons.Themes.ENABLE_BUTTON, 5)
        assert expected, 'ENABLE button found in the page.'

        click(AboutAddons.Themes.ENABLE_BUTTON)

        action_can_be_performed = exists(AboutAddons.Themes.ACTION_BUTTON)
        assert action_can_be_performed, 'Theme can be enabled/disabled.'
        click(AboutAddons.Themes.ACTION_BUTTON)

        expected = exists(AboutAddons.Themes.DISABLE_BUTTON, 10)
        assert expected, 'DISABLE button found in the page.'

        # Open at least 10 tabs and load pages in each one.
        for i in range(10):
            new_tab()
            navigate(LocalWeb.MOZILLA_TEST_SITE)
            expected = exists(LocalWeb.MOZILLA_LOGO, 120)
            assert expected, 'Mozilla page loaded successfully.'

        max_attempts = 9

        while max_attempts > 0:
            expected = exists(mozilla_tab_not_focused_light_theme, 3)

            if expected:
                inactive_tab_location = find(mozilla_tab_not_focused_light_theme)

                tab_title_width, tab_title_height = mozilla_tab_not_focused_light_theme.get_size()

                active_tab_region = Region(inactive_tab_location.x-5, inactive_tab_location.y - tab_title_height,
                                           tab_title_width * 4, tab_title_height * 10)

                hover(inactive_tab_location)

                expected = exists(mozilla_hover, 10, region=active_tab_region)
                assert expected, 'Mozilla page is hovered.'

                click(inactive_tab_location)

                expected = exists(close_tab_button, 10, region=active_tab_region)
                assert expected, 'Close tab button is visible.'

                close_tab_button_location = find(close_tab_button, active_tab_region)

                close_width, close_height = close_tab_button.get_size()

                close_click_location = Location(close_tab_button_location.x + close_width / 2,
                                                close_tab_button_location.y + close_width / 2)

                close_tab_hover_text_region = Region(close_tab_button_location.x-close_width,
                                                     close_tab_button_location.y,
                                                     close_width * 10, close_height*10)

                hover(close_click_location)

                expected = exists(close_tab_hover, 10, close_tab_hover_text_region)
                assert expected, 'Close button is hovered.'

                click(close_click_location)

                time.sleep(Settings.DEFAULT_UI_DELAY)

                max_attempts -= 1
            else:
                max_attempts = 0

        close_tab()

        # DARK theme.
        expected = exists(AboutAddons.THEMES, 10)
        assert expected, 'Add-ons page is in focus.'

        click(AboutAddons.THEMES)

        click(AboutAddons.Themes.DARK_THEME)

        action_can_be_performed = exists(AboutAddons.Themes.ACTION_BUTTON)
        assert action_can_be_performed, 'Theme can be enabled/disabled.'
        click(AboutAddons.Themes.ACTION_BUTTON)

        expected = exists(AboutAddons.Themes.ENABLE_BUTTON, 10)
        assert expected, 'ENABLE button found in the page.'

        click(AboutAddons.Themes.ENABLE_BUTTON)

        action_can_be_performed = exists(AboutAddons.Themes.ACTION_BUTTON)
        assert action_can_be_performed, 'Theme can be enabled/disabled.'
        click(AboutAddons.Themes.ACTION_BUTTON)

        expected = exists(AboutAddons.Themes.DISABLE_BUTTON, 10)
        assert expected, 'DISABLE button found in the page.'

        # Open at least 10 tabs and load pages in each one.
        for i in range(10):
            new_tab()
            navigate(LocalWeb.MOZILLA_TEST_SITE)
            expected = exists(LocalWeb.MOZILLA_LOGO, 120)
            assert expected, 'Mozilla page loaded successfully.'

        max_attempts = 9

        while max_attempts > 0:
            expected = exists(mozilla_tab_not_focused, 3)

            if expected:
                inactive_tab_location = find(mozilla_tab_not_focused)

                tab_title_width, tab_title_height = mozilla_tab_not_focused.get_size()

                active_tab_region = Region(inactive_tab_location.x-5, inactive_tab_location.y - tab_title_height,
                                           tab_title_width * 4, tab_title_height * 10)

                hover(inactive_tab_location)

                expected = exists(mozilla_hover_dark_theme, 10, region=active_tab_region)
                assert expected, 'Mozilla page is hovered.'

                click(inactive_tab_location)

                expected = exists(close_tab_button_dark_theme, 10, region=active_tab_region)
                assert expected, 'Close tab button is visible.'

                close_tab_dark_button_location = find(close_tab_button_dark_theme, active_tab_region)

                close_width, close_height = close_tab_button_dark_theme.get_size()

                close_dark_click_location = Location(close_tab_dark_button_location.x + close_width / 2,
                                                     close_tab_dark_button_location.y + close_width / 2)

                close_tab_hover_text_region = Region(close_tab_dark_button_location.x-close_width,
                                                     close_tab_dark_button_location.y,
                                                     close_width * 10, close_height*10)

                hover(close_dark_click_location)

                expected = exists(close_tab_hover_dark_theme, 10, close_tab_hover_text_region)
                assert expected, 'Close button is hovered.'

                click(close_dark_click_location)

                time.sleep(Settings.DEFAULT_UI_DELAY)

                max_attempts -= 1
            else:
                max_attempts = 0

        close_tab()

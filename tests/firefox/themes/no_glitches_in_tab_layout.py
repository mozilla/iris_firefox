# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description="There are no glitches in tab layout.",
        locale=["en-US"],
        test_case_id="15268",
        test_suite_id="494"
    )
    def run(self, firefox):
        mozilla_tab_not_focused = Pattern("mozilla_tab_not_focused.png").similar(0.7)
        mozilla_tab_not_focused_light_theme = Pattern("mozilla_tab_not_focused_light_theme.png").similar(0.7)
        mozilla_hover = Pattern("mozilla_hover.png").similar(0.7)
        mozilla_hover_dark_theme = Pattern("mozilla_hover_dark_theme.png").similar(0.7)
        close_tab_button = Pattern("close_tab_button.png").similar(0.7)
        close_tab_button_dark_theme = Pattern("close_tab_button_dark_theme.png").similar(0.7)
        close_tab_hover = Pattern("close_tab_hover.png").similar(0.7)
        close_tab_hover_dark_theme = Pattern("close_tab_hover_dark_theme.png")

        home_width, home_height = NavBar.HOME_BUTTON.get_size()
        tabs_region = Region(0, 0, Screen.SCREEN_WIDTH, home_height * 6)

        open_addons()
        previous_tab()
        close_tab()

        expected = exists(AboutAddons.THEMES, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, "Add-ons page couldn't load."

        click(AboutAddons.THEMES)

        expected = exists(AboutAddons.Themes.DEFAULT_THEME, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, "Default theme option not found in the page."

        expected = exists(AboutAddons.Themes.DARK_THEME, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, "Dark theme option not found in the page."

        if OSHelper.is_mac():
            click(Pattern("disabled_theme_header.png"))
            type(Key.DOWN)
        expected = exists(AboutAddons.Themes.LIGHT_THEME, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, "Light theme option not found in the page."

        # DEFAULT theme.
        click(AboutAddons.Themes.DEFAULT_THEME)
        time.sleep(Settings.DEFAULT_UI_DELAY)

        expected = not exists(AboutAddons.Themes.ENABLE_BUTTON, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert expected, "ENABLE button found in the page which is not expected"

        # Open at least 10 tabs and load pages in each one.
        for i in range(10):
            new_tab()
            navigate(LocalWeb.MOZILLA_TEST_SITE)
            expected = exists(LocalWeb.MOZILLA_LOGO, FirefoxSettings.FIREFOX_TIMEOUT)
            assert expected, "Mozilla page couldn't load."

        max_attempts = 9

        while max_attempts > 0:
            expected = exists(mozilla_tab_not_focused, FirefoxSettings.TINY_FIREFOX_TIMEOUT)

            if expected:
                inactive_tab_location = find(mozilla_tab_not_focused)

                hover(inactive_tab_location)

                expected = exists(mozilla_hover, FirefoxSettings.FIREFOX_TIMEOUT, region=tabs_region)
                assert expected, "Mozilla page couldn't hover."

                click(inactive_tab_location)

                time.sleep(Settings.DEFAULT_UI_DELAY_LONG)

                expected = exists(close_tab_button, FirefoxSettings.FIREFOX_TIMEOUT, region=tabs_region)
                assert expected, "Close tab button is not visible."

                close_width, close_height = close_tab_button.get_size()

                close_tab_button_location = find(close_tab_button, tabs_region)
                close_click_location = Location(
                    close_tab_button_location.x + close_width / 2, close_tab_button_location.y + close_width / 2
                )

                hover(close_click_location)

                expected = exists(close_tab_hover, FirefoxSettings.FIREFOX_TIMEOUT, tabs_region)
                assert expected, "Close button couldn't hover."

                click(close_click_location)

                time.sleep(Settings.DEFAULT_UI_DELAY)

                max_attempts -= 1
            else:
                max_attempts = 0

        open_addons()
        previous_tab()
        close_tab()

        # LIGHT theme.
        expected = exists(AboutAddons.THEMES, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, "Add-ons page is not in focus."

        navigate_back()

        expected = exists(AboutAddons.Themes.LIGHT_THEME,FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, "Light theme option couldn't found in the page."

        click(AboutAddons.Themes.LIGHT_THEME)

        expected = exists(AboutAddons.Themes.ENABLE_BUTTON, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert expected, "ENABLE button couldn't found in the page."

        click(AboutAddons.Themes.ENABLE_BUTTON)

        expected = exists(AboutAddons.Themes.DISABLE_BUTTON, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, "DISABLE button couldn't found in the page."

        # Open at least 10 tabs and load pages in each one.
        for i in range(10):
            new_tab()
            navigate(LocalWeb.MOZILLA_TEST_SITE)
            expected = exists(LocalWeb.MOZILLA_LOGO, FirefoxSettings.FIREFOX_TIMEOUT)
            assert expected, "Mozilla page couldn't load."

        max_attempts = 9

        while max_attempts > 0:
            expected = exists(mozilla_tab_not_focused_light_theme, FirefoxSettings.TINY_FIREFOX_TIMEOUT)

            if expected:
                inactive_tab_location = find(mozilla_tab_not_focused_light_theme)

                hover(inactive_tab_location)

                expected = exists(mozilla_hover, FirefoxSettings.FIREFOX_TIMEOUT, region=tabs_region)
                assert expected, "Mozilla page couldn't hover."

                click(inactive_tab_location)

                time.sleep(Settings.DEFAULT_UI_DELAY_LONG)

                expected = exists(close_tab_button, FirefoxSettings.FIREFOX_TIMEOUT, region=tabs_region)
                assert expected, "Close tab button is not visible."

                close_tab_button_location = find(close_tab_button, tabs_region)

                close_width, close_height = close_tab_button.get_size()

                close_click_location = Location(
                    close_tab_button_location.x + close_width / 2, close_tab_button_location.y + close_width / 2
                )

                hover(close_click_location)

                expected = exists(close_tab_hover, FirefoxSettings.FIREFOX_TIMEOUT, tabs_region)
                assert expected, "Close button couldn't hover."

                click(close_click_location)

                time.sleep(Settings.DEFAULT_UI_DELAY)

                max_attempts -= 1
            else:
                max_attempts = 0

        open_addons()
        previous_tab()
        close_tab()

        # DARK theme.
        expected = exists(AboutAddons.THEMES, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, "Add-ons page is not in focus."

        navigate_back()

        expected = exists(AboutAddons.Themes.DARK_THEME, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, "Dark theme option couldn't found in the page."

        click(AboutAddons.Themes.DARK_THEME)

        expected = exists(AboutAddons.Themes.ENABLE_BUTTON, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, "ENABLE button couldn't found in the page."

        click(AboutAddons.Themes.ENABLE_BUTTON)

        expected = exists(AboutAddons.Themes.DISABLE_BUTTON, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, "DISABLE button couldn't found in the page."

        # Open at least 10 tabs and load pages in each one.
        for i in range(10):
            new_tab()
            navigate(LocalWeb.MOZILLA_TEST_SITE)
            expected = exists(LocalWeb.MOZILLA_LOGO, FirefoxSettings.FIREFOX_TIMEOUT)
            assert expected, "Mozilla page couldn't load."

        max_attempts = 9

        while max_attempts > 0:
            expected = exists(mozilla_tab_not_focused, FirefoxSettings.TINY_FIREFOX_TIMEOUT)

            if expected:
                inactive_tab_location = find(mozilla_tab_not_focused)

                hover(inactive_tab_location)

                expected = exists(mozilla_hover_dark_theme, FirefoxSettings.FIREFOX_TIMEOUT, region=tabs_region)
                assert expected, "Mozilla page is couldn't hover."

                click(inactive_tab_location)

                time.sleep(Settings.DEFAULT_UI_DELAY_LONG)

                expected = exists(close_tab_button_dark_theme, FirefoxSettings.FIREFOX_TIMEOUT, region=tabs_region)
                assert expected, "Close tab button is not visible."

                close_tab_dark_button_location = find(close_tab_button_dark_theme, tabs_region)

                close_width, close_height = close_tab_button_dark_theme.get_size()

                close_dark_click_location = Location(
                    close_tab_dark_button_location.x + close_width / 2,
                    close_tab_dark_button_location.y + close_width / 2,
                )

                hover(close_dark_click_location)

                expected = exists(close_tab_hover_dark_theme, FirefoxSettings.FIREFOX_TIMEOUT, tabs_region)
                assert expected, "Close button is couldn't hover."

                click(close_dark_click_location)

                time.sleep(Settings.DEFAULT_UI_DELAY)

                max_attempts -= 1
            else:
                max_attempts = 0

        close_tab()

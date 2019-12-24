# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description="Check the appearance of browser with Default Themes applied in Menu Bar.",
        locale=["en-US"],
        test_case_id="15267",
        test_suite_id="494",
    )
    def run(self, firefox):
        open_addons()

        expected = exists(AboutAddons.THEMES, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, "Add-ons page successfully loaded."

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

        # Using the DEFAULT theme check that options from menu bar work correctly.
        click(AboutAddons.Themes.DEFAULT_THEME)
        time.sleep(Settings.DEFAULT_UI_DELAY)

        open_library()

        expected = exists(Library.BOOKMARKS_MENU, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, "Expand bookmarks menu button  doesn't displayed properly."

        if OSHelper.is_windows():
            type(text=Key.F4, modifier=KeyModifier.ALT)
        else:
            click_window_control("close")

        # Enable the LIGHT theme and check that options from menu bar work correctly using the selected theme.
        navigate_back()

        expected = exists(AboutAddons.Themes.LIGHT_THEME, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, "Light theme option  doesn't found in the page."

        click(AboutAddons.Themes.LIGHT_THEME)

        expected = exists(AboutAddons.Themes.ENABLE_BUTTON, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, "ENABLE button  doesn't found in the page."

        click(AboutAddons.Themes.ENABLE_BUTTON)

        expected = exists(AboutAddons.Themes.DISABLE_BUTTON, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, "DISABLE button  doesn't found in the page."

        open_library()

        expected = exists(Library.BOOKMARKS_MENU, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, "Expand bookmarks menu button  doesn't displayed properly."

        if OSHelper.is_windows():
            type(text=Key.F4, modifier=KeyModifier.ALT)
        else:
            click_window_control("close")

        # Enable the DARK theme and check that options from menu bar work correctly using the selected theme.
        navigate_back()

        expected = exists(AboutAddons.Themes.DARK_THEME, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, "Dark theme option  doesn't found in the page."

        click(AboutAddons.Themes.DARK_THEME)

        expected = exists(AboutAddons.Themes.ENABLE_BUTTON, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, "ENABLE button  doesn't found in the page."

        click(AboutAddons.Themes.ENABLE_BUTTON)

        expected = exists(AboutAddons.Themes.DISABLE_BUTTON, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, "DISABLE button  doesn't found in the page."

        open_library()

        expected = exists(Library.BOOKMARKS_MENU, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, "Expand bookmarks menu button doesn't displayed properly."

        if OSHelper.is_windows():
            type(text=Key.F4, modifier=KeyModifier.ALT)
        else:
            click_window_control("close")

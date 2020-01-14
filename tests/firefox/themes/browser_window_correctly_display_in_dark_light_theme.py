# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description="Browser window doesn't display when Dark/Light theme is enabled on Windows 10.",
        locale=["en-US"],
        test_case_id="118731",
        test_suite_id="494"
    )
    def run(self, firefox):
        iris_tab_light_theme = AboutAddons.Themes.IRIS_TAB_LIGHT_OR_DEFAULT_THEME
        iris_tab_dark_theme = AboutAddons.Themes.IRIS_TAB_DARK_THEME
        about_addons_url_dark_theme_pattern = Pattern("about_addons_url_dark_theme.png")
        about_addons_url_light_theme_pattern = Pattern("about_addons_url_light_theme.png")
        disabled_theme_header_pattern = Pattern("disabled_theme_header.png")

        open_hamburger_menu('Add-ons')

        themes_sidebar_expected = exists(AboutAddons.THEMES, FirefoxSettings.FIREFOX_TIMEOUT)
        assert themes_sidebar_expected, "Add-ons page couldn't load."

        click(AboutAddons.THEMES)

        expected = exists(AboutAddons.Themes.DEFAULT_THEME, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, "Default theme option not found in the page."

        expected = exists(AboutAddons.Themes.DARK_THEME, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, "Dark theme option not found in the page."

        if OSHelper.is_mac():
            click(disabled_theme_header_pattern)
            type(Key.DOWN)
            type(Key.DOWN)
        expected = exists(AboutAddons.Themes.LIGHT_THEME, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, "Light theme option not found in the page."

        themes_list = [AboutAddons.Themes.LIGHT_THEME, AboutAddons.Themes.DARK_THEME]
        iris_tab_theme_list = [iris_tab_light_theme, iris_tab_dark_theme]
        url_theme_pattern_list = [about_addons_url_light_theme_pattern, about_addons_url_dark_theme_pattern]

        for (theme_label, iris_tab_theme, url_theme_pattern) \
                in zip(themes_list, iris_tab_theme_list, url_theme_pattern_list):

            theme_location = find(theme_label)
            theme_width, theme_height = theme_label.get_size()
            theme_region = Region(0,
                                  theme_location.y - theme_height / 2,
                                  Screen.SCREEN_WIDTH,
                                  theme_height * 2)
            enable_button_expected = exists(AboutAddons.Themes.ENABLE_BUTTON, FirefoxSettings.FIREFOX_TIMEOUT,
                                            theme_region)
            theme_pattern_full_path = format(theme_label)
            theme_name_with_bracket = re.split("_", theme_pattern_full_path)
            theme_name = (str(theme_name_with_bracket[0]).replace("(", " "))
            assert enable_button_expected, "Enable button does not exists in {} theme region.".format(theme_name)

            click(AboutAddons.Themes.ENABLE_BUTTON, region=theme_region)
            previous_tab()
            theme_enabled = exists(iris_tab_theme, FirefoxSettings.FIREFOX_TIMEOUT)
            assert theme_enabled, "Unable to apply {} theme.".format(theme_name)
            firefox.restart()
            open_addons()
            browser_window_found = exists(url_theme_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
            assert browser_window_found, "Browser window doesn't display when {} theme is enabled".format(theme_name)

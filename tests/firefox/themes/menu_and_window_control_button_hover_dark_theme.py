# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description="Menu bar and window control button hover feedback lacks contrast on dark title bar",
        locale=["en-US"],
        test_case_id="118603",
        test_suite_id="494",
    )
    def run(self, firefox):
        file_menu_option_pattern = Pattern("file_menu_option.png")
        dark_theme_file_menu_option_selected_pattern = Pattern("dark_theme_file_menu_option_selected.png")

        # Preconditions
        open_addons()
        expected = exists(AboutAddons.THEMES, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, "Add-ons page successfully loaded."

        click(AboutAddons.THEMES)
        expected = exists(AboutAddons.Themes.DARK_THEME, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, "Dark theme option not found in the page."

        click(AboutAddons.Themes.DARK_THEME)
        expected = exists(AboutAddons.Themes.ENABLE_BUTTON, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, "ENABLE button  doesn't found in the page."

        click(AboutAddons.Themes.ENABLE_BUTTON)
        expected = exists(AboutAddons.Themes.DISABLE_BUTTON, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, "DISABLE button  doesn't found in the page."

        # Test case objective
        menu_option_region = Region(0,
                                    0,
                                    Screen.SCREEN_WIDTH / 3,
                                    Screen.SCREEN_HEIGHT / 10)
        if OSHelper.is_mac():
            click(file_menu_option_pattern, region=menu_option_region)
            highlighted_file_menu_option_found = exists(dark_theme_file_menu_option_selected_pattern,
                                                        FirefoxSettings.SHORT_FIREFOX_TIMEOUT,
                                                        region=menu_option_region)
            assert highlighted_file_menu_option_found, "Firefox View button highlighted"
        elif OSHelper.is_windows():
            previous_tab()
            iris_tab_expected = exists(AboutAddons.Themes.IRIS_TAB_DARK_THEME, FirefoxSettings.FIREFOX_TIMEOUT)
            assert iris_tab_expected, "Iris tab not found in the dark theme"
            iris_tab_location = find(AboutAddons.Themes.IRIS_TAB_DARK_THEME)
            iris_tab_width, iris_tab_height= AboutAddons.Themes.IRIS_TAB_DARK_THEME.get_size()
            right_click(iris_tab_location.offset(iris_tab_width * 3, iris_tab_height / 2))
            type(text="m",modifier=KeyModifier.SHIFT)
            file_menu_option_found = exists(file_menu_option_pattern,
                                            FirefoxSettings.SHORT_FIREFOX_TIMEOUT,
                                            region=menu_option_region)
            assert file_menu_option_found, "Firefox View button highlighted"
            click(file_menu_option_pattern)
            highlighted_file_menu_option_found = exists(dark_theme_file_menu_option_selected_pattern,
                                                        FirefoxSettings.SHORT_FIREFOX_TIMEOUT,
                                                        region=menu_option_region)
            assert highlighted_file_menu_option_found, "Firefox View button highlighted"
        elif OSHelper.is_linux():
            open_firefox_menu()
            file_menu_option_found = exists(file_menu_option_pattern,
                                            FirefoxSettings.SHORT_FIREFOX_TIMEOUT,
                                            region=menu_option_region)
            assert file_menu_option_found, "Firefox View button highlighted"
            click(file_menu_option_pattern)
            highlighted_file_menu_option_found = exists(dark_theme_file_menu_option_selected_pattern,
                                                        FirefoxSettings.SHORT_FIREFOX_TIMEOUT,
                                                        region=menu_option_region)
            assert highlighted_file_menu_option_found, "Firefox View button highlighted"

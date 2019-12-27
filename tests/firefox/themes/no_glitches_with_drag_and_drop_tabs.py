# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description="There are no UI glitches with drag & drop tabs.",
        locale=["en-US"],
        test_case_id="15271",
        test_suite_id="494"
    )
    def run(self, firefox):
        addons_manager_light_tab__pattern = Pattern("addons_manager_light.png")
        addons_manager_dark_tab_pattern = Pattern("addons_manager_dark.png")
        iris_tab_default_theme = AboutAddons.Themes.IRIS_TAB_LIGHT_OR_DEFAULT_THEME
        iris_tab_light_theme = AboutAddons.Themes.IRIS_TAB_LIGHT_OR_DEFAULT_THEME
        iris_tab_dark_theme = AboutAddons.Themes.IRIS_TAB_DARK_THEME

        open_hamburger_menu('Add-ons')

        themes_sidebar_expected = exists(AboutAddons.THEMES, FirefoxSettings.FIREFOX_TIMEOUT)
        assert themes_sidebar_expected, "Add-ons page couldn't load."

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

        iris_tabs = [iris_tab_light_theme,
                     iris_tab_default_theme,
                     iris_tab_dark_theme]
        themes = [AboutAddons.Themes.LIGHT_THEME,
                  AboutAddons.Themes.DEFAULT_THEME,
                  AboutAddons.Themes.DARK_THEME]

        for (theme_label, iris_tab) in zip(themes, iris_tabs):

            if OSHelper.is_mac():
                click(Pattern("disabled_theme_header.png"))
                type(Key.DOWN)

            theme_location = find(theme_label)
            theme_width, theme_height = theme_label.get_size()
            theme_region = Region(0,
                                  theme_location.y - theme_height / 2,
                                  Screen.SCREEN_WIDTH,
                                  theme_height * 2)
            enable_button_expected = exists(AboutAddons.Themes.ENABLE_BUTTON, FirefoxSettings.FIREFOX_TIMEOUT,
                                            theme_region)
            theme_pattern_full_path = format(theme_label)
            theme_name = re.split(".png", theme_pattern_full_path)
            theme = (str(theme_name[0]).replace("(", " ")).replace("_", " ")
            assert enable_button_expected, "Enable button does not exists in {} region.".format(theme)

            click(AboutAddons.Themes.ENABLE_BUTTON, region=theme_region)
            previous_tab()
            theme_enabled = exists(iris_tab, FirefoxSettings.FIREFOX_TIMEOUT)
            assert theme_enabled, "Unable to apply {}.".format(theme)

            drag_tab_location = find(iris_tab)
            iris_tab_width, iris_tab_height = iris_tab.get_size()
            previous_tab()
            if theme_label == AboutAddons.Themes.DARK_THEME:
                drop_tab_location = find(addons_manager_dark_tab_pattern)
            else:
                drop_tab_location = find(addons_manager_light_tab__pattern)
            drag_drop(drag_tab_location.offset(iris_tab_width/4, iris_tab_height/4), drop_tab_location)

            if theme_label == AboutAddons.Themes.LIGHT_THEME:
                iris_tab_location = find(iris_tab)
                addons_manager_tab_location = find(addons_manager_light_tab__pattern)
            elif theme_label == AboutAddons.Themes.DEFAULT_THEME:
                iris_tab_location = find(iris_tab_default_theme)
                addons_manager_tab_location = find(addons_manager_dark_tab_pattern)

            addons_manager_tab_width, addons_manager_tab_height = addons_manager_light_tab__pattern.get_size()
            reorder_tabs = Region(0,
                                  addons_manager_tab_location.y - addons_manager_tab_height / 2,
                                  Screen.SCREEN_WIDTH,
                                  addons_manager_tab_height * 2)
            if theme_label == AboutAddons.Themes.LIGHT_THEME:
                iris_tab_expected = exists(iris_tab, FirefoxSettings.FIREFOX_TIMEOUT, reorder_tabs)
            elif theme_label == AboutAddons.Themes.DEFAULT_THEME:
                iris_tab_expected = exists(iris_tab_default_theme,
                                           FirefoxSettings.FIREFOX_TIMEOUT, reorder_tabs)
            assert iris_tab_expected, "Iris tab not found in the {}.".format(theme)

            # Validate status of drag & drop tabs
            tabs_drag_drop = (addons_manager_tab_location.x < iris_tab_location.x)
            if theme_label == AboutAddons.Themes.DARK_THEME:
                assert tabs_drag_drop, "Unable to drag and drop tabs in tab strip for dark theme"
            else:
                assert tabs_drag_drop, "Unable to drag and drop tabs in tab strip for {}.".format(theme)
                next_tab()
                close_tab()
                open_addons()
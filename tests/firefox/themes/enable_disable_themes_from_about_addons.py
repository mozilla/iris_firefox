# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description="Enable/Disable Themes from about:addons",
        locale=["en-US"],
        test_case_id="14991",
        test_suite_id="494"
    )
    def run(self, firefox):
        addons_manager_light_tab = Pattern("addons_manager_light.png")
        addons_manager_dark_tab = Pattern("addons_manager_dark.png")
        light_theme_highlighted = Pattern("light_theme_enabled.png")
        most_visited_bookmarks = Pattern("most_visited_bookmarks.png")
        new_tab_icon = Pattern("new_tab_icon.png")
        pinned_tab = Pattern("pinned_new_tab.png")
        file_menu = Pattern("file_menu_option_light_theme.png")

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

        themes = [AboutAddons.Themes.DARK_THEME, AboutAddons.Themes.LIGHT_THEME]

        for theme_label in themes:
            theme_region, theme = self.region_creation_themes(theme_label, AboutAddons.Themes.ENABLE_BUTTON)

            addons_manager_tab = addons_manager_light_tab
            if theme_label == AboutAddons.Themes.DARK_THEME:
                addons_manager_tab = addons_manager_dark_tab
            for i in range(2):
                self.click_enable_disable_button(theme_region, addons_manager_tab, theme, button_type='enable')
                self.click_enable_disable_button(theme_region, addons_manager_tab, theme)
        self.switch_between_dark_and_light_themes(self,themes, addons_manager_tab)
        close_tab()

        new_private_window()
        private_window_expected = exists(PrivateWindow.PRIVATE_TAB, FirefoxSettings.FIREFOX_TIMEOUT)
        assert private_window_expected, "Unable to open private window."

        open_hamburger_menu('Add-ons')

        themes_sidebar_expected = exists(AboutAddons.THEMES, FirefoxSettings.FIREFOX_TIMEOUT)
        assert themes_sidebar_expected, "Add-ons page couldn't load."

        for i in range(2):
            theme_region, theme = self.region_creation_themes(light_theme_highlighted,
                                                              AboutAddons.Themes.DISABLE_BUTTON)
            self.click_enable_disable_button(theme_region, addons_manager_tab, theme)
            self.click_enable_disable_button(theme_region, addons_manager_tab, theme, button_type='enable')
        self.switch_between_dark_and_light_themes(self,themes, addons_manager_tab)

        # Verify basics actions
        new_tab()
        new_tab_expected = exists(PrivateWindow.PRIVATE_TAB, FirefoxSettings.FIREFOX_TIMEOUT)
        assert new_tab_expected, "Unable to open new tab"

        close_tab()
        themes_sidebar_expected = exists(AboutAddons.THEMES, FirefoxSettings.FIREFOX_TIMEOUT)
        assert themes_sidebar_expected, "Unable to close new tab"

        new_window()
        top_sites_expected = exists(Utils.TOP_SITES, FirefoxSettings.FIREFOX_TIMEOUT)
        assert top_sites_expected, "Unable to open new window."

        home_button = find(NavBar.HOME_BUTTON)
        right_click(home_button)
        if OSHelper.is_windows:
            type(text="b", modifier=KeyModifier.SHIFT)
        else:
            type(text="b", modifier=KeyModifier.CTRL)

        most_visited_sites_expected = exists(most_visited_bookmarks, FirefoxSettings.FIREFOX_TIMEOUT)
        assert most_visited_sites_expected, "Unable to open bookmarks toolbar."

        if OSHelper.is_linux():
            open_firefox_menu()
        elif OSHelper.is_windows():
            home_button = find(NavBar.HOME_BUTTON)
            right_click(home_button)
            type(text="m", modifier=KeyModifier.SHIFT)
        file_menu_expected = exists(file_menu, FirefoxSettings.FIREFOX_TIMEOUT)
        assert file_menu_expected, "unable to open menu bar"

        pin_new_tab = find(new_tab_icon)
        right_click(pin_new_tab)
        if OSHelper.is_windows:
            type(text="p", modifier=KeyModifier.SHIFT)
        else:
            type(text="p", modifier=KeyModifier.CTRL)
        mozilla_icon_expected = exists(pinned_tab, FirefoxSettings.FIREFOX_TIMEOUT)
        assert mozilla_icon_expected, "Unable to pin a tab"

        new_tab()
        new_tab_expected = exists(new_tab_icon, FirefoxSettings.FIREFOX_TIMEOUT)
        assert new_tab_expected, "Unable to open new tab"

        # drag new tab to new window
        controls_location = find(new_tab_icon)
        x_coord = controls_location.x
        y_coord = controls_location.y
        drag_start = Location(Screen.SCREEN_WIDTH/2, y_coord + 5)
        drag_end = Location(Screen.SCREEN_WIDTH/2, Screen.SCREEN_HEIGHT/2)
        drag_and_drop_duration = 2
        drag_drop(drag_start, drag_end, duration=drag_and_drop_duration)

        tab_location = find(new_tab_icon)
        drop_location = find(addons_manager_light_tab)
        drag_drop(tab_location, drop_location, duration=drag_and_drop_duration)

        top_sites_expected = exists(new_tab_icon, FirefoxSettings.FIREFOX_TIMEOUT)
        assert top_sites_expected, "Unable move a tab to new window."

    @staticmethod
    def switch_between_dark_and_light_themes(self, themes, addons_manager_tab):
        """Switch rapidly between 'Light' and 'Dark' theme by enabling/disabling.
        :param themes: image Pattern. locate for dark/light/default theme
        :param button: image Pattern, locate for enable/disable button
        :return: None
        """
        for i in range(2):
            for theme_label in themes:
                theme_region, theme_name = self.region_creation_themes(theme_label, AboutAddons.Themes.ENABLE_BUTTON)
                self.click_enable_disable_button(theme_region, addons_manager_tab, theme_name, button_type='enable')
        return True

    @staticmethod
    def click_enable_disable_button(theme_region, addons_manager_tab, theme_name, button_type=None):
        """Click rapidly enable/disable button in order to change the themes state
        :param theme_region: image Pattern. locate enable/disable button exists in the region
        :param addons_manager_tab: addons manager tab Pattern to confirm applied theme.
        :param theme_name: String, theme name.
        :param button_type: image Pattern, locate for enable/disable button
        :return: None.
        """
        button = AboutAddons.Themes.DISABLE_BUTTON
        if button_type:
            button = AboutAddons.Themes.ENABLE_BUTTON
        click(button, region=theme_region, duration=1)
        theme_enabled = exists(addons_manager_tab, FirefoxSettings.FIREFOX_TIMEOUT)
        assert theme_enabled, "Unable to apply {}.".format(theme_name)
        return True

    @staticmethod
    def region_creation_themes(themes, button):
        """Create a region to verify enable/disable button exists or not
        :param themes: image Pattern. locate for dark/light/default theme
        :param button: image Pattern, locate for enable/disable button
        :return: theme_region, theme_name.
        """
        themes_expected = exists(themes, FirefoxSettings.FIREFOX_TIMEOUT)
        theme_name = themes.get_filename().replace("_", " ").replace(".png", " ")
        assert themes_expected, "Unable to find {}".format(theme_name)

        theme_location = find(themes)
        theme_width, theme_height = themes.get_size()
        theme_region = Region(0,
                              theme_location.y - theme_height / 2,
                              Screen.SCREEN_WIDTH,
                              theme_height * 2)
        enable_button_expected = exists(button, FirefoxSettings.FIREFOX_TIMEOUT,
                                        theme_region)
        theme_name = themes.get_filename().replace("_", " ").replace(".png", " ")
        assert enable_button_expected, "Enable/Disable button does not exists in {}region.".format(theme_name)
        return theme_region, theme_name

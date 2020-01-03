# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description="All the themes can be applied and hovered in Customize mode",
        locale=["en-US"],
        test_case_id="14992",
        test_suite_id="494"
    )
    def run(self, firefox):
        dark_theme_pattern = Pattern("dark_theme_text.png")
        light_theme_location = Pattern("light_theme_text.png")
        default_theme_pattern = Pattern("default_theme_text.png")
        dark_hover_message_pattern = Pattern("dark_hover_message.png")
        light_hover_message_pattern = Pattern("light_hover_message.png")
        default_theme_hover_message_pattern = Pattern("default_hover_message.png")
        light_theme_doorhanger_pattern = Pattern("light_theme_doorhanger.png")
        dark_theme_doorhanger_pattern = Pattern("dark_theme_doorhanger.png")
        dark_theme_highlighted_pattern = Pattern("dark_theme_highlighted.png")
        light_theme_highlighted_pattern = Pattern("light_theme_highlighted.png")
        default_theme_highlighted_pattern = Pattern("default_theme_highlighted.png")
        undo_button_pattern = Pattern("undo_button.png")
        done_button_pattern = Pattern("done_button.png")
        dark_customize_pattern = Pattern("dark_customize.png")
        dark_download_icon_pattern = Pattern("dark_download_icon.png")
        dark_developer_tool_icon_pattern = Pattern("dark_developer_icon.png")
        dark_preferences_icon_pattern = Pattern("dark_preferences_icon.png")
        dark_search_icon_pattern = Pattern("dark_search_icon.png")
        dark_print_icon_pattern = Pattern("dark_print_icon.png")
        dark_history_icon_pattern = Pattern("dark_history_icon.png")

        open_hamburger_menu('Customize')

        default_theme_set_exist = exists(Customize.THEMES_DEFAULT_SET, FirefoxSettings.FIREFOX_TIMEOUT)
        assert default_theme_set_exist, "Could not open customize page"

        click(Customize.THEMES_DEFAULT_SET)

        default_theme_highlighted_exist = exists(default_theme_highlighted_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert default_theme_highlighted_exist, "Default theme is not highlighted"

        default_theme_highlighted_location = find(default_theme_highlighted_pattern)
        default_theme_width, default_theme_height = default_theme_highlighted_pattern.get_size()
        my_theme_region = Region(default_theme_highlighted_location.x,
                                 default_theme_highlighted_location.y,
                                 default_theme_width + default_theme_width / 4,
                                 default_theme_height * 4
                                 )

        all_theme = [default_theme_pattern, light_theme_location, dark_theme_pattern]
        for theme in all_theme:
            theme_exists = exists(theme, FirefoxSettings.FIREFOX_TIMEOUT, my_theme_region)
            doorhanger_theme_name = theme.get_filename().split(".")[0]
            assert theme_exists, f"Door-hanger does not display {doorhanger_theme_name}"

        default_theme_location = find(default_theme_pattern)
        light_theme_location = find(light_theme_location)
        dark_theme_location = find(dark_theme_pattern)

        theme_location_list = [default_theme_location, light_theme_location, dark_theme_location]
        hover_message_list = [default_theme_hover_message_pattern, light_hover_message_pattern,
                              dark_hover_message_pattern]

        for theme_location, hover_message in zip(theme_location_list, hover_message_list):
            hover(theme_location)
            hover_message_name = theme.get_filename().split(".")[0]
            default_theme_hover_message_exist = exists(hover_message, FirefoxSettings.FIREFOX_TIMEOUT)
            assert default_theme_hover_message_exist, f"{hover_message_name} message does not display"

        self.apply_theme(light_theme_location,
                         AboutAddons.Themes.IRIS_TAB_LIGHT_OR_DEFAULT_THEME,
                         light_theme_doorhanger_pattern,
                         light_theme_highlighted_pattern,
                         "light theme"
                         )

        self.apply_theme(default_theme_location,
                         AboutAddons.Themes.IRIS_TAB_LIGHT_OR_DEFAULT_THEME,
                         Customize.THEMES_DEFAULT_SET,
                         default_theme_highlighted_pattern,
                         "Default theme"
                         )

        self.apply_theme(dark_theme_location,
                         AboutAddons.Themes.IRIS_TAB_DARK_THEME,
                         dark_theme_doorhanger_pattern,
                         dark_theme_highlighted_pattern,
                         "Dark theme"
                         )

        click(done_button_pattern)

        dark_hamburger_exist = exists(NavBar.HAMBURGER_MENU_DARK_THEME, FirefoxSettings.FIREFOX_TIMEOUT)
        assert dark_hamburger_exist, "Could not find dark menu pattern"
        click(NavBar.HAMBURGER_MENU_DARK_THEME)

        dark_hamburg_menu_exists = exists(dark_customize_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert dark_hamburg_menu_exists, " Could not find customize option"
        click(dark_customize_pattern)

        customize_page_exists = exists(dark_theme_doorhanger_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert customize_page_exists, "Could not open customize page"

        download_icon_location = find(dark_download_icon_pattern)
        nav_width, nav_height = dark_download_icon_pattern.get_size()
        toolbar_region = Region(download_icon_location.x - nav_width * 10,
                                download_icon_location.y - nav_height / 4,
                                nav_width + nav_width * 10,
                                nav_height + nav_height / 2
                                )

        palette_items = [dark_developer_tool_icon_pattern, dark_preferences_icon_pattern, dark_search_icon_pattern,
                         dark_print_icon_pattern, dark_history_icon_pattern]
        for item in palette_items:
            developer_icon_location = find(item)
            drag_drop(developer_icon_location, download_icon_location)
            drop_location_exists = exists(item, FirefoxSettings.FIREFOX_TIMEOUT, toolbar_region)
            assert drop_location_exists, "Could not drag and drop {} in Navigation toolbar".format(item.get_filename())

        click(Customize.RESTORE_DEFAULTS)

        click(Customize.THEMES_DEFAULT_SET)
        default_theme_highlighted_check = exists(default_theme_highlighted_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert default_theme_highlighted_check, "Default theme is not highlighted in door-hanger"

        click(undo_button_pattern)
        dark_theme_exist = exists(AboutAddons.Themes.IRIS_TAB_DARK_THEME, FirefoxSettings.FIREFOX_TIMEOUT)
        assert dark_theme_exist, "Could not apply dark theme successfully"

    @staticmethod
    def apply_theme(unselected_theme_locations: Location,
                    confirm_tab_theme: Pattern,
                    selected_theme_door_hanger: Pattern,
                    confirm_selected_theme: Pattern,
                    theme_name: str):
        """Check if Pattern or image exists.
                :param unselected_theme_locations: Unselected theme pattern from 'My Theme' menu list.
                :param confirm_tab_theme: Iris tab Pattern to confirm the applied menu.
                :param selected_theme_door_hanger: Selected theme Pattern in collapsed theme menu.
                :param confirm_selected_theme: Selected theme pattern from 'My Theme' menu list.
                :param theme_name: Theme name.
                :return: None.
                """
        click(unselected_theme_locations)
        previous_tab()
        light_theme_check = exists(confirm_tab_theme, FirefoxSettings.FIREFOX_TIMEOUT)
        assert light_theme_check, f"Could not apply {theme_name} successfully"
        previous_tab()
        click(selected_theme_door_hanger)
        light_theme_highlighted_check = exists(confirm_selected_theme, FirefoxSettings.FIREFOX_TIMEOUT)
        assert light_theme_highlighted_check, f"{theme_name} is not highlighted in door-hanger"

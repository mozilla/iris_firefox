# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Search when High Contrast is activated'
        self.test_case_id = '127254'
        self.test_suite_id = '2085'
        self.locales = ['en-US']
        self.exclude = Platform.MAC

    def run(self):

        find_in_page_bar_contrast_pattern = Pattern('find_in_page_bar_contrast.png')
        find_in_page_bar_contrast_pattern.similarity = 0.6

        soap_page_loaded_contrast_pattern = Pattern('soap_page_loaded_contrast.png')
        see_label_contrast_pattern = Pattern('see_label_contrast.png')

        see_label_unhighlited_contrast_pattern = Pattern('see_label_unhighlited_contrast.png')
        see_label_zoom_in_contrast_pattern = Pattern('see_label_zoom_in_contrast.png')
        see_label_zoom_out_contrast_pattern = Pattern('see_label_zoom_out_contrast.png')


        # win theme settings
        if Settings.get_os() == Platform.WINDOWS:
            close_active_contrast_window_pattern = Pattern('close_active_contrast_window.png')
            win_off_high_contrast_button_theme_pattern = Pattern('win_off_high_contrast_theme.png')  # 10

            if get_os_version() == 'win7':         # windows 7 theme settings
                close_window_contrast_deactivated_pattern = Pattern('close_window_contrast_deactivated.png')

            else:   # windows 10 theme settings
                win_high_contrast_settings_pattern = Pattern('win_high_contrast_settings.png')
                win_on_high_contrast_theme_pattern = Pattern('high_contrast_is_on.png')  # high contrast is on

        if Settings.is_linux():

            high_contrast_bttn_normal_theme_pattern = Pattern('high_contrast_bttn_normal_theme.png')

            default_contrast_bttn_normal_theme_pattern = Pattern('default_contrast_bttn_normal_theme.png')
            default_contrast_bttn_normal_theme_pattern.similarity = 0.6

            default_contrast_bttn_high_theme_pattern = Pattern('default_contrast_bttn_high_theme.png')  # for closing
            default_contrast_bttn_high_theme_pattern.similarity = 0.6

            system_menu_opened_pattern = Pattern('system_search_menu_contrast.png')
            appearance_panel_default_pattern = Pattern('appearance_panel_default_contrast_displayed.png')
            appearance_panel_default_pattern.similarity = 0.6

            appearance_panel_high_pattern = Pattern('appearance_panel_high_contrast_displayed.png')

            type(Key.META)

            system_menu_opened = exists(system_menu_opened_pattern, 5)
            assert_true(self, system_menu_opened, 'System menu opened')

            type('appearance')
            # type(Key.TAB)
            type(Key.ENTER)

            appearance_panel_default_contrast_loaded = exists(appearance_panel_default_pattern, 5)
            assert_true(self, appearance_panel_default_contrast_loaded, 'Appearence menu loaded in default theme')

            contrast_dropdown_bttn_location = find(default_contrast_bttn_normal_theme_pattern)
            click(Location(contrast_dropdown_bttn_location.x+3,
                           contrast_dropdown_bttn_location.y+3), 1)

            click(high_contrast_bttn_normal_theme_pattern, 1)

            high_contrast_is_on = exists(appearance_panel_high_pattern, 5)

            type(Key.F4, KeyModifier.ALT)  # close window

            assert_true(self, high_contrast_is_on,
                        'Ubuntu theme changed to "HighContrast". High contrast theme activated')

        if Settings.is_windows():
            if get_os_version() == 'win7':
                os_program_menu_opened_basic_contrast_pattern = Pattern('os_program_menu_opened_basic_contrast.png')
                theme_menu_opened_pattern = Pattern('theme_menu_opened_basic_contrast.png')
                high_contrast_normal_button_pattern = Pattern('high_contrast_normal_button.png')
                high_contrast_black_button_active_pattern = Pattern('high_contrast_black_button_active.png')

                type(Key.WIN)
                os_program_menu_opened = exists(os_program_menu_opened_basic_contrast_pattern, 20)
                assert_true(self, os_program_menu_opened, 'OS program menu opened properly.')

                type("Change the theme")
                type(Key.ENTER)
                theme_menu_opened_exists = exists(theme_menu_opened_pattern, 30)
                assert_true(self, theme_menu_opened_exists, "Theme settings menu opened properly")

                #  click on theme
                click(high_contrast_normal_button_pattern, 1)
                #  theme changed

                theme_changed_to_high_contrast = wait_vanish(high_contrast_normal_button_pattern.similar(0.75), 40)
                assert_true(self, theme_changed_to_high_contrast, 'Theme changed to high contrast theme.')

                #  close theme page
                #  wait wanish theme page close
                type(Key.F4, KeyModifier.ALT)

                # Check that the Theme Settings window was closed properly.
                theme_settings_window_is_closed = wait_vanish(high_contrast_black_button_active_pattern.similar(0.75), 10)
                assert_true(self, theme_settings_window_is_closed,
                            'Theme Setting window was closed properly.')

            else:  # win 10

                type(Key.WIN)

                paste('themes and related settings')
                type(Key.ENTER)

                win_high_contrast_settings_exists = exists(win_high_contrast_settings_pattern, 10)
                win_high_contrast_settings_location = find(win_high_contrast_settings_pattern)
                click(Location(win_high_contrast_settings_location.x+10,
                               win_high_contrast_settings_location.y+10), 1)

                win_off_high_contrast_theme_exists = exists(win_off_high_contrast_button_theme_pattern, 10)
                win_off_high_contrast_theme_location = find(win_off_high_contrast_button_theme_pattern)
                click(Location(win_off_high_contrast_theme_location.x+7,
                               win_off_high_contrast_theme_location.y+7), 1)

                # delay for high contrast to be enabled
                time.sleep(5)
                high_contrast_enabled = exists(win_on_high_contrast_theme_pattern, 5)
                assert_true(self, high_contrast_enabled, 'High contrast option enabled on Windows 10')

                win_close_active_window_location = find(close_active_contrast_window_pattern)
                click(close_active_contrast_window_pattern, 1)

        # test body
        test_page_local = self.get_asset_path('wiki_soap.html')
        navigate(test_page_local)

        soap_page_loaded_exists = exists(soap_page_loaded_contrast_pattern, 20)

        assert_true(self, soap_page_loaded_exists, 'The page is successfully loaded.')

        time.sleep(1)

        open_find()
        edit_select_all()
        edit_delete()

        find_toolbar_opened = exists(find_in_page_bar_contrast_pattern, 10)
        assert_true(self, find_toolbar_opened, 'Find Toolbar opened.')

        type('see', interval=1)
        type(Key.ENTER)

        selected_label_exists = exists(see_label_contrast_pattern, 5)
        unhighlighted_label_exists = exists(see_label_unhighlited_contrast_pattern, 5)

        assert_true(self, selected_label_exists,
                    'The first one has a green background highlighted.')
        assert_true(self, unhighlighted_label_exists,
                    'The others are not highlighted.')

        zoom_in()

        selected_label_exists = exists(see_label_zoom_in_contrast_pattern, 5)

        assert_true(self, selected_label_exists,
                    'Zoom in: The highlight of the found items does not affect the visibility '
                    'of other words/letters')

        zoom_out()
        zoom_out()

        selected_label_exists = exists(see_label_zoom_out_contrast_pattern, 5)

        assert_true(self, selected_label_exists,
                    'Zoom out: The highlight of the found items does not affect the visibility '
                    'of other words/letters')

        #
        # Return back to normal mode,
        # and close themes settings, and console window
        #

        if Settings.is_linux():
            try:
                type(Key.META)

                system_menu_opened = exists(system_menu_opened_pattern, 5)
                assert_true(self, system_menu_opened, 'System menu opened')

                type('appearance')
                # type(Key.TAB)
                type(Key.ENTER)

                appearance_panel_high_contrast_loaded = exists(appearance_panel_high_pattern, 5)
                assert_true(self, appearance_panel_high_contrast_loaded, 'Appearence menu loaded in high contrast theme')

                click(Location(contrast_dropdown_bttn_location.x+5,
                               contrast_dropdown_bttn_location.y+5), 1)

                click(default_contrast_bttn_high_theme_pattern, 1)

                high_contrast_is_off = exists(appearance_panel_default_pattern, 5)

                type(Key.F4, KeyModifier.ALT) # close window

                assert_true(self, high_contrast_is_off,
                                'Ubuntu theme changed to default "Ambiance". '
                                'High contrast theme deactivated')
            except FindError:
                logger.warn("Can't find pattern to exit contrast mode. One more attempt")

                type(Key.META)

                system_menu_opened = exists(system_menu_opened_pattern, 5)
                assert_true(self, system_menu_opened, 'System menu opened')

                type('appearance')
                # type(Key.TAB)
                type(Key.ENTER)

                appearance_panel_high_contrast_loaded = exists(appearance_panel_high_pattern, 5)
                assert_true(self, appearance_panel_high_contrast_loaded,
                            'Appearence menu loaded in high contrast theme')

                click(Location(contrast_dropdown_bttn_location.x + 5,
                               contrast_dropdown_bttn_location.y + 5), 1)

                click(default_contrast_bttn_high_theme_pattern, 1)

                high_contrast_is_off = exists(appearance_panel_default_pattern, 5)

                type(Key.F4, KeyModifier.ALT)  # close window

                assert_true(self, high_contrast_is_off,
                            'Ubuntu theme changed to default "Ambiance". '
                            'High contrast theme deactivated')

        if Settings.is_windows():
            if get_os_version() == 'win7':
                theme_menu_opened_in_high_contrast_pattern = Pattern('os_program_menu_opened_high_contrast.png')
                high_contrast_basic_theme_button_pattern = Pattern('high_contrast_basic_theme_button.png')

                type(Key.WIN)
                os_program_menu_opened_in_high_contrast = exists(theme_menu_opened_in_high_contrast_pattern, 20)
                assert_true(self, os_program_menu_opened_in_high_contrast, 'OS program menu opened properly.')

                type("Change the theme")
                type(Key.ENTER)
                theme_menu_opened_in_high_contrast = exists(high_contrast_black_button_active_pattern, 30)
                assert_true(self, theme_menu_opened_in_high_contrast, "Theme settings menu opened properly")

                #  click on theme
                click(high_contrast_basic_theme_button_pattern, 1)
                #  theme changed

                theme_changed_to_basic_contrast = exists(theme_menu_opened_pattern.similar(0.75), 40)
                assert_true(self, theme_changed_to_basic_contrast, 'Theme changed to basic contrast theme.')

                #  close theme page
                #  wait vanish theme page close
                type(Key.F4, KeyModifier.ALT)

                # Check that the Theme Settings window was closed properly.
                theme_settings_window_is_closed = wait_vanish(theme_menu_opened_pattern.similar(0.75), 40)
                assert_true(self, theme_settings_window_is_closed,
                            'Theme Setting window was closed properly.')

            else: # deactivate high contrast mode on WIN 10
                try:

                    type(Key.WIN)

                    paste('themes and related settings')
                    type(Key.ENTER)

                    click(Location(win_high_contrast_settings_location.x + 10,
                                   win_high_contrast_settings_location.y + 10), 1)

                    click(Location(win_off_high_contrast_theme_location.x + 7,
                                   win_off_high_contrast_theme_location.y + 7), 1)

                    contrast_mode_off = exists(win_off_high_contrast_button_theme_pattern, 10)

                    # close theme settings window
                    click(Location(win_close_active_window_location.x+2,
                                   win_close_active_window_location.y+2), 1)

                    assert_true(self, contrast_mode_off,
                                'High contrast mode deactivated')

                except FindError:
                    type(Key.WIN)

                    paste('themes and related settings')
                    type(Key.ENTER)

                    click(Location(win_high_contrast_settings_location.x + 10,
                                   win_high_contrast_settings_location.y + 10), 1)

                    click(Location(win_off_high_contrast_theme_location.x + 7,
                                   win_off_high_contrast_theme_location.y + 7), 1)

                    contrast_mode_off = exists(win_off_high_contrast_button_theme_pattern, 10)

                    # close theme settings window
                    click(Location(win_close_active_window_location.x+2,
                                   win_close_active_window_location.y+2), 1)

                    assert_true(self, contrast_mode_off,
                                'High contrast mode deactivated')
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description='Search when High Contrast is activated',
        locale=['en-US'],
        test_case_id='127254',
        test_suite_id='2085',
        blocked_by={'id': 'issue_1667', 'platform': OSPlatform.ALL}
    )
    def run(self, firefox):
        find_in_page_bar_contrast_pattern = Pattern('find_in_page_bar_contrast.png').similar(0.6)
        soap_page_loaded_contrast_pattern = Pattern('soap_page_loaded_contrast.png')
        see_label_contrast_pattern = Pattern('see_label_contrast.png')
        see_label_not_highlighted_contrast_pattern = Pattern('see_label_not_highlighted_contrast.png')
        see_label_zoom_in_contrast_pattern = Pattern('see_label_zoom_in_contrast.png')
        see_label_zoom_out_contrast_pattern = Pattern('see_label_zoom_out_contrast.png')

        #  Change theme to high contrast
        os_program_menu_opened_basic_contrast_pattern = Pattern('os_program_menu_opened_basic_contrast.png')
        theme_menu_opened_pattern = Pattern('theme_menu_opened_basic_contrast.png')
        high_contrast_normal_button_pattern = Pattern('high_contrast_normal_button.png')
        high_contrast_black_button_active_pattern = Pattern('high_contrast_black_button_active.png')

        theme_menu_opened_in_high_contrast_pattern = Pattern('os_program_menu_opened_high_contrast.png')
        high_contrast_basic_theme_button_pattern = Pattern('high_contrast_basic_theme_button.png')

        if OSHelper.is_linux():
            default_contrast_normal_button_pattern = Pattern('default_contrast_normal_button.png')  # for closing
            high_contrast_button_high_theme_pattern = Pattern('high_contrast_button_high_theme.png')
            type(Key.META)

        if OSHelper.is_windows():
            type(Key.WIN)

        os_program_menu_opened = exists(os_program_menu_opened_basic_contrast_pattern,
                                        FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert os_program_menu_opened, 'System menu opened'

        if OSHelper.is_windows() and OSHelper.get_os_version() is not 'win7':
            type('Change high contrast theme')
        if OSHelper.get_os_version() == 'win7':
            type('Change the theme')
        if OSHelper.is_linux():
            type('Appearance')

        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)

        type(Key.ENTER)

        theme_menu_opened = exists(theme_menu_opened_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert theme_menu_opened, 'Theme settings menu opened properly'

        if OSHelper.is_linux():
            click(default_contrast_normal_button_pattern, 1)

        if OSHelper.get_os_version() == 'win7':
            maximize_window()

        high_contrast_normal_button_pattern_is_visible = exists(high_contrast_normal_button_pattern,
                                                                FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert high_contrast_normal_button_pattern_is_visible, 'High contrast button is visible.'

        click(high_contrast_normal_button_pattern, 1)
        theme_changed_to_high_contrast = exists(high_contrast_black_button_active_pattern.similar(0.75),
                                                FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert theme_changed_to_high_contrast, 'Theme changed to high contrast theme.'

        try:
            type(Key.F4, KeyModifier.ALT)

            theme_settings_window_is_closed = wait_vanish(high_contrast_black_button_active_pattern.similar(0.75),
                                                          FirefoxSettings.FIREFOX_TIMEOUT)
            assert theme_settings_window_is_closed is not True, 'Theme Setting window was closed properly.'
        except FindError:
            raise FindError('Theme Setting window was not closed properly.')

        # test body
        try:
            navigate(LocalWeb.SOAP_WIKI_TEST_SITE)
            soap_page_loaded_exists = exists(soap_page_loaded_contrast_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
            assert soap_page_loaded_exists, 'The page is successfully loaded.'

            time.sleep(2)

            open_find()
            edit_select_all()
            edit_delete()

            find_toolbar_opened = exists(find_in_page_bar_contrast_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
            assert find_toolbar_opened, 'Find Toolbar opened.'

            paste('see')
            type(Key.ENTER)

            selected_label_exists = exists(see_label_contrast_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
            assert selected_label_exists, 'The first one has a green background highlighted.'

            unhighlighted_label_exists = exists(see_label_not_highlighted_contrast_pattern,
                                                FirefoxSettings.FIREFOX_TIMEOUT)
            assert unhighlighted_label_exists, 'The others are not highlighted.'

            zoom_in()
            selected_label_exists = exists(see_label_zoom_in_contrast_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
            assert selected_label_exists, 'Zoom in: The highlight of the found items does not affect the visibility ' \
                                          'of other words/letters'

            zoom_out()
            zoom_out()
            selected_label_exists = exists(see_label_zoom_out_contrast_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
            assert selected_label_exists, 'Zoom out: The highlight of the found items does not affect the visibility ' \
                                          'of other words/letters'

        except FindError:
            raise FindError('Unable to find an element')

        finally:
            #
            # Return back to default contrast theme,
            # and close Themes Settings window
            #
            if OSHelper.is_linux():
                type(Key.META)
            else:
                type(Key.WIN)

            os_program_menu_opened_in_high_contrast = exists(theme_menu_opened_in_high_contrast_pattern,
                                                             FirefoxSettings.FIREFOX_TIMEOUT)
            assert os_program_menu_opened_in_high_contrast, 'OS program menu opened properly.'

            if OSHelper.is_windows() and OSHelper.get_os_version() is not 'win7':
                type('Change high contrast theme')
            if OSHelper.get_os_version() == 'win7':
                type('Change the theme')
            if OSHelper.is_linux():
                type('Appearance')

            time.sleep(2)
            type(Key.ENTER)
            theme_menu_opened_in_high_contrast = exists(high_contrast_black_button_active_pattern,
                                                        FirefoxSettings.SITE_LOAD_TIMEOUT)
            assert theme_menu_opened_in_high_contrast, 'Theme settings menu opened properly'
            if OSHelper.get_os_version() == 'win7':
                maximize_window()
            if OSHelper.is_linux():
                click(high_contrast_button_high_theme_pattern, 1)

            high_contrast_basic_theme_button_pattern_is_visible = exists(high_contrast_basic_theme_button_pattern,
                                                                         FirefoxSettings.SITE_LOAD_TIMEOUT)
            assert high_contrast_basic_theme_button_pattern_is_visible, 'High contrast basic theme button is visible.'
            click(high_contrast_basic_theme_button_pattern, 1)

            theme_changed_to_basic_contrast = exists(theme_menu_opened_pattern.similar(0.75),
                                                     FirefoxSettings.SITE_LOAD_TIMEOUT)
            assert theme_changed_to_basic_contrast, 'Theme changed to basic contrast theme.'

            try:
                type(Key.F4, KeyModifier.ALT)
                theme_settings_window_is_closed = wait_vanish(theme_menu_opened_pattern.similar(0.75),
                                                              FirefoxSettings.FIREFOX_TIMEOUT)
                assert theme_settings_window_is_closed is not True, 'Theme Setting window was closed properly.'
            except FindError:
                raise FindError('Theme Setting window was not closed properly.')

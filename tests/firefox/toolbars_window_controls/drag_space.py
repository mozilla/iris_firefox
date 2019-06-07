# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description='This is a test case that checks that the drag space can be activated properly.',
        locale=['en-US'],
        test_case_id='118184',
        test_suite_id='1998',
        exclude=OSPlatform.LINUX
    )
    def run(self, firefox):
        customize_page_drag_space_disabled_pattern = Pattern('customize_page_drag_space_disabled.png')
        drag_space_disabled_pattern = Pattern('drag_space_disabled.png')
        customize_page_drag_space_enabled_pattern = Pattern('customize_page_drag_space_enabled.png')
        drag_space_enabled_new_tab_pattern = Pattern('drag_space_enabled_new_tab.png')
        window_controls_restore_pattern = Pattern('window_controls_restore.png')
        window_controls_maximize_pattern = Pattern('window_controls_maximize.png')
        hamburger_menu_pattern = NavBar.HAMBURGER_MENU
        zoom_controls_customize_page_pattern = NavBar.ZOOM_CONTROLS_CUSTOMIZE_PAGE

        navigate('about:home')
        click_hamburger_menu_option('Customize...')

        region = Region(0, 0, Screen.SCREEN_WIDTH / 2, Screen.SCREEN_HEIGHT / 2)
        assert region.exists(zoom_controls_customize_page_pattern, 10), '\'Customize\' page successfully loaded.'
        assert exists(customize_page_drag_space_disabled_pattern, 10) and exists(drag_space_disabled_pattern, 10), \
            '\'Customize\' page is correctly displayed before \'drag space\' is enabled.'

        click(drag_space_disabled_pattern)
        assert exists(customize_page_drag_space_enabled_pattern, 10), \
            '\'Drag space\' successfully activated in the \'Customize\' page.'
        close_customize_page()

        new_tab()
        assert exists(drag_space_enabled_new_tab_pattern, 10), '\'Drag space\' successfully activated in a new tab.'

        if exists(hamburger_menu_pattern, 10):
            click_window_control('minimize', 'main')
            time.sleep(Settings.DEFAULT_UI_DELAY_LONG)
            try:
                assert wait_vanish(Tabs.NEW_TAB_NOT_HIGHLIGHTED, 10), 'Window successfully minimized.'
            except FindError:
                raise FindError('Window not minimized.')
        else:
            raise FindError('Can\'t find the \'hamburger menu\' in the page.')

        restore_window_from_taskbar()
        assert exists(hamburger_menu_pattern, 10), 'Window in view again.'

        if OSHelper.is_mac():
            logger.debug('Window size restore not applicable on OSX.')
        else:
            assert exists(window_controls_restore_pattern, 10), 'The window control \'restore\' is visible.'
            click_window_control('restore', 'main')
            assert exists(window_controls_maximize_pattern, 10), 'Window successfully restored.'

            click_window_control('maximize', 'main')
            assert exists(window_controls_restore_pattern, 10), 'Window successfully maximized.'

        if exists(hamburger_menu_pattern, 10):
            click_window_control('close', 'main')
            try:
                assert wait_vanish(NavBar.HOME_BUTTON.similar(0.9), 10), 'Window successfully closed.'
            except FindError:
                raise FindError('Window not closed')
        else:
            raise FindError('Can\'t find the \'hamburger menu\' in the page')

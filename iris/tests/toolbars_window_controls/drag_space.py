# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'This is a test case that checks that the drag space can be activated properly'
        self.test_case_id = '118184'
        self.test_suite_id = '1998'
        self.locales = ['en-US']
        # Feature not available on LINUX
        self.exclude = Platform.LINUX

    def run(self):
        url = 'about:home'
        customize_page_drag_space_disabled_pattern = Pattern('customize_page_drag_space_disabled.png')
        drag_space_disabled_pattern = Pattern('drag_space_disabled.png')
        customize_page_drag_space_enabled_pattern = Pattern('customize_page_drag_space_enabled.png')
        drag_space_enabled_new_tab_pattern = Pattern('drag_space_enabled_new_tab.png')
        window_controls_restore_pattern = Pattern('window_controls_restore.png')
        window_controls_maximize_pattern = Pattern('window_controls_maximize.png')
        hamburger_menu_pattern = NavBar.HAMBURGER_MENU
        zoom_controls_customize_page_pattern = NavBar.ZOOM_CONTROLS_CUSTOMIZE_PAGE

        navigate(url)
        click_hamburger_menu_option('Customize...')

        expected_1 = exists(zoom_controls_customize_page_pattern, 10,
                            in_region=Region(0, 0, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        assert_true(self, expected_1, '\'Customize\' page successfully loaded.')

        expected_2 = exists(customize_page_drag_space_disabled_pattern, 10) and exists(drag_space_disabled_pattern, 10)
        assert_true(self, expected_2, '\'Customize\' page is correctly displayed before \'drag space\' is enabled')
        click(drag_space_disabled_pattern)

        expected_3 = exists(customize_page_drag_space_enabled_pattern, 10)
        assert_true(self, expected_3, '\'Drag space\' successfully activated in the \'Customize\' page.')
        close_customize_page()

        new_tab()
        expected_4 = exists(drag_space_enabled_new_tab_pattern, 10)
        assert_true(self, expected_4, '\'Drag space\' successfully activated in a new tab.')

        if exists(hamburger_menu_pattern, 10):
            click_window_control('minimize', 'main')
            time.sleep(DEFAULT_UI_DELAY_LONG)
            try:
                expected_5 = wait_vanish(NavBar.HOME_BUTTON.similar(0.9), 10)
                assert_true(self, expected_5, 'Window successfully minimized')
            except FindError:
                raise FindError('Window not minimized.')
        else:
            raise FindError('Can\'t find the \'hamburger menu\' in the page.')

        restore_window_from_taskbar()

        expected_6 = exists(hamburger_menu_pattern, 10)
        assert_true(self, expected_6, 'Window in view again')

        if Settings.get_os() == Platform.MAC:
            logger.debug('Window size restore not applicable on OSX')
        else:
            expected_7 = exists(window_controls_restore_pattern, 10)
            assert_true(self, expected_7, 'The window control \'restore\' is visible')
            click_window_control('restore', 'main')

            expected_8 = exists(window_controls_maximize_pattern, 10)
            assert_true(self, expected_8, 'Window successfully restored')

            click_window_control('maximize', 'main')
            expected_9 = exists(window_controls_restore_pattern, 10)
            assert_true(self, expected_9, 'Window successfully maximized')

        if exists(hamburger_menu_pattern, 10):
            click_window_control('close', 'main')
            try:
                expected_11 = wait_vanish(NavBar.HOME_BUTTON.similar(0.9), 10)
                assert_true(self, expected_11, 'Window successfully closed')
            except FindError:
                raise FindError('Window not closed')
        else:
            raise FindError('Can\'t find the \'hamburger menu\' in the page')

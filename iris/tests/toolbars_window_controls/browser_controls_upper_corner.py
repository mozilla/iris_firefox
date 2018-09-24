# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This is a test case that checks that the upper corner browser controls work as expected'
        self.test_case_id = '120464'
        self.test_suite_id = '1998'

    def run(self):
        url = 'about:home'
        window_controls_minimize_pattern = Pattern('window_controls_minimize.png')
        hover_minimize_control_pattern = Pattern('hover_minimize_control.png')
        window_controls_restore_pattern = Pattern('window_controls_restore.png')
        hover_restore_control_pattern = Pattern('hover_restore_control.png')
        window_controls_maximize_pattern = Pattern('window_controls_maximize.png')
        hover_maximize_control_pattern = Pattern('hover_maximize_control.png')
        window_controls_close_pattern = Pattern('window_controls_close.png')
        hover_close_control_pattern = Pattern('hover_close_control.png')
        hamburger_menu_pattern = NavBar.HAMBURGER_MENU

        navigate(url)
        time.sleep(Settings.UI_DELAY_LONG)

        hover(window_controls_minimize_pattern)
        expected = exists(hover_minimize_control_pattern, 10)
        assert_true(self, expected, 'Hover over the \'minimize\' button works correctly.')

        if Settings.get_os() == Platform.WINDOWS or Settings.get_os() == Platform.LINUX:
            hover(window_controls_restore_pattern)
            expected = exists(hover_restore_control_pattern, 10)
            assert_true(self, expected, 'Hover over the \'restore\' button works correctly.')

        if Settings.get_os() == Platform.MAC:
            middle = find(hover_maximize_control_pattern)
            hover(Location(middle.x + 10, middle.y + 5))
            expected = exists(hover_maximize_control_pattern, 10)
            assert_true(self, expected, 'Hover over the \'maximize\' button works correctly.')

            hover(Location(middle.x - 10, middle.y + 5))
            expected = exists(hover_close_control_pattern, 10)
            assert_true(self, expected, 'Hover over the \'close\' button works correctly.')
        else:
            hover(window_controls_close_pattern)
            expected = exists(hover_close_control_pattern, 10)
            assert_true(self, expected, 'Hover over the \'close\' button works correctly.')

        if Settings.get_os() == Platform.WINDOWS or Settings.get_os() == Platform.LINUX:
            minimize_window()
            time.sleep(Settings.UI_DELAY)
            hover(window_controls_maximize_pattern)
            expected = exists(hover_maximize_control_pattern, 10)
            assert_true(self, expected,
                        'Hover over the \'maximize\' button works correctly; Window successfully restored.')

        if Settings.get_os() == Platform.LINUX:
            click(window_controls_minimize_pattern)
        else:
            expected = exists(hamburger_menu_pattern, 10)
            assert_true(self, expected, 'Found \'hamburger menu\'')

            minimize_window()
            time.sleep(Settings.UI_DELAY)
            expected = False
            try:
                expected = wait_vanish(hamburger_menu_pattern, 10)
            except FindError:
                logger.error('Window not minimized.')
            assert_true(self, expected, 'Window successfully minimized.')

        restore_window_from_taskbar()
        if Settings.get_os() == Platform.WINDOWS:
            maximize_window()

        expected = exists(hamburger_menu_pattern, 10)
        assert_true(self, expected, 'Window successfully opened again.')

        hover(hamburger_menu_pattern)
        time.sleep(Settings.FX_DELAY)

        close_window()
        time.sleep(Settings.FX_DELAY)
        type(Key.ENTER)
        try:
            expected = wait_vanish(hamburger_menu_pattern, 10)
            assert_true(self, expected, 'Window successfully closed.')
        except FindError:
            assert_true(self, False, 'Window successfully closed.')

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Browser controls work as expected.'
        self.test_case_id = '119481'
        self.test_suite_id = '1998'
        self.locales = ['en-US']

    def run(self):
        window_controls_minimize_pattern = Pattern('window_controls_minimize.png')
        hover_minimize_control_pattern = Pattern('hover_minimize_control.png')
        window_controls_restore_pattern = Pattern('window_controls_restore.png')
        hover_restore_control_pattern = Pattern('hover_restore_control.png')
        window_controls_maximize_pattern = Pattern('window_controls_maximize.png')
        hover_maximize_control_pattern = Pattern('hover_maximize_control.png')
        window_controls_close_pattern = Pattern('window_controls_close.png')
        hover_close_control_pattern = Pattern('hover_close_control.png')

        navigate(LocalWeb.FIREFOX_TEST_SITE)
        expected = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert_true(self, expected, 'Page successfully loaded, firefox logo found.')

        hover(window_controls_minimize_pattern)
        expected = exists(hover_minimize_control_pattern, 10)
        assert_true(self, expected, 'Hover over the \'minimize\' button works correctly.')

        if Settings.get_os() == Platform.WINDOWS or Settings.get_os() == Platform.LINUX:
            hover(window_controls_restore_pattern)
            expected = exists(hover_restore_control_pattern, 10)
            assert_true(self, expected, 'Hover over the \'restore\' button works correctly.')

        if Settings.get_os() == Platform.MAC:
            middle = find(hover_maximize_control_pattern)
            hover(Location(middle.x + 7, middle.y + 5))
            expected = exists(hover_maximize_control_pattern, 10)
            assert_true(self, expected, 'Hover over the \'maximize\' button works correctly.')

            hover(Location(middle.x - 35, middle.y + 5))
            expected = exists(hover_close_control_pattern, 10)
            assert_true(self, expected, 'Hover over the \'close\' button works correctly.')
        else:
            hover(window_controls_close_pattern)
            expected = exists(hover_close_control_pattern, 10)
            assert_true(self, expected, 'Hover over the \'close\' button works correctly.')

        if Settings.get_os() == Platform.WINDOWS or Settings.get_os() == Platform.LINUX:
            click_window_control('restore', 'main')
            time.sleep(Settings.UI_DELAY)
            hover(window_controls_maximize_pattern)
            expected = exists(hover_maximize_control_pattern, 10)
            assert_true(self, expected,
                        'Hover over the \'maximize\' button works correctly; Window successfully restored.')
        if Settings.is_mac():
            mouse_move(Pattern('home_button.png'))
        click_window_control('minimize', 'main')
        time.sleep(Settings.UI_DELAY)

        try:
            expected = wait_vanish(LocalWeb.FIREFOX_LOGO, 10)
        except FindError:
            raise FindError('Window not minimized.')
        assert_true(self, expected, 'Window successfully minimized.')

        restore_window_from_taskbar()

        if Settings.get_os() == Platform.WINDOWS:
            click_window_control('maximize', 'main')

        expected = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert_true(self, expected, 'Window successfully opened again.')

        click_window_control('close', 'main')

        try:
            expected = wait_vanish(LocalWeb.FIREFOX_LOGO, 10)
            assert_true(self, expected, 'Window successfully closed.')
        except FindError:
            assert_true(self, False, 'Window successfully closed.')

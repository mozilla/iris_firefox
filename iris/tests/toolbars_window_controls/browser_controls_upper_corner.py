# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This is a test case that checks that the upper corner browser controls work as expected'

    def run(self):
        url = 'about:home'
        window_controls_minimize = 'window_controls_minimize.png'
        hover_minimize_control = 'hover_minimize_control.png'
        window_controls_restore = 'window_controls_restore.png'
        hover_restore_control = 'hover_restore_control.png'
        window_controls_maximize = 'window_controls_maximize.png'
        hover_maximize_control = 'hover_maximize_control.png'
        window_controls_close = 'window_controls_close.png'
        hover_close_control = 'hover_close_control.png'
        hamburger_menu = 'hamburger_menu.png'

        navigate(url)
        time.sleep(Settings.UI_DELAY_LONG)

        hover(window_controls_minimize)
        expected = exists(hover_minimize_control, 10)
        assert_true(self, expected, 'Hover over the \'minimize\' button works correctly.')

        if Settings.get_os() == Platform.WINDOWS or Settings.get_os() == Platform.LINUX:
            hover(window_controls_restore)
            expected = exists(hover_restore_control, 10)
            assert_true(self, expected, 'Hover over the \'restore\' button works correctly.')

        if Settings.get_os() == Platform.MAC:
            middle = find(hover_maximize_control)
            hover(Location(middle.x + 10, middle.y + 5))
            expected = exists(hover_maximize_control, 10)
            assert_true(self, expected, 'Hover over the \'maximize\' button works correctly.')

            hover(Location(middle.x - 10, middle.y + 5))
            expected = exists(hover_close_control, 10)
            assert_true(self, expected, 'Hover over the \'close\' button works correctly.')
        else:
            hover(window_controls_close)
            expected = exists(hover_close_control, 10)
            assert_true(self, expected, 'Hover over the \'close\' button works correctly.')

        if Settings.get_os() == Platform.WINDOWS or Settings.get_os() == Platform.LINUX:
            # Restore window
            minimize_window()
            time.sleep(Settings.UI_DELAY)
            hover(window_controls_maximize)
            expected = exists(hover_maximize_control, 10)
            assert_true(self, expected,
                        'Hover over the \'maximize\' button works correctly; Window successfully restored.')

        if Settings.get_os() == Platform.LINUX:
            # Minimize window
            click(window_controls_minimize)
        else:
            expected = exists(hamburger_menu, 10)
            assert_true(self, expected, 'Found \'hamburger menu\'')

            # Minimize window
            minimize_window()
            expected = False
            try:
                expected = wait_vanish(hamburger_menu, 10)
            except Exception as error:
                logger.error('Window not minimized.')
            assert_true(self, expected, 'Window successfully minimized.')

        # Focus on Firefox and open the browser again
        restore_window_from_taskbar()
        if Settings.get_os() == Platform.WINDOWS:
            maximize_window()

        expected = exists(hamburger_menu, 10)
        assert_true(self, expected, 'Window successfully opened again.')

        # Make sure that focus is on the browser
        hover(hamburger_menu)
        time.sleep(Settings.FX_DELAY)

        # Close the window
        close_window()
        time.sleep(Settings.FX_DELAY)
        type(Key.ENTER)
        try:
            expected = wait_vanish(hamburger_menu, 10)
            assert_true(self, expected, 'Window successfully closed.')
        except Exception as error:
            assert_true(self, False, 'Window successfully closed.')

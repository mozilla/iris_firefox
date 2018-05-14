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

        hover(window_controls_minimize)
        time.sleep(0.5)

        expected = exists(hover_minimize_control, 10)
        assert_true(self, expected, 'Hover over the \'minimize\' button works correctly.')

        if Settings.getOS() == Platform.WINDOWS or Settings.getOS() == Platform.LINUX:
            hover(window_controls_restore)
            time.sleep(0.5)
            expected = exists(hover_restore_control, 10)
            assert_true(self, expected, 'Hover over the \'restore\' button works correctly.')

        if Settings.getOS() == Platform.MAC:
            middle = find(hover_maximize_control)
            hover(Location(middle.x + 10, middle.y + 5))
            time.sleep(1)

            expected = exists(hover_maximize_control, 10)
            assert_true(self, expected, 'Hover over the \'maximize\' button works correctly.')

            hover(Location(middle.x - 10, middle.y + 5))
            time.sleep(1)

            expected = exists(hover_close_control, 10)
            assert_true(self, expected, 'Hover over the \'close\' button works correctly.')
        else:
            hover(window_controls_close)
            expected = exists(hover_close_control, 10)
            assert_true(self, expected, 'Hover over the \'close\' button works correctly.')
            time.sleep(0.5)

        if Settings.getOS() == Platform.WINDOWS or Settings.getOS() == Platform.LINUX:
            # Restore window
            minimize_window()
            time.sleep(1)
            hover(window_controls_maximize)
            time.sleep(0.5)
            expected = exists(hover_maximize_control, 10)
            assert_true(self, expected,
                        'Hover over the \'maximize\' button works correctly; Window successfully restored.')

        if get_os() == 'linux':
            # Minimize window
            click(window_controls_minimize)
            time.sleep(0.5)
        else:
            if exists(hamburger_menu, 10):
                # Minimize window
                minimize_window()
                time.sleep(0.5)
                try:
                    expected = waitVanish(hamburger_menu, 10)
                    assert_true(self, expected, 'Window successfully minimized.')
                except Exception as error:
                    logger.error('Window not minimized.')
                    raise error
            else:
                logger.error('Can\'t find the \'hamburger menu\' in the page.')

        # Focus on Firefox and open the browser again
        restore_window_from_taskbar()
        if get_os() == 'linux':
            time.sleep(0.5)
        elif get_os() == 'win':
            maximize_window()
            time.sleep(0.5)

        expected = exists(hamburger_menu, 10)
        assert_true(self, expected, 'Window successfully opened again.')

        # Close the window
        close_window()
        time.sleep(0.5)
        type(Key.ENTER)
        time.sleep(0.5)
        try:
            expected = waitVanish(hamburger_menu, 10)
            assert_true(self, expected, 'Window successfully closed.')
        except Exception as error:
            logger.error('Window not closed.')
            raise error

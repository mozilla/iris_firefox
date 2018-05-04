# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This is a test case that checks that the drag space can be activated properly'

    def run(self):
        url = 'about:home'
        customize_page_drag_space_disabled = 'customize_page_drag_space_disabled.png'
        drag_space_disabled = 'drag_space_disabled.png'
        customize_page_drag_space_enabled = 'customize_page_drag_space_enabled.png'
        drag_space_enabled_new_tab = 'drag_space_enabled_new_tab.png'
        hamburger_menu = 'hamburger_menu.png'
        window_controls_restore = 'window_controls_restore.png'
        window_controls_maximize = 'window_controls_maximize.png'
        close_multiple_tabs_warning = 'close_multiple_tabs_warning.png'

        navigate(url)

        # Open Customize from the Hamburger Menu
        click_hamburger_menu_option('Customize...')
        time.sleep(1)

        # Check that the customize page is opened by searcing for text "Drag"
        try:
            expected_1 = wait('Drag', 10)
            assert_true(self, expected_1, 'customize page present.')
        except Exception as error:
            logger.error('Can\'t find Drag text.')
            raise error
        else:
            if exists(customize_page_drag_space_disabled, 10) and exists(drag_space_disabled, 10):
                click(drag_space_disabled)
                if exists(customize_page_drag_space_enabled) and not exists(drag_space_disabled, 1):
                    logger.debug('drag space successfully activated in the Customize page')
                else:
                    logger.error('drag space not properly activated')
            else:
                logger.error('Customize page is not correctly displayed before drag space is enabled')
            close_customize_page()

            # Check that changes persist in a new tab
            new_tab()
            if exists(drag_space_enabled_new_tab):
                logger.debug('drag space successfully activated in a new tab')
            else:
                logger.debug('drag space not correctly activated in a new tab')

            if exists(hamburger_menu, 10):
                # Minimize window
                minimize_window()
                if get_os() == "win":
                    time.sleep(0.5)
                    minimize_window()
                    time.sleep(1)
                try:
                    expected_2 = waitVanish(hamburger_menu, 10)
                    assert_true(self, expected_2, 'window successfully minimized')
                except Exception as error:
                    logger.error('window not minimized.')
                    raise error
            else:
                logger.error('Can\'t find the hamburger menu in the page.')

            # Focus on Firefox and open the browser again
            restore_window_from_taskbar()
            maximize_window()
            if exists(hamburger_menu, 10):
                logger.debug('window in view again')
            else:
                logger.error('window not in view.')

            # Restore window (applies to Windows and Linux)
            if get_os() =="osx":
                logger.debug ('Window size restore not applicable on OSX')
            else:
                if exists(window_controls_restore, 10):
                    minimize_window()
                    if exists(window_controls_maximize, 10):
                        logger.debug('window successfully restored')
                        # Maximize window
                        maximize_window()
                        if exists(window_controls_restore, 10):
                            logger.debug('window successfully maximized')
                        else:
                            logger.error('window not maximized')
                    else:
                        logger.error('window not restored')
                else:
                    logger.error('the window control restore not visible')

            # Close the window
            if exists(hamburger_menu, 10):
                close_window()
                time.sleep(1)
                if exists(close_multiple_tabs_warning, 10):
                    logger.debug('Close multiple tabs warning')
                    click(close_multiple_tabs_warning)
                try:
                    expected_3 =  waitVanish(hamburger_menu, 10)
                    assert_true(self, expected_3, 'window successfully closed')
                except Exception as error:
                    logger.error('window not closed')
                    raise error
            else:
                logger.error('Can\'t find the hamburger menu in the page')


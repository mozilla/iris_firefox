# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.assets = os.path.join(os.path.split(__file__)[0], "assets")
        self.meta = "This is a test case that checks that Browser Control Console work as expected"
        self.test_case_id = '119481'
        self.test_suite_id = '1998'
        self.locales = ['en-US']

        # Disabling until test has been updated
        self.exclude = Platform.ALL

    def run(self):

        url = "about:home"
        navigate(url)
        pop_up_region = click_hamburger_menu_option("Web Developer")
        pop_up_region.click("Web Console")
        time.sleep(Settings.UI_DELAY_LONG)

        developer_menu_message = 'Console '
        screen = get_screen()
        left_corner_screen_region = Sikuli.Region(screen.x(), screen.height() / 2, screen.width() / 2, screen.height())

        if left_corner_screen_region.exists(developer_menu_message, 5):
            logger.debug('Developer Console is displayed')

            # Open a console from developer tool command line.
            console_command = 'window.alert("test alert")'

            type(console_command)
            type(Key.ENTER)

            # Check if one of the Developer console tabs are displayed.
            pop_up_message = 'test'
            found = False
            center_screen = Sikuli.Region(screen.x() + 100, screen.y() + 100, screen.width(), screen.height() / 2)
            center_screen.highlight(2)
            if pop_up_message in center_screen.text():
                logger.debug('Item is present: ' + pop_up_message)
                found = True

            if found:
                logger.debug('Pop up message is displayed ')
                type(Key.ENTER)
                logger.debug('Pop up message is closed ')
                open_browser_console()
                logger.debug('Opening browser console with keyboard shortcut ')

                console_items = ['Net', 'CSS', 'JS', 'Security']
                browser_console_items = False
                for word in console_items:
                    if word in center_screen.text():
                        logger.debug('Item is present: ' + word)
                        browser_console_items = True

                if browser_console_items:
                    logger.debug('Close console')
                    center_screen.click('auxiliary_window_close_button.png')
                    time.sleep(1)
                    if center_screen.exists('auxiliary_window_close_button.png', 5):
                        logger.error('Browser Console was not closed')
                        print "FAIL"
                    else:
                        logger.debug('Browser console is closed')
                        open_browser_console()
                        if exists('auxiliary_window_close_button.png', 5):
                            logger.debug('Browser Console was reopened successfully')
                            if center_screen.exists('auxiliary_window_minimize.png', 5):
                                center_screen.click('auxiliary_window_minimize.png')
                                logger.debug('Browser Console is minimized')
                                open_browser_console()
                                if center_screen.exists('auxiliary_window_maximize.png', 5):
                                    center_screen.click('auxiliary_window_maximize.png')
                                    logger.debug('Browser Console is maximized')
                                    if Settings.get_os() == Platform.MAC:
                                        screen.click('auxiliary_window_close_button.png')
                                    else:
                                        force_close()
                                    print "PASS"
                                else:
                                    logger.error('Browser Console was not maximized')
                            else:
                                logger.error('Browser Console was not minimized')
                        else:
                            logger.error('Browser Console was not been reopened successfully')

            else:
                logger.error('Developer console is not open')
                print "Fail"
        else:

            logger.error('Developer toolbar is NOT opened ')
            print "FAIL"

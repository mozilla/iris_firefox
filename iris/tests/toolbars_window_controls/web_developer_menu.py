# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from test_case import *


class test(base_test):

    def __init__(self, app):
        base_test.__init__(self, app)
        base_test.set_image_path(self, os.path.split(__file__)[0])
        self.assets = os.path.join(os.path.split(__file__)[0], "assets")
        self.meta = "This is a test case that checks that Developer Toolbar controls work as expected"

    def run(self):

        url = "about:home"
        navigate(url)

        pop_up_region = click_hamburger_menu_option("Web Developer")
        pop_up_region.click("Developer Toolbar")
        # time.sleep(5)

        screen = get_screen()
        left_corner_screen_region = Sikuli.Region(screen.getX(), screen.getH()/2, screen.getW()/2, screen.getH())

        # left_corner_screen_region.highlight(5)
        right_corner_region = Sikuli.Region(screen.getW()/2, screen.getH()/2, screen.getW()/2, screen.getH()/2)
        # right_corner_region.highlight(5)

        if left_corner_screen_region.exists('web_developer_insert.png', 5):
            logger.debug('Developer toolbar is opened')
            if Settings.getOS() == Platform.MAC:
                left_corner_screen_region.click('web_developer_close_button.png')
                logger.debug('Closing web developer bar')

            else:

                # right_corner_region.highlight(3)
                right_corner_region.click('web_developer_close_button.png')
                logger.debug('Closing web developer bar')
            if Settings.getOS() == Platform.MAC:
                if left_corner_screen_region.waitVanish('web_developer_close_button.png', 5):
                    logger.debug('Web developer bar was closed')
                    open_web_developer_menu()
                    time.sleep(3)
                    # open a console from developer tool command line to check the functionality
                    open_console = 'console open'
                    paste(open_console)
                    type(Key.ENTER)
                    console_items = ['Inspector', 'Debugger', 'Console']
                    found = False
                    for word in console_items:
                        if word in left_corner_screen_region.text():
                            logger.debug('Item is present: '+word)
                            # left_corner_screen_region.highlight(2)
                            found = True

                    if found:
                        logger.debug('Developer console is open and all the tabs are present')
                        print "PASS"
                    else:
                        logger.error('Developer console is not open')
                        print 'FAIL'
                else:
                    logger.error('Web developer bar was not closed')
                    print 'FAIL'
            else:
                if right_corner_region.waitVanish('web_developer_close_button.png', 7):
                    # right_corner_region.highlight(2)
                    logger.debug('Web developer bar was closed')
                    open_web_developer_menu()
                    logger.debug('Web developer bar was reopened')
                    # open a console from developer tool command line to check the functionality
                    open_console = 'console open'
                    time.sleep(5)
                    paste(open_console)
                    type(Key.ENTER)
                    logger.debug('Opening console from command line')
                    # time.sleep(5)
                    # check if one of the Developer console tabs are displayed to be sure that the console is opened
                    console_items = ['Inspector', 'Debugger', 'Console']
                    found = False
                    for word in console_items:
                        if word in left_corner_screen_region.text():
                            logger.debug('Item is present: '+word)
                            # left_corner_screen_region.highlight(2)
                            found = True
                    if found:
                        logger.debug('Developer console is open and all the tabs are present')
                        print "PASS"
                    else:
                        logger.error('Developer console is not open')
                        print "Fail"
        else:
            logger.debug('Web developer bar was NOT closed')
            print 'FAIL'

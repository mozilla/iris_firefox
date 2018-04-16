# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from test_case import *


class test(base_test):

    def __init__(self, app):
        base_test.__init__(self, app)
        base_test.set_image_path(self, os.path.split(__file__)[0])
        self.assets = os.path.join(os.path.split(__file__)[0], "assets")
        self.meta = "This is a test case that checks that Browser Control Console work as expected"

    def run(self):

        url = "about:home"
        navigate(url)
        pop_up_region=click_hamburger_menu_option("Web Developer")
        pop_up_region.click("Web Console")
        time.sleep(5)

        developer_menu_message='Console '
        screen=get_screen()
        left_corner_screen_region=Sikuli.Region(screen.getX(),screen.getH()/2,screen.getW()/2,screen.getH())


        if left_corner_screen_region.exists(developer_menu_message,5):
            logger.debug('Developer Console is displayed')

            #open a console from developer tool command line

            console_command='window.alert("test alert")'

            type(console_command)
            type(Key.ENTER)

            #check if one of the Developer console tabs are displayed
            pop_up_message='test'
            found=False
            center_screen=Sikuli.Region(screen.getX()+100,screen.getY()+100,screen.getW(),screen.getH()/2)
            center_screen.highlight(2)
            if pop_up_message in center_screen.text():
                logger.debug('Item is present: '+pop_up_message)
                found=True

            if found:
                logger.debug('Pop up message is displayed ')
                type(Key.ENTER)
                logger.debug('Pop up message is closed ')

                open_web_console()
                logger.debug('Opening web console with keyboard shortcut ')

                console_items=['Net','CSS','JS','Security']
                web_console_items=False
                for word in console_items:
                    if word in center_screen.text():
                        logger.debug('Item is present: '+word)
                        web_console_items=True

                if web_console_items:
                    logger.debug('Close console')
                    center_screen.click('web_console_close_button.png')
                    time.sleep(3)
                    if center_screen.exists('web_console_close_button.png',2):
                        logger.error('Web Console was not closed')
                        print "FAIL"
                    else:
                        logger.debug('Web console is closed')
                        open_web_console()
                        if exists('web_console_close_button.png',5):
                            logger.debug('Web Console was reopened successfully')
                            if center_screen.exists('web_console_minimize.png',5):
                                center_screen.click('web_console_minimize.png')
                                logger.debug('Web Console is minimized')
                                open_web_console()
                                if center_screen.exists('web_console_maximize.png',5):
                                    center_screen.click('web_console_maximize.png')
                                    logger.debug('Web Console is maximized')
                                    print "PASS"
                                    time.sleep(3)
                                else:
                                    logger.error('Web Console was not maximized')

                            else:
                                logger.error('Web Console was not minimized')


                        else:
                            logger.error('Web Console was not been reopened successfully')

            else:
                logger.error('Developer console is not open')
                print "Fail"
        else:
            logger.error('Developer toolbar  is NOT opened ')
            print "FAIL"









# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):
    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = "This is a test case that checks that Developer Toolbar controls work as expected"

    def run(self):

        url = "about:home"
        navigate(url)

        open_web_developer_menu()
        screen = get_screen()
        left_corner_screen_region = Region(screen.getX(), screen.getH() / 2, screen.getW() / 2, screen.getH() / 2)
        right_corner_region = Region(screen.getW() / 2, screen.getH() / 2, screen.getW() / 2, screen.getH() / 2)

        web_developer_text_assert = screen.exists('web_developer_insert.png', 10)
        assert_true(self, web_developer_text_assert, 'Web developer bar is present')
        if Settings.getOS() == Platform.MAC:
            left_corner_screen_region.click('web_developer_close_button.png')
            logger.debug('Closing web developer bar')
        else:
            right_corner_region.click('web_developer_close_button.png')
            logger.debug('Closing web developer bar')
        if Settings.getOS() == Platform.MAC:
            close_button_assert = left_corner_screen_region.waitVanish('web_developer_close_button.png', 5)
            assert_true(self, close_button_assert, 'Bar was closed')
            open_web_developer_menu()
            time.sleep(3)
            open_console = 'console open'
            paste(open_console)
            type(Key.ENTER)
            console_items = ['Inspector', 'Debugger', 'Console', 'Performance', 'Memory']
            found = False
            resized_region = Region(left_corner_screen_region.getX(), left_corner_screen_region.getY() - 100,
                                    left_corner_screen_region.getW(), left_corner_screen_region.getH())
            for word in console_items:
                if word in resized_region.text():
                    logger.debug('Item is present: ' + word)
                    found = True
            assert_true(self, found, 'Text found')
        else:
            developer_close_button_assert = right_corner_region.waitVanish('web_developer_close_button.png', 4)
            assert_true(self, developer_close_button_assert, 'Web developer bar was closed')
            open_web_developer_menu()
            # open a console from developer tool command line to check the functionality
            open_console = 'console open'
            time.sleep(5)
            paste(open_console)
            type(Key.ENTER)
            logger.debug('Opening console from command line')
            # check if one of the Developer console tabs are displayed to be sure that the console is opened
            console_items = ['Inspector', 'Debugger', 'Console', 'Performance', 'Memory','Network','Storage']
            found = False
            for word in console_items:
                if word in left_corner_screen_region.text():
                    logger.debug('Item is present: ' + word)
                    found = True
            assert_true(self, found, 'Text found')

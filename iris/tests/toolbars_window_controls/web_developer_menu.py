# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):
    def __init__(self):
        BaseTest.__init__(self)
        self.meta = "This is a test case that checks that Developer Toolbar controls work as expected."
        # Skipping test from running since the 'Developer Toolbar' has been removed from Firefox 62. See more details
        # here https://developer.mozilla.org/en-US/docs/Tools/GCLI
        self.test_case_id = '119483'
        self.test_suite_id = '1998'
        self.locales = ['en-US']
        self.exclude = Platform.ALL

    def run(self):

        navigate("about:home")

        open_web_developer_menu()
        screen = get_screen()
        left_corner_screen_region = Region(screen.x, screen.height / 2, screen.width / 2, screen.height / 2)
        right_corner_region = Region(screen.width / 2, screen.height / 2, screen.width / 2, screen.height / 2)

        web_developer_text_assert = screen.exists(Pattern('web_developer_insert.png'), 10)
        assert_true(self, web_developer_text_assert, 'Web developer bar is present.')
        if Settings.get_os() == Platform.MAC:
            left_corner_screen_region.click(Pattern('web_developer_close_button.png'))
            logger.debug('Closing web developer bar.')
        else:
            right_corner_region.click(Pattern('web_developer_close_button.png'))
            logger.debug('Closing web developer bar.')
        if Settings.get_os() == Platform.MAC:
            close_button_assert = left_corner_screen_region.wait_vanish(Pattern('web_developer_close_button.png'), 5)
            assert_true(self, close_button_assert, 'Bar was closed.')
            open_web_developer_menu()
            time.sleep(Settings.UI_DELAY_LONG)
            open_console = 'console open'
            paste(open_console)
            type(Key.ENTER)
            console_items = ['Inspector', 'Debugger', 'Console', 'Performance', 'Memory']
            found = False
            resized_region = Region(left_corner_screen_region.x, left_corner_screen_region.y - 100,
                                    left_corner_screen_region.width, left_corner_screen_region.height)
            for word in console_items:
                if word in resized_region.text():
                    logger.debug('Item is present: ' + word)
                    found = True
            assert_true(self, found, 'Text found.')
        else:
            dev_close_button_assert = right_corner_region.wait_vanish(Pattern('web_developer_close_button.png'), 4)
            assert_true(self, dev_close_button_assert, 'Web developer bar was closed.')
            open_web_developer_menu()
            # open a console from developer tool command line to check the functionality
            open_console = 'console open'
            time.sleep(Settings.UI_DELAY_LONG)
            paste(open_console)
            type(Key.ENTER)
            logger.debug('Opening console from command line.')
            # check if one of the Developer console tabs are displayed to be sure that the console is opened
            console_items = ['Inspector', 'Debugger', 'Console', 'Performance', 'Memory', 'Network', 'Storage']
            found = False
            for word in console_items:
                if word in left_corner_screen_region.text():
                    logger.debug('Item is present: ' + word)
                    found = True
            assert_true(self, found, 'Text found.')

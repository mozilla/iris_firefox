# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Drop html data in demopage'
        self.test_case_id = '165088'
        self.test_suite_id = '102'
        self.locale = ['en-US']

    def run(self):

        # iris_tab_pattern = Pattern('eyes.ico')
        # time.sleep(30)
        # restore_firefox_focus()
        change_preference('devtools.chrome.enabled', True)
        minimize_window()
        open_browser_console()
        paste('window.resizeTo({0}, {1})'.format(SCREEN_WIDTH/2, SCREEN_HEIGHT))
        type(Key.ENTER)
        close_tab()
        # start_offset = NavBar.HOME_BUTTON.get_size()[0]
        # start_position = find(NavBar.HOME_BUTTON).offset(start_offset*2, 0)
        # window_drop_position = Location(10, SCREEN_WIDTH/10)
        # drag_drop(start_position, window_drop_position)
        # iris_tab = find(iris_tab_pattern)
        # drag_drop(iris_tab, Location(0, SCREEN_HEIGHT/2))
        navigate('https://mystor.github.io/dragndrop/')
        new_window()
        opened_tab_location = find(Tabs.NEW_TAB_HIGHLIGHTED)
        new_window_drop_location = Location(SCREEN_WIDTH/2, SCREEN_HEIGHT/20)
        drag_drop(opened_tab_location, new_window_drop_location)
        navigate('https://en.wikipedia.org/wiki/Firefox')
        time.sleep(5)
        close_window()

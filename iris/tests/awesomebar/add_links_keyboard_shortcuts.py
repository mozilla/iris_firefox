# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This test case adds links using \'CTRL/CMD\' + \'ENTER\' keys.'
        self.test_case_id = '119484'
        self.test_suite_id = '1902'

    def run(self):
        cnn_tab_pattern = Pattern('cnn_tab.png')
        cnn_icon_pattern = Pattern('cnn_icon.png')
        facebook_tab_pattern = Pattern('facebook_tab.png')

        region = Region(0, 0, SCREEN_WIDTH, 2 * SCREEN_HEIGHT / 3)

        # Navigate to the 'CNN' page using the 'CTRL'/'CMD' + 'ENTER' keys starting from the name of the page.
        select_location_bar()
        type('cnn')

        if Settings.get_os() == Platform.WINDOWS or Settings.get_os() == Platform.LINUX:
            key_down(Key.CTRL)
            type(Key.ENTER)
            key_up(Key.CTRL)
        else:
            key_down(Key.CMD)
            type(Key.ENTER)
            key_up(Key.CMD)

        expected = region.exists(cnn_tab_pattern, 10) and region.exists(cnn_icon_pattern, 10)
        assert_true(self, expected, 'CNN page successfully loaded .')

        # In a new tab, navigate to the 'Facebook' page using the 'CTRL'/'CMD' + 'ENTER' keys starting from the name of
        # the page.
        new_tab()

        select_location_bar()
        type('facebook')

        if Settings.get_os() == Platform.WINDOWS or Settings.get_os() == Platform.LINUX:
            key_down(Key.CTRL)
            type(Key.ENTER)
            key_up(Key.CTRL)
        else:
            key_down(Key.CMD)
            type(Key.ENTER)
            key_up(Key.CMD)

        expected = region.exists(facebook_tab_pattern, 10)
        assert_true(self, expected, 'Facebook page successfully loaded.')

        # Navigate to the previous tab and press 'CTRL'/'CMD' + 'ENTER' keys in the address bar.
        previous_tab()
        select_location_bar()

        if Settings.get_os() == Platform.WINDOWS or Settings.get_os() == Platform.LINUX:
            key_down(Key.CTRL)
            type(Key.ENTER)
            key_up(Key.CTRL)
        else:
            key_down(Key.CMD)
            type(Key.ENTER)
            key_up(Key.CMD)

        expected = region.exists(cnn_tab_pattern, 10)
        assert_true(self, expected, 'CNN page successfully reloaded.')

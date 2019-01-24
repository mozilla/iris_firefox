# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'This test case adds links using \'CTRL\' + \'ENTER\' keys.'
        self.test_case_id = '119484'
        self.test_suite_id = '1902'
        self.locales = ['en-US']
        self.set_profile_pref({'browser.contentblocking.enabled': False})

    def run(self):
        cnn_tab_pattern = Pattern('cnn_tab.png')
        cnn_icon_pattern = Pattern('cnn_icon.png')
        facebook_tab_pattern = Pattern('facebook_tab.png')

        region = Region(0, 0, SCREEN_WIDTH, 2 * SCREEN_HEIGHT / 3)

        # Navigate to the 'CNN' page using the 'CTRL' + 'ENTER' keys starting from the name of the page.
        select_location_bar()
        paste('cnn')

        key_down(Key.CTRL)
        type(Key.ENTER)
        key_up(Key.CTRL)

        close_content_blocking_pop_up()

        expected = region.exists(cnn_tab_pattern, 15) and region.exists(cnn_icon_pattern, 10)
        assert_true(self, expected, 'CNN page successfully loaded .')

        # In a new tab, navigate to the 'Facebook' page using the 'CTRL' + 'ENTER' keys starting from the name of
        # the page.
        new_tab()

        select_location_bar()
        type('facebook')

        key_down(Key.CTRL)
        type(Key.ENTER)
        key_up(Key.CTRL)

        expected = region.exists(facebook_tab_pattern, 10)
        assert_true(self, expected, 'Facebook page successfully loaded.')

        # Navigate to the previous tab and press 'CTRL'/'CMD' + 'ENTER' keys in the address bar.
        previous_tab()
        select_location_bar()

        key_down(Key.CTRL)
        type(Key.ENTER)
        key_up(Key.CTRL)

        expected = region.exists(cnn_tab_pattern, 10)
        assert_true(self, expected, 'CNN page successfully reloaded.')

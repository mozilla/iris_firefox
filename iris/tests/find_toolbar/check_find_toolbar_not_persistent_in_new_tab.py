# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Check Find Toolbar is not persistent in a new tab / window'
        self.test_case_id = '127262'
        self.test_suite_id = '2085'
        self.locales = ['en-US']

    def run(self):
        new_tab_icon_pattern = Tabs.NEW_TAB_HIGHLIGHTED

        # Open Firefox and open the Find Toolbar
        open_find()
        edit_select_all()
        edit_delete()

        find_toolbar_is_opened = exists(FindToolbar.FINDBAR_TEXTBOX, 5)
        assert_true(self, find_toolbar_is_opened, 'The find toolbar is opened')

        # Open another tab
        new_tab()

        new_tab_is_opened = exists(new_tab_icon_pattern, 5)
        assert_true(self, new_tab_is_opened, 'New tab is opened')

        find_toolbar_is_opened = exists(FindToolbar.FINDBAR_TEXTBOX, 5)
        assert_false(self, find_toolbar_is_opened, 'The find toolbar is not opened on a new tab')

        # Open a new window
        new_window()

        new_tab_is_opened = exists(new_tab_icon_pattern, 5)
        assert_true(self, new_tab_is_opened, 'New tab is opened')

        find_toolbar_is_opened = exists(FindToolbar.FINDBAR_TEXTBOX, 5)
        assert_false(self, find_toolbar_is_opened, 'The find toolbar is not opened in a new window')

        close_window()

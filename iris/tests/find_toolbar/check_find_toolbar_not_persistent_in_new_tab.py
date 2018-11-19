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
        """
        TEST Check Find Toolbar is not persistent in a new tab / window

        STEP 1:
            DESCRIPTION:
                Open Firefox.

            EXPECTED:
                Firefox is opened.

        STEP 2:
            DESCRIPTION:
                Open the Find Toolbar (CTRL+F).

            EXPECTED:
                Find Toolbar is opened.

        STEP 3:
            DESCRIPTION:
                Open another tab.

            EXPECTED:
                Find Toolbar is not persistent on other tabs.

        STEP 4:
            DESCRIPTION:
                Open a new window (CTRL+N).

            EXPECTED:
                Find Toolbar is not persistent on the new opened window.

        NOTES:
            Initial version - Pavel Ciapa - 11-Nov-2018
            Code review complete - Paul Prokhorov - 16-Nov-2018
        """

        find_toolbar_pattern = Pattern('find_toolbar_text.png')
        new_tab_icon_pattern = Pattern('new_tab_icon.png')

        """
        STEP 1:
            DESCRIPTION: 
                Open Firefox.

            EXPECTED: 
                Firefox is opened.
        """

        # Step is done by the test framework

        """ END OF STEP 1 """

        """
        STEP 2:
           DESCRIPTION:
               Open the Find Toolbar (CTRL+F).
            
           EXPECTED:
               Find Toolbar is opened.
        """

        open_find()
        edit_select_all()
        edit_delete()

        find_toolbar_is_opened = wait(find_toolbar_pattern, 5)

        assert_true(self, find_toolbar_is_opened, 'The find toolbar is opened')

        """ END OF STEP 2 """

        """
        STEP 3: 
            DESCRIPTION:
                Open another tab.

            EXPECTED: 
                Find Toolbar is not persistent on other tabs.
        """

        new_tab()
        exists(new_tab_icon_pattern, 5)

        find_toolbar_is_opened = exists(find_toolbar_pattern, 2)

        assert_false(self, find_toolbar_is_opened, 'The find toolbar is not opened on a new tab')

        """ END OF STEP 3 """

        """
        STEP 4:
            DESCRIPTION:
                Open a new window (CTRL+N).
            
            EXPECTED: 
                Find Toolbar is not persistent on the new opened window.
        """

        new_window()
        exists(new_tab_icon_pattern, 5)

        find_toolbar_is_opened = exists(find_toolbar_pattern, 2)
        close_window()

        assert_false(self, find_toolbar_is_opened, 'The find toolbar is not opened in a new window')

        """ END OF STEP 4 """

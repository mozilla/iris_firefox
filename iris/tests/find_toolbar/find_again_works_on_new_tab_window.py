# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Check "Find Again" works on a new tab/window'
        self.test_case_id = '0'
        self.test_suite_id = '0'
        self.locales = ['en-US']

    def run(self):
        """
        Check "Find Again" works on a new tab/window

        STEP 1:
            DESCRIPTION:
                Open Firefox.

            EXPECTED:
                Firefox is successfully opened.

        STEP 2:
            DESCRIPTION:
                Open the Find Toolbar (CTRL+F).

            EXPECTED:
                Find Toolbar is opened.

        STEP 3:
            DESCRIPTION:
                Enter a search term (e.g. ""abc"").

            EXPECTED:
                The input shows the entered term.

        STEP 4:
            DESCRIPTION:
                Open another tab.

            EXPECTED:
                The tab is opened.

        STEP 5:
            DESCRIPTION:
                Open the Find Toolbar (CTRL+F).

            EXPECTED:
                Find Toolbar is opened and contains the term searched on step 3 ('abc').

        STEP 6:
            DESCRIPTION:
                Open a new window (CTRL+N).

            EXPECTED:
                New window is opened.

        STEP 7:
            DESCRIPTION:
                Open the Find Toolbar (CTRL+F).

            EXPECTED:
                Find Toolbar is opened and contains the term searched on step 3 ('abc').

        NOTES:
            Initial version - Pavel Ciapa  - 11-Nov-2018
            Test fails on Step 7 because find toolbar doesn't contain any text in new window - Paul Prokhorov - 16-Nov-2018
        """

        find_toolbar_pattern = Pattern('find_toolbar_text.png')
        new_tab_icon_pattern = Pattern('new_tab_icon.png')
        find_toolbar_abc_text_pattern = Pattern('find_toolbar_abc_text.png')
        find_toolbar_abc_text_hovered_pattern = Pattern('find_toolbar_abc_text_hovered.png')

        """ STEP 1 """

        # Step is done by the test framework

        """ END STEP 1 """

        """ STEP 2 """

        open_find()

        # Remove all text from the Find Toolbar
        edit_select_all()
        edit_delete()

        find_toolbar_is_opened = wait(find_toolbar_pattern, 5)

        assert_true(self, find_toolbar_is_opened, 'The find toolbar is opened')

        """ END STEP 2 """

        """ STEP 3 """

        type('abc')
        if Settings.get_os() == Platform.MAC:
            key_down(Key.ENTER)
            key_up(Key.ENTER)


        # When 'abc' doesn't appear on the page it has red highlight
        find_toolbar_abc_text_typed_red = exists(find_toolbar_abc_text_pattern, 5)

        assert_true(self, find_toolbar_abc_text_typed_red, 'The search term \'abc\' is typed into find toolbar.')

        """ END STEP 3 """

        """ STEP 4 """

        new_tab()
        new_tab_is_opened = exists(new_tab_icon_pattern)

        assert_true(self, new_tab_is_opened, "New tab is opened.")

        """ END STEP 4 """

        """ STEP 5 """

        open_find()

        find_toolbar_abc_text_hovered = exists(find_toolbar_abc_text_hovered_pattern)

        assert_true(self, find_toolbar_abc_text_hovered, 'The find toolbar is opened and contains search term \"abc\".')

        """ END STEP 5 """

        """ STEP 6 """

        new_window()

        new_window_is_opened = exists(new_tab_icon_pattern)

        assert_true(self, new_window_is_opened, "New window is opened.")

        """ END STEP 6 """

        """ STEP 7 """

        open_find()

        find_toolbar_abc_text_hovered = exists(find_toolbar_abc_text_hovered_pattern)

        assert_true(self, find_toolbar_abc_text_hovered, 'The find toolbar is opened and contains search term \"abc\".')

        """ END STEP 7 """

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Opens find toolbar'
        self.test_case_id = '0'
        self.test_suite_id = '0'
        self.locales = ['en-US']

    def run(self):
        """
        Opens find toolbar

        STEP 1:
            DESCRIPTION:
                Launch Firefox.

            EXPECTED:
                Firefox launches without any issues.

        STEP 2:
            DESCRIPTION:
                Open the Find Toolbar.
                1) by pressing CTRL + F / Cmd + F,
                2) Menu bar > Edit > Find in This Page,
                3) Menu > Find in This Page.

            EXPECTED:
                - Find Tollbar is opened at the bottom of the browser.
                - On the lower left corner you can find the search field.
                - 'Highlight All', 'Match Case' and 'Whole Words' buttons
                are displayed on the right side of the search field."

        NOTES:
            Initial version - Pavel Ciapa  - 11-Nov-2018
            Code review complete - Paul Prokhorov - 16-Nov-2018
        """

        find_toolbar_pattern = Pattern('find_toolbar_text.png')
        bttn_hl_all_pattern = Pattern('find_bttn_hl_all.png')
        bttn_match_case_pattern = Pattern('find_bttn_match_case.png')
        find_bttn_whole_words_pattern = Pattern('find_bttn_whole_words.png')

        menu_bar_edit_pattern = Pattern('menu_bar_edit_pattern.png')
        hamburger_menu_pattern = Pattern('hamburger_menu_pattern.png')
        hamburger_menu_find_in_page_pattern = Pattern('hamburger_menu_find_in_page_pattern.png')
        menu_bar_edit_find_in_page_pattern = Pattern('menu_bar_edit_find_in_page_pattern.png')

        """ STEP 1 """

        # Step is done by the test framework

        """ END STEP 1 """

        """ STEP 2 """

        # 1) by pressing CTRL + F / Cmd + F

        open_find()

        # Remove all text from the Find Toolbar
        edit_select_all()
        edit_delete()

        find_toolbar_is_opened = wait(find_toolbar_pattern, 5)

        assert_true(self, find_toolbar_is_opened, 'The Find Toolbar is successfully displayed '
                                                  'by pressing CTRL + F / Cmd + F,.')

        find_toolbar_x = find(find_toolbar_pattern).x
        bttn_hl_all_x = find(bttn_hl_all_pattern).x
        bttn_match_case_x = find(bttn_match_case_pattern).x
        find_bttn_whole_words_pattern_x = find(find_bttn_whole_words_pattern).x

        type(Key.ESC)
        wait_vanish(find_toolbar_pattern, 20)

        items_appear_in_proper_way = find_toolbar_x < bttn_hl_all_x < bttn_match_case_x < find_bttn_whole_words_pattern_x

        assert_true(self, items_appear_in_proper_way,
                    'The Buttons of Find toolbar are displayed in correct order.')

        # 2) Menu bar > Edit > Find in This Page,

        if Settings.get_os() == Platform.WINDOWS:
            key_down(Key.ALT)
            key_up(Key.ALT)

            wait(menu_bar_edit_pattern, 5)
            click(menu_bar_edit_pattern, 1)

            wait(menu_bar_edit_find_in_page_pattern, 3)
            click(menu_bar_edit_find_in_page_pattern, 1)

        if Settings.get_os() == Platform.MAC:
            type(Key.F2, KeyModifier.CTRL)
            type(Key.RIGHT)
            type(Key.RIGHT)
            type(Key.RIGHT)
            type(Key.DOWN)
            type('f')
            type(Key.ENTER)

        if Settings.get_os() == Platform.LINUX:
            type('e', KeyModifier.ALT, 15)

            click(menu_bar_edit_find_in_page_pattern, 5)

        edit_select_all()
        edit_delete()

        find_toolbar_menu_bar = wait(find_toolbar_pattern, 5)

        assert_true(self, find_toolbar_menu_bar, 'The Find Toolbar is successfully displayed '
                                                  'by pressing Menu bar > Edit > Find in This Page.')

        find_toolbar_x = find(find_toolbar_pattern).x
        bttn_hl_all_x = find(bttn_hl_all_pattern).x
        bttn_match_case_x = find(bttn_match_case_pattern).x
        find_bttn_whole_words_pattern_x = find(find_bttn_whole_words_pattern).x

        type(Key.ESC)
        wait_vanish(find_toolbar_pattern, 20)

        items_appear_in_proper_way = find_toolbar_x < bttn_hl_all_x < bttn_match_case_x < find_bttn_whole_words_pattern_x

        assert_true(self, items_appear_in_proper_way,
                    'The Buttons of Find toolbar are displayed in correct order.')

        # 3) Menu > Find in This Page.

        wait(hamburger_menu_pattern, 5)
        click(hamburger_menu_pattern, 1)

        wait(hamburger_menu_find_in_page_pattern, 5)
        click(hamburger_menu_find_in_page_pattern, 1)

        edit_select_all()
        edit_delete()

        find_toolbar_opened_hamburger = wait(find_toolbar_pattern, 5)

        assert_true(self, find_toolbar_opened_hamburger,
                    'The Find Toolbar is successfully displayed by pressing Menu bar > Edit > Find in This Page.')

        find_toolbar_x = find(find_toolbar_pattern).x
        bttn_hl_all_x = find(bttn_hl_all_pattern).x
        bttn_match_case_x = find(bttn_match_case_pattern).x
        find_bttn_whole_words_pattern_x = find(find_bttn_whole_words_pattern).x

        type(Key.ESC)
        wait_vanish(find_toolbar_pattern, 20)

        items_appear_in_proper_way = find_toolbar_x < bttn_hl_all_x < bttn_match_case_x < find_bttn_whole_words_pattern_x

        assert_true(self, items_appear_in_proper_way,
                    'The Buttons of Find toolbar are displayed in correct order.')

        """ END STEP 2 """

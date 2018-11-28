# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Open find toolbar'
        self.test_case_id = '127238'
        self.test_suite_id = '2085'
        self.locales = ['en-US']

    def run(self):
        menu_bar_edit_pattern = Pattern('menu_bar_edit_pattern.png')
        hamburger_menu_pattern = Pattern('hamburger_menu_pattern.png')
        hamburger_menu_find_in_page_pattern = Pattern('hamburger_menu_find_in_page_pattern.png')
        menu_bar_edit_find_in_page_pattern = Pattern('menu_bar_edit_find_in_page_pattern.png')

        # Open Find Toolbar
        # 1) by pressing CTRL + F / Cmd + F
        open_find()
        edit_select_all()
        edit_delete()
        find_toolbar_is_opened = exists(FindToolbar.FINDBAR_TEXTBOX, 1)
        assert_true(self, find_toolbar_is_opened, 'The Find Toolbar is successfully displayed ')

        try:
            find_toolbar_x = find(FindToolbar.FINDBAR_TEXTBOX).x
        except FindError:
            raise FindError('Could not get the x-coordinate of the Find Toolbar')

        try:
            bttn_hl_all_x = find(FindToolbar.HIGHLIGHT).x
        except FindError:
            raise FindError('Could not get the x-coordinate of the Highlight All button')

        try:
            bttn_match_case_x = find(FindToolbar.FIND_CASE_SENSITIVE).x
        except FindError:
            raise FindError('Could not get the x-coordinate of the Match Case button')

        try:
            find_bttn_whole_words_pattern_x = find(FindToolbar.FIND_ENTIRE_WORD).x
        except FindError:
            raise FindError('Could not get the x-coordinate of the Whole Words button')

        type(Key.ESC)

        try:
            wait_vanish(FindToolbar.FINDBAR_TEXTBOX, 20)
            logger.debug('The Find toolbar successfully disappeared.')
        except FindError:
            raise FindError('The Find toolbar did not disappear.')

        items_appear_in_proper_way = find_toolbar_x < bttn_hl_all_x < bttn_match_case_x < find_bttn_whole_words_pattern_x
        assert_true(self, items_appear_in_proper_way,
                    'The Buttons of Find toolbar are displayed in correct order.')

        # 2) Menu bar > Edit > Find in This Page,

        if Settings.get_os() == Platform.WINDOWS:
            key_down(Key.ALT)
            key_up(Key.ALT)

            menu_bar_displayed = exists(menu_bar_edit_pattern, 5)
            if menu_bar_displayed:
                click(menu_bar_edit_pattern, 3)
            else:
                raise FindError('Menu bar is not displayed')

            menu_bar_find_in_page_displayed = exists(menu_bar_edit_find_in_page_pattern, 3)
            if menu_bar_find_in_page_displayed:
                click(menu_bar_edit_find_in_page_pattern, 3)
            else:
                raise FindError('Find in page tab in Menu bar is not displayed')

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
        find_toolbar_menu_bar = exists(FindToolbar.FINDBAR_TEXTBOX, 5)
        assert_true(self, find_toolbar_menu_bar, 'The Find Toolbar is successfully displayed ')

        try:
            find_toolbar_x = find(FindToolbar.FINDBAR_TEXTBOX).x
        except FindError:
            raise FindError('Could not get the x-coordinate of the Find Toolbar')

        try:
            bttn_hl_all_x = find(FindToolbar.HIGHLIGHT).x
        except FindError:
            raise FindError('Could not get the x-coordinate of the Highlight All button')

        try:
            bttn_match_case_x = find(FindToolbar.FIND_CASE_SENSITIVE).x
        except FindError:
            raise FindError('Could not get the x-coordinate of the Match Case button')

        try:
            find_bttn_whole_words_pattern_x = find(FindToolbar.FIND_ENTIRE_WORD).x
        except FindError:
            raise FindError('Could not get the x-coordinate of the Whole Words button')

        type(Key.ESC)

        try:
            wait_vanish(FindToolbar.FINDBAR_TEXTBOX, 20)
            logger.debug('The Find toolbar successfully disappeared.')
        except FindError:
            raise FindError('The Find toolbar did not disappear.')

        items_appear_in_proper_way = find_toolbar_x < bttn_hl_all_x < bttn_match_case_x < find_bttn_whole_words_pattern_x
        assert_true(self, items_appear_in_proper_way,
                    'The Buttons of Find toolbar are displayed in correct order.')

        # 3) Menu > Find in This Page.

        hamburger_menu_displayed = exists(hamburger_menu_pattern, 5)
        if hamburger_menu_displayed:
            click(hamburger_menu_pattern, 1)
        else:
            raise FindError('Hamburger menu is not displayed')

        hamburger_menu_find_in_page_displayed = exists(hamburger_menu_find_in_page_pattern, 5)
        if hamburger_menu_find_in_page_displayed:
            click(hamburger_menu_find_in_page_pattern, 1)
        else:
            raise FindError('The Find in page tab in the Hamburger menu is not displayed')

        edit_select_all()
        edit_delete()
        find_toolbar_opened_hamburger = exists(FindToolbar.FINDBAR_TEXTBOX, 5)
        assert_true(self, find_toolbar_opened_hamburger,
                    'The Find Toolbar is successfully displayed by pressing Menu bar > Edit > Find in This Page.')

        try:
            find_toolbar_x = find(FindToolbar.FINDBAR_TEXTBOX).x
        except FindError:
            raise FindError('Could not get the x-coordinate of the Find Toolbar')

        try:
            bttn_hl_all_x = find(FindToolbar.HIGHLIGHT).x
        except FindError:
            raise FindError('Could not get the x-coordinate of the Highlight All button')

        try:
            bttn_match_case_x = find(FindToolbar.FIND_CASE_SENSITIVE).x
        except FindError:
            raise FindError('Could not get the x-coordinate of the Match Case button')

        try:
            find_bttn_whole_words_pattern_x = find(FindToolbar.FIND_ENTIRE_WORD).x
        except FindError:
            raise FindError('Could not get the x-coordinate of the Whole Words button')

        type(Key.ESC)

        try:
            wait_vanish(FindToolbar.FINDBAR_TEXTBOX, 20)
            logger.debug('The Find toolbar successfully disappeared.')
        except FindError:
            raise FindError('The Find toolbar did not disappear.')

        items_appear_in_proper_way = find_toolbar_x < bttn_hl_all_x < bttn_match_case_x < find_bttn_whole_words_pattern_x
        assert_true(self, items_appear_in_proper_way,
                    'The Buttons of Find toolbar are displayed in correct order.')

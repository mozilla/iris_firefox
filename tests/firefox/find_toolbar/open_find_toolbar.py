# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description='Open find toolbar',
        locale=['en-US'],
        test_case_id='127238',
        test_suite_id='2085'
    )
    def run(self, firefox):
        open_find()
        edit_select_all()
        edit_delete()

        find_toolbar_is_opened = exists(FindToolbar.FINDBAR_TEXTBOX, FirefoxSettings.FIREFOX_TIMEOUT)
        assert find_toolbar_is_opened, 'The Find Toolbar is successfully displayed '

        try:
            find_toolbar_x = find(FindToolbar.FINDBAR_TEXTBOX.similar(0.6)).x
        except FindError:
            raise FindError('Could not get the x-coordinate of the Find Toolbar')

        try:
            button_highlight_all_x = find(FindToolbar.HIGHLIGHT).x
        except FindError:
            raise FindError('Could not get the x-coordinate of the Highlight All button')

        try:
            button_match_case_x = find(FindToolbar.FIND_CASE_SENSITIVE).x
        except FindError:
            raise FindError('Could not get the x-coordinate of the Match Case button')

        try:
            button_whole_words_x = find(FindToolbar.FIND_ENTIRE_WORD).x
        except FindError:
            raise FindError('Could not get the x-coordinate of the Whole Words button')

        type(Key.ESC)

        try:
            wait_vanish(FindToolbar.FINDBAR_TEXTBOX, FirefoxSettings.FIREFOX_TIMEOUT)
            logger.debug('The Find toolbar successfully disappeared.')
        except FindError:
            raise FindError('The Find toolbar did not disappear.')

        correct_order = find_toolbar_x < button_highlight_all_x < button_match_case_x < button_whole_words_x
        assert correct_order, 'The Buttons of Find toolbar are displayed in correct order.'

        # 2) Menu bar > Edit > Find in This Page,

        if OSHelper.is_linux():
            type('e', KeyModifier.ALT, FirefoxSettings.FIREFOX_TIMEOUT)

            click(MenuBar.Edit.EDIT_FIND_IN_PAGE)
        else:
            if OSHelper.is_windows():
                type(Key.ALT)

            menu_bar_displayed = exists(MenuBar.Edit.EDIT_PATTERN, FirefoxSettings.FIREFOX_TIMEOUT)
            if menu_bar_displayed:
                click(MenuBar.Edit.EDIT_PATTERN)
            else:
                raise FindError('Menu bar is not displayed')

            menu_bar_find_in_page_displayed = exists(MenuBar.Edit.EDIT_FIND_IN_PAGE,
                                                     FirefoxSettings.TINY_FIREFOX_TIMEOUT)
            if menu_bar_find_in_page_displayed:
                click(MenuBar.Edit.EDIT_FIND_IN_PAGE)
            else:
                raise FindError('Find in page tab in Menu bar is not displayed')

        edit_select_all()
        edit_delete()

        find_toolbar_menu_bar = exists(FindToolbar.FINDBAR_TEXTBOX, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert find_toolbar_menu_bar, 'The Find Toolbar is successfully displayed '

        try:
            find_toolbar_x = find(FindToolbar.FINDBAR_TEXTBOX).x
        except FindError:
            raise FindError('Could not get the x-coordinate of the Find Toolbar')

        try:
            button_highlight_all_x = find(FindToolbar.HIGHLIGHT).x
        except FindError:
            raise FindError('Could not get the x-coordinate of the Highlight All button')

        try:
            button_match_case_x = find(FindToolbar.FIND_CASE_SENSITIVE).x
        except FindError:
            raise FindError('Could not get the x-coordinate of the Match Case button')

        try:
            button_whole_words_x = find(FindToolbar.FIND_ENTIRE_WORD).x
        except FindError:
            raise FindError('Could not get the x-coordinate of the Whole Words button')

        type(Key.ESC)

        try:
            wait_vanish(FindToolbar.FINDBAR_TEXTBOX, FirefoxSettings.FIREFOX_TIMEOUT)
            logger.debug('The Find toolbar successfully disappeared.')
        except FindError:
            raise FindError('The Find toolbar did not disappear.')

        correct_order = find_toolbar_x < button_highlight_all_x < button_match_case_x < button_whole_words_x
        assert correct_order, 'The Buttons of Find toolbar are displayed in correct order.'

        # 3) Menu > Find in This Page.

        hamburger_menu_displayed = exists(NavBar.HAMBURGER_MENU, FirefoxSettings.FIREFOX_TIMEOUT)
        if hamburger_menu_displayed:
            click(NavBar.HAMBURGER_MENU)
        else:
            raise FindError('Hamburger menu is not displayed')

        hamburger_menu_find_in_page_displayed = exists(HamburgerMenu.HAMBURGER_MENU_FIND_IN_PAGE_PATTERN,
                                                       FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        if hamburger_menu_find_in_page_displayed:
            click(HamburgerMenu.HAMBURGER_MENU_FIND_IN_PAGE_PATTERN)
        else:
            raise FindError('The Find in page tab in the Hamburger menu is not displayed')

        edit_select_all()
        edit_delete()
        find_toolbar_opened_hamburger = exists(FindToolbar.FINDBAR_TEXTBOX, FirefoxSettings.FIREFOX_TIMEOUT)
        assert find_toolbar_opened_hamburger, 'The Find Toolbar is successfully displayed by ' \
                                              'pressing Menu bar > Edit > Find in This Page.'

        try:
            find_toolbar_x = find(FindToolbar.FINDBAR_TEXTBOX).x
        except FindError:
            raise FindError('Could not get the x-coordinate of the Find Toolbar')

        try:
            button_highlight_all_x = find(FindToolbar.HIGHLIGHT).x
        except FindError:
            raise FindError('Could not get the x-coordinate of the Highlight All button')

        try:
            button_match_case_x = find(FindToolbar.FIND_CASE_SENSITIVE).x
        except FindError:
            raise FindError('Could not get the x-coordinate of the Match Case button')

        try:
            button_whole_words_x = find(FindToolbar.FIND_ENTIRE_WORD).x
        except FindError:
            raise FindError('Could not get the x-coordinate of the Whole Words button')

        type(Key.ESC)

        try:
            wait_vanish(FindToolbar.FINDBAR_TEXTBOX, FirefoxSettings.FIREFOX_TIMEOUT)
            logger.debug('The Find toolbar successfully disappeared.')
        except FindError:
            raise FindError('The Find toolbar did not disappear.')

        correct_order = find_toolbar_x < button_highlight_all_x < button_match_case_x < button_whole_words_x
        assert correct_order, 'The Buttons of Find toolbar are displayed in correct order.'

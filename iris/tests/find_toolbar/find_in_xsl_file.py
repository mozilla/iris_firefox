# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Search on a XSL file. [Test is unstable on Linux.]'
        self.test_case_id = '127274'
        self.test_suite_id = '2085'
        self.locales = ['en-US']
        self.enabled = False

    def run(self):
        xls_first_occurrence_highlighted_pattern = Pattern('xls_first_occurrence_hl.png')
        xls_first_occurrence_unhighlighted_pattern = Pattern('xls_first_occurrence_white.png')
        xls_second_occurrence_highlighted_pattern = Pattern('xls_second_occurrence_hl.png')
        xls_second_occurrence_unhighlighted_pattern = Pattern('xls_second_occurrence_white.png')
        xls_cell_pattern = Pattern('xls_cell.png').similar(0.6)
        autosum_icon_pattern = Pattern('autosum_xls_icon.png')

        # Open Firefox and open a [XSL file]
        navigate('https://docs.google.com/spreadsheets/d/1DerWok62-wirXdtk7HhE_JAHZImPc7d6LT2jFFJRPxs')
        time.sleep(30)

        xls_spreadsheet_logo_pattern_exists = exists(xls_cell_pattern, 15)
        assert_true(self, xls_spreadsheet_logo_pattern_exists, 'The page is successfully loaded.')

        autosum_icon_exists = exists(autosum_icon_pattern, 20)
        assert_true(self, autosum_icon_exists, 'Spreadsheet loaded')

        if Settings.get_os() == Platform.LINUX:
            x = Location(x=500, y=0)
            key_down(Key.ALT)
            mouse_move(x, 2)
            key_up(Key.ALT)
            key_down(Key.ALT)
            mouse_move(x, 1)
            key_up(Key.ALT)

            menu_bar_edit_displayed = exists(MenuBar.Edit.EDIT_PATTERN, 5)
            if menu_bar_edit_displayed:
                key_up(Key.ALT)
                click(MenuBar.Edit.EDIT_PATTERN, 5)
                click(MenuBar.Edit.EDIT_FIND_IN_PAGE, 2)
            else:
                raise FindError('Menu bar edit is not displayed (Linux)')

        else:
            if Settings.get_os() == Platform.WINDOWS:
                key_down(Key.ALT)
                key_up(Key.ALT)

            menu_bar_edit_displayed = exists(MenuBar.Edit.EDIT_PATTERN, 5)
            if menu_bar_edit_displayed:
                click(MenuBar.Edit.EDIT_PATTERN, 1)
            else:
                raise FindError('Menu bar edit is not displayed.')

            menu_bar_edit_find_in_page_displayed = exists(MenuBar.Edit.EDIT_FIND_IN_PAGE, 3)

            if menu_bar_edit_find_in_page_displayed:
                click(MenuBar.Edit.EDIT_FIND_IN_PAGE, 1)
            else:
                raise FindError('Menu bar edit -> find in page is not displayed.')

        edit_select_all()
        edit_delete()

        find_toolbar_is_opened = exists(FindToolbar.FINDBAR_TEXTBOX, 5)
        assert_true(self, find_toolbar_is_opened, 'The Find Toolbar is successfully displayed ')

        # Navigate through found items
        type('re')
        if Settings.get_os() == Platform.LINUX:
            type(Key.ENTER)

        first_occurrence_highlighted_exists = exists(xls_first_occurrence_highlighted_pattern, 5)
        assert_true(self, first_occurrence_highlighted_exists, 'The first occurrence is highlighted.')

        second_occurrence_unhighlighted_exists = exists(xls_second_occurrence_unhighlighted_pattern, 5)
        assert_true(self, second_occurrence_unhighlighted_exists, 'The second occurrence is not highlighted.')

        find_next()

        first_occurrence_unhighlighted_exists = exists(xls_first_occurrence_unhighlighted_pattern, 5)
        assert_true(self, first_occurrence_unhighlighted_exists, 'The first occurrence is not highlighted.')

        second_occurrence_highlighted_exists = exists(xls_second_occurrence_highlighted_pattern, 5)
        assert_true(self, second_occurrence_highlighted_exists, 'The second occurrence is highlighted.')

        # Scroll the page up and down
        find_previous()
        first_occurrence_exists_before_scroll = exists(xls_first_occurrence_highlighted_pattern, 5)
        assert_true(self, first_occurrence_exists_before_scroll,
                    'The first occurrence is displayed before scrolling down and up')

        repeat_key_down(4)
        repeat_key_up(4)

        first_occurrence_exists_after_scroll = exists(xls_first_occurrence_highlighted_pattern, 5)
        assert_true(self, first_occurrence_exists_after_scroll,
                    'The first occurrence is displayed after scrolling down and up')

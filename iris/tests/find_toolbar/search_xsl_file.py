# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Search on a XSL file'
        self.test_case_id = '127274'
        self.test_suite_id = '2085'
        self.locales = ['en-US']

    def run(self):
        menu_bar_edit_pattern = Pattern('menu_bar_edit_pattern.png')
        menu_bar_edit_find_in_page_pattern = Pattern('menu_bar_edit_find_in_page_pattern.png')
        xls_first_occurrence_highlighted_pattern = Pattern('xls_first_occurrence_hl.png')
        xls_first_occurrence_unhighlighted_pattern = Pattern('xls_first_occurrence_white.png')
        xls_second_occurrence_highlighted_pattern = Pattern('xls_second_occurrence_hl.png')
        xls_second_occurrence_unhighlighted_pattern = Pattern('xls_second_occurrence_white.png')
        xls_cell_pattern = Pattern('xls_cell.png').similar(0.6)
        autosum_icon_pattern = Pattern('autosum_xls_icon.png')

        # Open Firefox and open a [XSL file]
        navigate('https://docs.google.com/spreadsheets/d/1izvhs2b9UX2JCD-0MsHonQBfPnjFsRpVuUOYGJYX2Oo/edit#gid=1283474565t')
        xls_spreadsheet_logo_pattern_exists = exists(xls_cell_pattern, 15)
        assert_true(self, xls_spreadsheet_logo_pattern_exists, 'The page is successfully loaded.')

        # Open the Find Toolbar from Menubar > Edit > Find
        xls_cell_displayed = exists(xls_cell_pattern, 5)
        if xls_cell_displayed:
            hover(xls_cell_pattern, 0.1)
            click(xls_cell_pattern)
        else:
            raise FindError('XLS cell is not displayed')

        autosum_icon_exists = exists(autosum_icon_pattern, 20)
        assert_true(self, autosum_icon_exists, 'Spreadsheet loaded')

        if Settings.get_os() == Platform.WINDOWS:
            key_down(Key.ALT)
            key_up(Key.ALT)

            menu_bar_edit_displayed = exists(menu_bar_edit_pattern, 5)
            if menu_bar_edit_displayed:
                click(menu_bar_edit_pattern, 1)
            else:
                raise FindError('Menu bar edit is not displayed (Windows)')

            menu_bar_edit_find_in_page_displayed = exists(menu_bar_edit_find_in_page_pattern, 3)
            if menu_bar_edit_find_in_page_displayed:
                click(menu_bar_edit_find_in_page_pattern, 1)
            else:
                raise FindError('Menu bar edit -> find in page is not displayed (Windows)')

        if Settings.get_os() == Platform.LINUX:
            x = Location(x=500, y=0)
            key_down(Key.ALT)
            mouse_move(x, 2)
            key_up(Key.ALT)
            key_down(Key.ALT)
            mouse_move(x, 1)
            key_up(Key.ALT)

            menu_bar_edit_displayed = exists(menu_bar_edit_pattern, 5)
            if menu_bar_edit_displayed:
                key_up(Key.ALT)
                click(menu_bar_edit_pattern, 5)
                click(menu_bar_edit_find_in_page_pattern, 2)
            else:
                raise FindError('Menu bar edit is not displayed (Linux)')

        if Settings.get_os() == Platform.MAC:
            type(Key.F2, KeyModifier.CTRL)
            type(Key.RIGHT)
            type(Key.RIGHT)
            type(Key.RIGHT)
            type(Key.DOWN)
            type('f')
            type(Key.ENTER)

        edit_select_all()
        edit_delete()
        find_toolbar_is_opened = exists(FindToolbar.FINDBAR_TEXTBOX, 5)
        assert_true(self, find_toolbar_is_opened, 'The Find Toolbar is successfully displayed ')

        # Navigate through found items
        type('re')
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
        [scroll_down() for _ in range(4)]
        [scroll_up() for _ in range(4)]
        first_occurrence_exists_after_scroll = exists(xls_first_occurrence_highlighted_pattern, 5)
        assert_true(self, first_occurrence_exists_after_scroll,
                    'The first occurrence is displayed after scrolling down and up')

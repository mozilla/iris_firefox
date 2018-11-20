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

        find_toolbar_pattern = Pattern('find_toolbar_text.png')
        xls_spreadsheet_logo_pattern = Pattern('xls_tab_logo.png')
        xls_spreadsheet_logo_pattern.similarity = 0.6

        menu_bar_edit_pattern = Pattern('menu_bar_edit_pattern.png')
        menu_bar_edit_find_in_page_pattern = Pattern('menu_bar_edit_find_in_page_pattern.png')

        xls_first_occurrence_hl_pattern = Pattern('xls_first_occurrence_hl.png')
        xls_first_occurrence_white_pattern = Pattern('xls_first_occurrence_white.png')
        xls_second_occurrence_hl_pattern = Pattern('xls_second_occurrence_hl.png')
        xls_second_occurrence_white_pattern = Pattern('xls_second_occurrence_white.png')

        xls_cell_pattern = Pattern('xls_cell.png')
        xls_cell_pattern.similarity = 0.6

        navigate('https://docs.google.com/spreadsheets/d/1izvhs2b9UX2JCD-0MsHonQBfPnjFsRpVuUOYGJYX2Oo/edit#gid=1283474565t')

        xls_spreadsheet_logo_pattern_exists = exists(xls_spreadsheet_logo_pattern, 15)

        assert_true(self, xls_spreadsheet_logo_pattern_exists, 'The page is successfully loaded.')

        click(xls_cell_pattern, 5)

        # Menu bar > Edit > Find in This Page,

        if Settings.get_os() == Platform.WINDOWS:
            key_down(Key.ALT)
            key_up(Key.ALT)

            wait(menu_bar_edit_pattern, 5)
            click(menu_bar_edit_pattern, 1)

            wait(menu_bar_edit_find_in_page_pattern, 3)
            click(menu_bar_edit_find_in_page_pattern, 1)

        if Settings.get_os() == Platform.LINUX:
            x = Location(x = 500, y = 0)
            key_down(Key.ALT)
            mouse_move(x, 2)
            key_up(Key.ALT)
            key_down(Key.ALT)
            mouse_move(x, 1)
            key_up(Key.ALT)

            wait(menu_bar_edit_pattern, 5)
            key_up(Key.ALT)
            click(menu_bar_edit_pattern, 5)
            click(menu_bar_edit_find_in_page_pattern, 2)


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

        find_toolbar_is_opened = wait(find_toolbar_pattern, 5)

        assert_true(self, find_toolbar_is_opened, 'The Find Toolbar is successfully displayed '
                                                  'by pressing Menu bar > Edit > Find in This Page.')

        type('an')

        first_occurrence_hl_exists = exists(xls_first_occurrence_hl_pattern, 5)
        second_occurrence_white_exists = exists(xls_second_occurrence_white_pattern, 5)

        assert_true(self, (first_occurrence_hl_exists and second_occurrence_white_exists),
                    'All the matching words/characters are found.')

        first_occurrence_hl_exists = exists(xls_first_occurrence_hl_pattern, 5)
        second_occurrence_white_exists = exists(xls_second_occurrence_white_pattern, 5)
        assert_true(self, first_occurrence_hl_exists and second_occurrence_white_exists,
                    'First occurrence highlighted')

        find_next()

        first_occurrence_white_exists = exists(xls_first_occurrence_white_pattern, 5)
        second_occurrence_hl_exists = exists(xls_second_occurrence_hl_pattern, 5)

        assert_true(self, first_occurrence_white_exists and second_occurrence_hl_exists,
                    'Second occurrence highlighted')

        # Get back to first occurrence
        find_previous()

        first_occurrence_exists_before_scroll = exists(xls_first_occurrence_hl_pattern, 5)

        for i in range(4):
            scroll_down()

        for i in range(4):
            scroll_up()

        first_occurrence_exists_after_scroll = exists(xls_first_occurrence_hl_pattern, 5)

        assert_true(self, first_occurrence_exists_before_scroll and first_occurrence_exists_after_scroll,
                    'Occurrence exists after scroll up and down')

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description='Search on a XSL file. [Test is unstable on Linux.]',
        locale=['en-US'],
        test_case_id='127274',
        test_suite_id='2085',
        enabled=False
    )
    def run(self, firefox):
        xls_first_occurrence_highlighted_pattern = Pattern('xls_first_occurrence_hl.png')
        xls_first_occurrence_unhighlighted_pattern = Pattern('xls_first_occurrence_white.png')
        xls_second_occurrence_highlighted_pattern = Pattern('xls_second_occurrence_hl.png')
        xls_second_occurrence_unhighlighted_pattern = Pattern('xls_second_occurrence_white.png')
        xls_cell_pattern = Pattern('xls_cell.png').similar(0.6)
        autosum_icon_pattern = Pattern('autosum_xls_icon.png')

        # Open Firefox and open a [XSL file]
        navigate('https://docs.google.com/spreadsheets/d/1DerWok62-wirXdtk7HhE_JAHZImPc7d6LT2jFFJRPxs')

        xls_spreadsheet_logo_pattern_exists = exists(xls_cell_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert xls_spreadsheet_logo_pattern_exists, 'The page is successfully loaded.'

        autosum_icon_exists = exists(autosum_icon_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert autosum_icon_exists, 'Spreadsheet loaded'

        if OSHelper.is_linux():
            x = Location(x=500, y=0)
            key_down(Key.ALT)
            move(x, 2)
            key_up(Key.ALT)
            key_down(Key.ALT)
            mouse_reset(x, 1)
            key_up(Key.ALT)

            menu_bar_edit_displayed = exists(MenuBar.Edit.EDIT_PATTERN, FirefoxSettings.FIREFOX_TIMEOUT)
            if menu_bar_edit_displayed:
                key_up(Key.ALT)
                click(MenuBar.Edit.EDIT_PATTERN, FirefoxSettings.TINY_FIREFOX_TIMEOUT)
                click(MenuBar.Edit.EDIT_FIND_IN_PAGE, 2)
            else:
                raise FindError('Menu bar edit is not displayed (Linux)')

        else:
            if OSHelper.is_windows():
                key_down(Key.ALT)
                key_up(Key.ALT)

            menu_bar_edit_displayed = exists(MenuBar.Edit.EDIT_PATTERN, FirefoxSettings.FIREFOX_TIMEOUT)
            if menu_bar_edit_displayed:
                click(MenuBar.Edit.EDIT_PATTERN, 1)
            else:
                raise FindError('Menu bar edit is not displayed.')

            menu_bar_edit_find_in_page_displayed = exists(MenuBar.Edit.EDIT_FIND_IN_PAGE)

            if menu_bar_edit_find_in_page_displayed:
                click(MenuBar.Edit.EDIT_FIND_IN_PAGE, 1)
            else:
                raise FindError('Menu bar edit -> find in page is not displayed.')

        edit_select_all()
        edit_delete()

        find_toolbar_is_opened = exists(FindToolbar.FINDBAR_TEXTBOX, FirefoxSettings.FIREFOX_TIMEOUT)
        assert find_toolbar_is_opened, 'The Find Toolbar is successfully displayed '

        # Navigate through found items
        type('re')
        if OSHelper.is_linux():
            type(Key.ENTER)

        first_occurrence_highlighted_exists = exists(xls_first_occurrence_highlighted_pattern,
                                                     FirefoxSettings.FIREFOX_TIMEOUT)
        assert first_occurrence_highlighted_exists, 'The first occurrence is highlighted.'

        second_occurrence_unhighlighted_exists = exists(xls_second_occurrence_unhighlighted_pattern,
                                                        FirefoxSettings.FIREFOX_TIMEOUT)
        assert second_occurrence_unhighlighted_exists, 'The second occurrence is not highlighted.'

        find_next()

        first_occurrence_unhighlighted_exists = exists(xls_first_occurrence_unhighlighted_pattern,
                                                       FirefoxSettings.FIREFOX_TIMEOUT)
        assert first_occurrence_unhighlighted_exists, 'The first occurrence is not highlighted.'

        second_occurrence_highlighted_exists = exists(xls_second_occurrence_highlighted_pattern,
                                                      FirefoxSettings.FIREFOX_TIMEOUT)
        assert second_occurrence_highlighted_exists, 'The second occurrence is highlighted.'

        # Scroll the page up and down
        find_previous()

        first_occurrence_exists_before_scroll = exists(xls_first_occurrence_highlighted_pattern,
                                                       FirefoxSettings.FIREFOX_TIMEOUT)
        assert first_occurrence_exists_before_scroll, 'The first occurrence is displayed before scrolling down and up'

        repeat_key_down(4)
        repeat_key_up(4)

        first_occurrence_exists_after_scroll = exists(xls_first_occurrence_highlighted_pattern,
                                                      FirefoxSettings.FIREFOX_TIMEOUT)
        assert first_occurrence_exists_after_scroll, 'The first occurrence is displayed after scrolling down and up'

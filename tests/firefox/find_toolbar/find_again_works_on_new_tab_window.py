# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description='Check "Find Again" works on a new tab/window ',
        locale=['en-US'],
        test_case_id='127263',
        test_suite_id='2085',
        blocked_by={'id': '913536', 'platform': OSPlatform.ALL}
    )
    def run(self, firefox):
        new_tab_icon_pattern = Tabs.NEW_TAB_HIGHLIGHTED
        find_toolbar_abc_text_pattern = Pattern('find_toolbar_abc_text.png')
        find_toolbar_abc_text_hovered_pattern = Pattern('find_toolbar_abc_text_hovered.png')

        # Open the Find Toolbar
        open_find()
        edit_select_all()
        edit_delete()
        find_toolbar_is_opened = exists(FindToolbar.FINDBAR_TEXTBOX, FirefoxSettings.FIREFOX_TIMEOUT)
        assert find_toolbar_is_opened, 'The find toolbar is opened'

        # Enter a search term (e.g. "abc")
        type('abc')
        if OSHelper.is_mac():
            type(Key.ENTER)

        # When 'abc' doesn't appear on the page it has red highlight
        find_toolbar_abc_text_typed_red = exists(find_toolbar_abc_text_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert find_toolbar_abc_text_typed_red, 'The search term \'abc\' is typed into find toolbar.'

        # Open another tab
        new_tab()
        new_tab_is_opened = exists(new_tab_icon_pattern)
        assert new_tab_is_opened, 'New tab is opened.'

        # Open the Find Toolbar
        open_find()
        find_toolbar_abc_text_hovered = exists(find_toolbar_abc_text_hovered_pattern)
        assert find_toolbar_abc_text_hovered, 'The find toolbar is opened and contains search term \"abc\".'

        # Open a new window
        new_window()
        new_window_is_opened = exists(new_tab_icon_pattern)
        assert new_window_is_opened, 'New window is opened.'

        # Open the Find Toolbar
        open_find()
        find_toolbar_abc_text_hovered = exists(find_toolbar_abc_text_hovered_pattern)
        assert find_toolbar_abc_text_hovered, 'The find toolbar is opened and contains search term \"abc\".'

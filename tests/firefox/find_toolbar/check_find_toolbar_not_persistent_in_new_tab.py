# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description='Check Find Toolbar is not persistent in a new tab / window',
        locale=['en-US'],
        test_case_id='127262',
        test_suite_id='2085'
    )
    def run(self, firefox):
        new_tab_icon_pattern = Tabs.NEW_TAB_HIGHLIGHTED

        # Open Firefox and open the Find Toolbar
        open_find()
        edit_select_all()
        edit_delete()

        find_toolbar_is_opened = exists(FindToolbar.FINDBAR_TEXTBOX, FirefoxSettings.FIREFOX_TIMEOUT)
        assert find_toolbar_is_opened, 'The find toolbar is opened'

        # Open another tab
        new_tab()

        new_tab_is_opened = exists(new_tab_icon_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert new_tab_is_opened, 'New tab is opened'

        find_toolbar_is_opened = exists(FindToolbar.FINDBAR_TEXTBOX, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert find_toolbar_is_opened is not True, 'The find toolbar is not opened on a new tab'

        # Open a new window
        new_window()

        new_tab_is_opened = exists(new_tab_icon_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert new_tab_is_opened, 'New tab is opened'

        find_toolbar_is_opened = exists(FindToolbar.FINDBAR_TEXTBOX, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert find_toolbar_is_opened is not True, 'The find toolbar is not opened in a new window'

        close_window()

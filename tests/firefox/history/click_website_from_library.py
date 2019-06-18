# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Click on a website from the Library.',
        locale=['en-US'],
        test_case_id='172043',
        test_suite_id='2000'
    )
    def run(self, firefox):
        show_all_history_pattern = History.HistoryMenu.SHOW_ALL_HISTORY
        iris_bookmark_pattern = Pattern('iris_bookmark.png')
        iris_bookmark_focus_pattern = Pattern('iris_bookmark_focus.png')

        new_tab()

        # Open History and check if it is populated with the Iris page.
        open_library_menu('History')

        right_upper_corner = Region(Screen().width / 2, 0, Screen().width / 2, Screen().height / 2)

        expected = right_upper_corner.exists(iris_bookmark_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, 'Iris page is displayed in the History menu list.'

        click(show_all_history_pattern)

        expected = exists(iris_bookmark_focus_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, 'Iris page is displayed in the Recent History list.'

        double_click(iris_bookmark_focus_pattern)

        test_site_opened = exists(LocalWeb.IRIS_LOGO, FirefoxSettings.FIREFOX_TIMEOUT)
        assert test_site_opened, 'Iris page is successfully opened in the same tab.'

        # Get the library in focus again.
        open_library()

        click_window_control('close')

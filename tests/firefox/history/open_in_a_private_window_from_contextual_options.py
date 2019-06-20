# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Use \'Open in a Private Window\' button from the contextual options.',
        locale=['en-US'],
        test_case_id='174041',
        test_suite_id='2000',
        profile=Profiles.TEN_BOOKMARKS
    )
    def run(self, firefox):
        show_all_history_pattern = History.HistoryMenu.SHOW_ALL_HISTORY
        last_searched_item_pattern = Pattern('iris_bookmark_focus.png')

        # Check that the Library window is displayed properly.
        library_button_exists = exists(NavBar.LIBRARY_MENU)
        assert library_button_exists is True, 'Library button exists'

        click(NavBar.LIBRARY_MENU)

        history_button_exists = exists(LibraryMenu.HISTORY_BUTTON, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert history_button_exists is True, 'History button exists'

        click(LibraryMenu.HISTORY_BUTTON)

        show_all_history_exists = exists(show_all_history_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert show_all_history_exists is True, '\"Show All History\" option exists.'

        click(show_all_history_pattern)

        # Open the last searched item in a new private window.
        last_searched_item_exists = exists(last_searched_item_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert last_searched_item_exists is True, 'Last searched item was found.'

        right_click_and_type(last_searched_item_pattern, FirefoxSettings.TINY_FIREFOX_TIMEOUT, 'p')

        # Assert the newly opened window.
        private_window_exists = exists(PrivateWindow.private_window_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert private_window_exists is True, 'The private window was successfully opened.'

        iris_logo_exists = exists(LocalWeb.IRIS_LOGO, FirefoxSettings.FIREFOX_TIMEOUT)
        assert iris_logo_exists is True, 'The page was successfully opened.'

        # Close the private window and then the auxiliary window.
        close_window()

        click_window_control('close')

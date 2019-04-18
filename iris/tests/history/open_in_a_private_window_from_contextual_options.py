# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from iris.test_case import *


class Test(BaseTest):
    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Use \'Open in a Private Window\' button from the contextual options.'
        self.test_case_id = '174041'
        self.test_suite_id = '2000'
        self.locales = ['en-US']

    def setup(self):
        """Test case setup
         This overrides the setup method in the BaseTest class, so that it can use a brand new profile.
        """
        BaseTest.setup(self)
        self.profile = Profile.TEN_BOOKMARKS
        return

    def run(self):
        show_all_history_pattern = History.HistoryMenu.SHOW_ALL_HISTORY
        last_searched_item = Pattern('iris_bookmark_focus.png')

        # Check that the Library window is displayed properly.
        library_button_exists = exists(NavBar.LIBRARY_MENU)
        assert_true(self, library_button_exists, 'Library button exists')

        click(NavBar.LIBRARY_MENU)

        history_button_exists = exists(LibraryMenu.HISTORY_BUTTON, Settings.SHORT_FIREFOX_TIMEOUT)
        assert_true(self, history_button_exists, 'History button exists')

        click(LibraryMenu.HISTORY_BUTTON)

        expected = exists(show_all_history_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, expected, '\"Show All History\" option exists.')

        click(show_all_history_pattern)

        # Open the last searched item in a new private window.
        expected = exists(last_searched_item, Settings.FIREFOX_TIMEOUT)
        assert_true(self, expected, 'Last searched item was found.')

        right_click(last_searched_item)

        type(text='p')

        # Assert the newly opened window.
        expected = exists(PrivateWindow.private_window_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, expected, 'The private window was successfully opened.')

        expected = exists(LocalWeb.IRIS_LOGO, Settings.FIREFOX_TIMEOUT)
        assert_true(self, expected, 'The page was successfully opened.')

        # Close the private window and then the auxiliary window.
        close_window()

        click_window_control('close')

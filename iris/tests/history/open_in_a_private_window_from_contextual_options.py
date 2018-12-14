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
        iris_logo = Pattern('iris_logo.png')
        private_window = Pattern('private_window.png')

        # Check that the Library window is displayed properly.
        open_library_menu('History')
        expected = exists(show_all_history_pattern, 10)
        assert_true(self, expected, '\"Show All History\" option exists.')
        click(show_all_history_pattern)

        # Open the last searched item in a new private window.
        expected = exists(last_searched_item, 10)
        assert_true(self, expected, 'Last searched item was found.')
        right_click(last_searched_item)
        type(text='p')

        # Assert the newly opened window.
        expected = exists(private_window, 10)
        assert_true(self, expected, 'The private window was successfully opened.')
        expected = exists(iris_logo, 10)
        assert_true(self, expected, 'The page was successfully opened.')

        # Close the private window and then the auxiliary window.
        close_window()
        click_window_control('close')

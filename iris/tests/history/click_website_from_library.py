# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *
from iris.api.core.firefox_ui.history import History


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Click on a website from the Library.'
        self.test_case_id = '174037'
        self.test_suite_id = '2000'
        self.locales = ['en-US']

    def run(self):
        show_all_history_pattern = History.HistoryMenu.SHOW_ALL_HISTORY
        iris_bookmark_pattern = Pattern('iris_bookmark.png')
        iris_bookmark_focus_pattern = Pattern('iris_bookmark_focus.png')
        iris_logo_pattern = Pattern('iris_logo.png')

        new_tab()

        # Open History and check if it is populated with the Iris page.
        open_library_menu('History')

        right_upper_corner = Region(SCREEN_WIDTH / 2, 0, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        expected = right_upper_corner.exists(iris_bookmark_pattern, 10)
        assert_true(self, expected, 'Iris page is displayed in the History menu list.')

        click(show_all_history_pattern)

        expected = exists(iris_bookmark_focus_pattern, 10)
        assert_true(self, expected, 'Iris page is displayed in the Recent History list.')

        double_click(iris_bookmark_focus_pattern)
        time.sleep(DEFAULT_UI_DELAY)

        expected = exists(iris_logo_pattern, 10)
        assert_true(self, expected, 'Iris page is successfully opened in the same tab.')

        # Get the library in focus again.
        open_library()

        click_window_control('close')

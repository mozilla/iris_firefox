# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Forget a page from the Library - History menu.'
        self.test_case_id = '174050'
        self.test_suite_id = '2000'
        self.locales = ['en-US']

    def run(self):
        show_all_history = History.HistoryMenu.SHOW_ALL_HISTORY
        iris_bookmark = Pattern('iris_bookmark.png')
        iris_bookmark_focus = Pattern('iris_bookmark_focus.png')

        # Open History and check if is populated with Iris page.
        open_library_menu('History')
        right_upper_corner = Region(SCREEN_WIDTH / 2, 0, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        expected_1 = right_upper_corner.exists(iris_bookmark, 10)
        assert_true(self, expected_1, 'Iris page is displayed in the History menu list successfully.')

        click(show_all_history)

        expected_2 = exists(iris_bookmark_focus, 10)
        assert_true(self, expected_2, 'Iris page is displayed Recent History list successfully.')

        # Forget Mozilla page.
        right_click(iris_bookmark_focus)
        type(text='f')

        try:
            expected_3 = wait_vanish(iris_bookmark_focus, 10)
            assert_true(self, expected_3, 'Iris page was deleted successfully from the history.')
        except FindError:
            raise FindError('Iris page is still displayed in the history.')

        click_window_control('close')

        # Check that Mozilla page is not displayed in the Recent History list.
        open_library_menu('History')
        expected_4 = exists(iris_bookmark, 5)
        assert_false(self, expected_4, 'Iris page is not displayed in the History menu list.')

        type(Key.ESC)

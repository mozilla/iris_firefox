# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Use \'Open in a New Window\' button from the contextual options.'
        self.test_case_id = '174040'
        self.test_suite_id = '2000'
        self.locales = ['en-US']

    def run(self):
        iris_bookmark_pattern = Pattern('iris_bookmark.png')
        show_all_history_pattern = History.HistoryMenu.SHOW_ALL_HISTORY
        new_tab_pattern = Pattern('new_tab.png')
        mozilla_bookmark_focus_pattern = Pattern('mozilla_bookmark_focus.png')

        # Open a page to create some history.
        navigate(LocalWeb.MOZILLA_TEST_SITE)
        expected = exists(LocalWeb.MOZILLA_LOGO, 10)
        assert_true(self, expected, 'Mozilla page loaded successfully.')
        new_tab()
        previous_tab()
        close_tab()

        # Open History and check if it is populated with the Iris page.
        open_library_menu('History')

        right_upper_corner = Region(SCREEN_WIDTH / 2, 0, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        expected = right_upper_corner.exists(iris_bookmark_pattern, 10)
        assert_true(self, expected, 'Iris page is displayed in the History menu list.')

        click(show_all_history_pattern)

        expected = exists(mozilla_bookmark_focus_pattern, 10)
        assert_true(self, expected, 'Mozilla page is displayed in the Recent History list.')

        # Open page in new window.
        right_click(mozilla_bookmark_focus_pattern)
        type(text='n')

        # Make sure that the selected website is opened in a new window.
        expected = exists(LocalWeb.MOZILLA_LOGO, 10)
        assert_true(self, expected, 'Mozilla page loaded successfully.')

        expected = exists(new_tab_pattern, 3)
        assert_false(self, expected, 'about:newtab page is not visible in the new opened window.')

        close_window()
        click_window_control('close')

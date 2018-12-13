# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Use \'Open in a New Tab\' button from the contextual options.'
        self.test_case_id = '174039'
        self.test_suite_id = '2000'
        self.locales = ['en-US']

    def setup(self):
        """ Test case setup
        This overrides the setup method in the BaseTest class,
        so that it can use a profile that already has been launched.
        """
        BaseTest.setup(self)
        self.profile = Profile.TEN_BOOKMARKS
        return

    def run(self):
        iris_bookmark_pattern = Pattern('iris_bookmark.png')
        show_all_history_pattern = History.HistoryMenu.SHOW_ALL_HISTORY
        history_today_pattern = Library.HISTORY_TODAY
        library_bookmarks_mozilla_pattern = Pattern('library_bookmarks_mozilla.png')
        iris_tab_icon = Pattern('iris_logo_tab.png')

        # Open a page to create some today's history.
        new_tab()
        navigate(LocalWeb.MOZILLA_TEST_SITE)
        expected_1 = exists(LocalWeb.MOZILLA_LOGO, 10)
        assert_true(self, expected_1, 'Mozilla page loaded successfully.')
        close_tab()

        # Select the History option from the View History, saved bookmarks and more Menu.
        open_library_menu('History')
        right_upper_corner = Region(SCREEN_WIDTH / 2, 0, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        expected_2 = right_upper_corner.exists(iris_bookmark_pattern, 10)
        assert_true(self, expected_2, 'Iris page is displayed in the History menu list.')

        # Click on the Show All History button.
        click(show_all_history_pattern)
        expected_3 = exists(history_today_pattern, 10)
        assert_true(self, expected_3, 'Today history option is available.')

        # Verify if Mozilla page is present in Today's History.
        click(history_today_pattern)
        expected_4 = exists(library_bookmarks_mozilla_pattern, 10)
        assert_true(self, expected_4, 'Mozilla page is displayed successfully in the History list.')

        # Open the Mozilla page using the 'Open in a New Tab' button from the context menu.
        right_click(library_bookmarks_mozilla_pattern)
        time.sleep(Settings.FX_DELAY)
        type(text='w')

        # Close the library.
        open_library()
        time.sleep(Settings.FX_DELAY)
        click_window_control('close')
        time.sleep(Settings.FX_DELAY)

        # Check that the Mozilla page loaded successfully in a new tab.
        expected_5 = exists(LocalWeb.MOZILLA_LOGO, 10)
        assert_true(self, expected_5, 'Mozilla page loaded successfully.')

        expected_6 = exists(iris_tab_icon, 10)
        assert_true(self, expected_6, 'Iris local page is still open in the first tab.')

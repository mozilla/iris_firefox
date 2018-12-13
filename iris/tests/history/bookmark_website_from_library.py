# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Bookmark a website from the Library - History menu.'
        self.test_case_id = '174043'
        self.test_suite_id = '2000'
        self.locales = ['en-US']

    def setup(self):
        """Test case setup

        Override the setup method to use a pre-canned bookmarks profile to have a dirty profile.
        """
        BaseTest.setup(self)
        self.profile = Profile.TEN_BOOKMARKS
        return

    def run(self):
        show_all_history_pattern = History.HistoryMenu.SHOW_ALL_HISTORY
        iris_bookmark_pattern = Pattern('iris_bookmark.png')
        iris_bookmark_focus_pattern = Pattern('iris_bookmark_focus.png')
        library_bookmarks_iris_pattern = Pattern('library_bookmarks_iris.png')
        library_expand_bookmarks_menu_pattern = Library.BOOKMARKS_MENU
        save_bookmark_button_pattern = Pattern('save_bookmark_name.png')

        # Open History and check if it is populated with the Iris page.
        open_library_menu('History')

        right_upper_corner = Region(SCREEN_WIDTH / 2, 0, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        expected = right_upper_corner.exists(iris_bookmark_pattern, 10)
        assert_true(self, expected, 'Iris page is displayed in the History menu list.')

        click(show_all_history_pattern)

        expected = exists(iris_bookmark_focus_pattern, 10)
        assert_true(self, expected, 'Iris page is displayed in the Recent History list.')

        right_click(iris_bookmark_focus_pattern)
        type(text='b')

        # Bookmark the website.
        expected = exists(save_bookmark_button_pattern, 10)
        assert_true(self, expected, 'New Bookmark popup displayed properly.')

        click(save_bookmark_button_pattern)

        try:
            expected = wait_vanish(save_bookmark_button_pattern, 10)
            assert_true(self, expected, 'New Bookmark popup was closed successfully.')
        except FindError:
            raise FindError('New Bookmark popup is still open')

        click_window_control('close')
        time.sleep(DEFAULT_UI_DELAY)

        # Open the library and check that the page was bookmarked with default settings.
        open_library()

        expected = exists(library_expand_bookmarks_menu_pattern, 10)
        assert_true(self, expected, 'Expand bookmarks menu button displayed properly.')

        click(library_expand_bookmarks_menu_pattern)

        expected = exists(library_bookmarks_iris_pattern, 10)
        assert_true(self, expected, 'The website is bookmarked in the Bookmarks Menu folder, with the default name and '
                                    'without any tags.')

        click_window_control('close')

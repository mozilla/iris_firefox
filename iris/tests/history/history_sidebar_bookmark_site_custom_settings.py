# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This is a test that bookmarks a page from the History sidebar with custom settings.'

    def setup(self):
        """Test case setup

        This overrides the setup method in the BaseTest class, so that it can use a brand new profile.
        """
        BaseTest.setup(self)
        self.profile = Profile.BRAND_NEW
        return

    def run(self):
        history_sidebar_mozilla = LocalWeb.MOZILLA_BOOKMARK_SMALL
        search_history_box = 'search_history_box.png'
        expand_button_history_sidebar = 'expand_button_history_sidebar.png'
        save_bookmark_button = 'save_bookmark_name.png'
        library_bookmarks_mozilla_custom_settings = 'library_bookmarks_mozilla_custom_settings.png'
        new_bookmark_folder_bookmarks_menu = 'new_bookmark_folder_bookmarks_menu.png'

        # Open a page to create some history.
        navigate(LocalWeb.MOZILLA_TEST_SITE)
        expected_1 = exists(LocalWeb.MOZILLA_LOGO, 10)
        assert_true(self, expected_1, 'Mozilla page loaded successfully.')

        # Open the History sidebar.
        history_sidebar()
        expected_2 = exists(search_history_box, 10)
        assert_true(self, expected_2, 'Sidebar was opened successfully.')

        expected_3 = exists(expand_button_history_sidebar, 10)
        assert_true(self, expected_3, 'Expand history button displayed properly.')
        click(expand_button_history_sidebar)

        # Bookmark a page from the History sidebar with custom settings.
        history_sidebar_region = Region(0, find(NavBar.HOME_BUTTON).y, SCREEN_WIDTH / 4, SCREEN_HEIGHT / 3)
        expected_4 = history_sidebar_region.exists(history_sidebar_mozilla, 10)
        assert_true(self, expected_4, 'Mozilla page is displayed in the History list successfully.')

        history_sidebar_region.right_click(history_sidebar_mozilla, 1)
        type(text='b')

        expected_5 = exists(save_bookmark_button, 10)
        assert_true(self, expected_5, 'New Bookmark popup displayed properly.')

        paste('Test name')
        if Settings.is_mac():
            click(new_bookmark_folder_bookmarks_menu)
            type(Key.DOWN)
            type(Key.RETURN)
            type(Key.TAB)
        else:
            type(Key.TAB)
            type(Key.DOWN)
            type(Key.TAB)
            type(Key.TAB)
        paste('Test_tag')
        click(save_bookmark_button)

        try:
            expected_6 = wait_vanish(save_bookmark_button, 10)
            assert_true(self, expected_6, 'New Bookmark popup was closed successfully.')
        except FindError:
            raise FindError('New Bookmark popup is still open')

        # Open the library and check that the page was bookmarked with custom settings
        open_library()
        expected_7 = exists(library_bookmarks_mozilla_custom_settings, 10)
        assert_true(self, expected_7, 'Mozilla page is bookmarked with custom name and tags in a different folder.')
        click_auxiliary_window_control('close')

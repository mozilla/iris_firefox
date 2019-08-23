# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='This is a test that bookmarks a page from the History sidebar.',
        locale=['en-US'],
        test_case_id='120123',
        test_suite_id='2000',
        profile=Profiles.BRAND_NEW
    )
    def run(self, firefox):
        history_sidebar_mozilla_pattern = LocalWeb.MOZILLA_BOOKMARK_HISTORY_SIDEBAR
        search_history_box_pattern = Sidebar.HistorySidebar.SEARCH_BOX
        history_today_sidebar_pattern = Sidebar.HistorySidebar.Timeline.TODAY
        save_bookmark_button_pattern = Pattern('save_bookmark_name.png')
        library_expand_bookmarks_menu_pattern = Library.BOOKMARKS_MENU
        library_bookmarks_mozilla_pattern = Pattern('library_bookmarks_mozilla.png')

        # Open a page to create some history.
        navigate(LocalWeb.MOZILLA_TEST_SITE)

        expected_1 = exists(LocalWeb.MOZILLA_LOGO, 10)
        assert expected_1, 'Mozilla page loaded successfully.'

        # Open the History sidebar.
        history_sidebar()

        expected_2 = exists(search_history_box_pattern, 10)
        assert expected_2, 'Sidebar was opened successfully.'

        expected_3 = exists(history_today_sidebar_pattern, 10)
        assert expected_3, 'Expand history button displayed properly.'

        click(history_today_sidebar_pattern)

        # Bookmark a page from the History sidebar.
        history_sidebar_region = Screen().new_region(0, image_find(NavBar.HOME_BUTTON).y, Screen.SCREEN_WIDTH / 4,
                                                     Screen.SCREEN_HEIGHT / 3)
        expected_4 = history_sidebar_region.exists(history_sidebar_mozilla_pattern, 10)
        assert expected_4, 'Mozilla page is displayed in the History list successfully.'

        history_sidebar_region.right_click(history_sidebar_mozilla_pattern, 1)
        time.sleep(Settings.DEFAULT_UI_DELAY)
        type(text='b')

        expected_5 = exists(save_bookmark_button_pattern, 10)
        assert expected_5, 'New Bookmark popup displayed properly.'

        click(save_bookmark_button_pattern, FirefoxSettings.TINY_FIREFOX_TIMEOUT)

        try:
            expected_6 = wait_vanish(save_bookmark_button_pattern, 10)
            assert expected_6, 'New Bookmark popup was closed successfully.'
        except FindError:
            raise FindError('New Bookmark popup is still open')

        # Open the library and check that the page was bookmarked with default settings
        open_library()

        expected_7 = exists(library_expand_bookmarks_menu_pattern, 10)
        assert expected_7, 'Expand bookmarks menu button displayed properly.'

        click(library_expand_bookmarks_menu_pattern)

        expected_8 = exists(library_bookmarks_mozilla_pattern, 10)
        assert expected_8, 'Mozilla page is bookmarked with default name and without tags.'

        click_window_control('close')

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Bookmark a website from the Library - History menu.',
        locale=['en-US'],
        test_case_id='174043',
        test_suite_id='2000',
        profile=Profiles.TEN_BOOKMARKS
    )
    def run(self, firefox):
        show_all_history_pattern = History.HistoryMenu.SHOW_ALL_HISTORY
        iris_bookmark_pattern = Pattern('iris_bookmark.png')
        iris_bookmark_focus_pattern = Pattern('iris_bookmark_focus.png')
        library_bookmarks_iris_pattern = Pattern('library_bookmarks_iris.png')
        library_expand_bookmarks_menu_pattern = Library.BOOKMARKS_MENU
        save_bookmark_button_pattern = Pattern('save_bookmark_name.png')

        # Open History and check if it is populated with the Iris page.
        open_library_menu('History')

        right_upper_corner = Screen().new_region(Screen.SCREEN_WIDTH / 2, 0, Screen.SCREEN_WIDTH / 2,
                                                 Screen.SCREEN_HEIGHT / 2)
        expected = right_upper_corner.exists(iris_bookmark_pattern, 10)
        assert expected, 'Iris page is displayed in the History menu list.'

        try:
            wait(show_all_history_pattern, 10)
            logger.debug('Show All History option found.')
            click(show_all_history_pattern)
        except FindError:
            raise FindError('Show All History option is not present on the page, aborting.')

        expected = exists(iris_bookmark_focus_pattern, 10)
        assert expected, 'Iris page is displayed in the Recent History list.'

        right_click_and_type(iris_bookmark_focus_pattern, keyboard_action='b')

        # Bookmark the website.
        expected = exists(save_bookmark_button_pattern, 10)
        assert expected, 'New Bookmark popup displayed properly.'

        click(save_bookmark_button_pattern)

        try:
            expected = wait_vanish(save_bookmark_button_pattern, 10)
            assert expected, 'New Bookmark popup was closed successfully.'
        except FindError:
            raise FindError('New Bookmark popup is still open')

        click_window_control('close')
        time.sleep(Settings.DEFAULT_UI_DELAY)

        # Open the library and check that the page was bookmarked with default settings.
        open_library()

        expected = exists(library_expand_bookmarks_menu_pattern, 10)
        assert expected, 'Expand bookmarks menu button displayed properly.'

        click(library_expand_bookmarks_menu_pattern)

        expected = exists(library_bookmarks_iris_pattern, 10)
        assert expected, 'The website is bookmarked in the Bookmarks Menu folder, with the default name and ' \
                         'without any tags.'

        click_window_control('close')

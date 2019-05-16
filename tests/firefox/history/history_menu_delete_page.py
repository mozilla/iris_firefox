# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Delete a page from the Library - History menu.',
        locale=['en-US'],
        test_case_id='174048',
        test_suite_id='2000',
        profile=Profiles.TEN_BOOKMARKS
    )
    def run(self, firefox):
        show_all_history = History.HistoryMenu.SHOW_ALL_HISTORY
        iris_bookmark = Pattern('iris_bookmark.png')
        iris_bookmark_focus = Pattern('iris_bookmark_focus.png')

        # Open History and check if is populated with Iris page.
        open_library_menu('History')

        right_upper_corner = Screen().new_region(Screen.SCREEN_WIDTH / 2, 0, Screen.SCREEN_WIDTH / 2,
                                                 Screen.SCREEN_HEIGHT / 2)
        expected_1 = right_upper_corner.exists(iris_bookmark, 10)
        assert expected_1, 'Iris page is displayed in the History menu list successfully.'

        try:
            wait(show_all_history, 10)
            logger.debug('Show All History option found.')
            click(show_all_history)
        except FindError:
            raise FindError('Show All History option is not present on the page, aborting.')

        expected_2 = exists(iris_bookmark_focus, 10)
        assert expected_2, 'Iris page is displayed Recent History list successfully.'

        # Delete Iris page.
        right_click_and_type(iris_bookmark_focus, keyboard_action='d')

        try:
            expected_3 = wait_vanish(iris_bookmark_focus, 10)
            assert expected_3, 'Iris page was deleted successfully from the history.'
        except FindError:
            raise FindError('Iris page is still displayed in the history.')

        click_window_control('close')

        # Check that Mozilla page is not displayed in the Recent History list.
        open_library_menu('History')

        expected_4 = exists(iris_bookmark, 5)
        assert expected_4 is not True, 'Iris page is not displayed in the History menu list.'

        type(Key.ESC)

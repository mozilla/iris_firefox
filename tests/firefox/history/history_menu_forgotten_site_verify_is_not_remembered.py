# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Verify if the deleted page from History is not retained by auto-complete.',
        locale='[en-US]',
        test_case_id='174051',
        test_suite_id='2000'
    )
    def test_run(self, firefox):
        show_all_history = History.HistoryMenu.SHOW_ALL_HISTORY
        mozilla_bookmark_focus = Pattern('mozilla_bookmark_focus.png')
        mozilla_autocomplete = Pattern('mozilla_autocomplete.png')
        recent_history_mozilla_pattern = Pattern('recent_history_mozilla.png')

        # Visit a page at least two times to make sure that auto-fill is working in the URL bar.
        new_tab()
        navigate(LocalWeb.MOZILLA_TEST_SITE)
        navigate(LocalWeb.MOZILLA_TEST_SITE)

        select_location_bar()
        paste('http://127.0.0.1:2000/m')

        expected_1 = exists(mozilla_autocomplete, 10)
        assert expected_1, 'Mozilla page is auto-completed successfully.'

        close_tab()
        new_tab()

        # Navigate to history and forget the Mozilla page.
        open_library_menu('History')

        right_upper_corner = Screen().new_region(Screen.SCREEN_WIDTH / 2, 0, Screen.SCREEN_WIDTH / 2,
                                                 Screen.SCREEN_HEIGHT / 2)

        expected_2 = right_upper_corner.exists(recent_history_mozilla_pattern, 10)
        assert expected_2, 'Mozilla page is displayed in the Recent History list.'

        try:
            wait(show_all_history, 10)
            logger.debug('Show All History option found.')
            click(show_all_history)
        except FindError:
            raise FindError('Show All History option is not present on the page, aborting.')

        expected_3 = exists(mozilla_bookmark_focus, 10)
        assert expected_3, 'Mozilla page is displayed in the History list successfully.'


        right_click_and_type(mozilla_bookmark_focus, keyboard_action='f')


        try:
            expected_4 = wait_vanish(mozilla_bookmark_focus, 10)
            assert expected_4, 'Mozilla page was deleted successfully from the Library.'
        except FindError:
            raise FindError('Mozilla page is still displayed in the Library.')

        click_window_control('close')

        # Check that Mozilla page is not displayed in the Recent History list.
        open_library_menu('History')

        expected_5 = wait_vanish(recent_history_mozilla_pattern, 5)
        assert expected_5, 'Mozilla page is not displayed in the Recent History list.'

        # Check that the forgotten page is not auto-completed in the URL bar.
        select_location_bar()
        paste('http://127.0.0.1:2000/m')

        expected_6 = wait_vanish(mozilla_autocomplete.similar(0.9), 10)
        assert expected_6, 'Mozilla page is not auto-completed in the URL bar.'

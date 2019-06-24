# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Verify if the deleted page from History is not retained by auto-complete.',
        locale=['en-US'],
        test_case_id='174051',
        test_suite_id='2000'
    )
    def run(self, firefox):
        show_all_history_pattern = History.HistoryMenu.SHOW_ALL_HISTORY
        mozilla_bookmark_focus_pattern = Pattern('mozilla_bookmark_focus.png')
        mozilla_autocomplete_pattern = Pattern('mozilla_autocomplete.png')
        recent_history_mozilla_pattern = Pattern('recent_history_mozilla.png')

        # Visit a page at least two times to make sure that auto-fill is working in the URL bar.
        new_tab()
        navigate(LocalWeb.MOZILLA_TEST_SITE)
        navigate(LocalWeb.MOZILLA_TEST_SITE)

        select_location_bar()

        type('http://127.0.0.1:2000/m', interval=0.1)

        mozilla_autocomplete_exists = exists(mozilla_autocomplete_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert mozilla_autocomplete_exists, 'Mozilla page is auto-completed successfully.'

        close_tab()
        new_tab()

        # Navigate to history and forget the Mozilla page.
        open_library_menu('History')

        right_upper_corner = Screen().new_region(Screen.SCREEN_WIDTH / 2, 0, Screen.SCREEN_WIDTH / 2,
                                                 Screen.SCREEN_HEIGHT / 2)

        recent_history_mozilla_exists = right_upper_corner.exists(recent_history_mozilla_pattern,
                                                                  FirefoxSettings.FIREFOX_TIMEOUT)
        assert recent_history_mozilla_exists, 'Mozilla page is displayed in the Recent History list.'

        show_all_history_exists = exists(show_all_history_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert show_all_history_exists, 'Show All History option found.'

        click(show_all_history_pattern)

        mozilla_bookmark_focus_exists = exists(mozilla_bookmark_focus_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert mozilla_bookmark_focus_exists, 'Mozilla page is displayed in the History list successfully.'

        right_click_and_type(mozilla_bookmark_focus_pattern, keyboard_action='f')

        try:
            mozilla_bookmark_focus_vanished = wait_vanish(mozilla_bookmark_focus_pattern,
                                                          FirefoxSettings.FIREFOX_TIMEOUT)
            assert mozilla_bookmark_focus_vanished, 'Mozilla page was deleted successfully from the Library.'
        except FindError:
            raise FindError('Mozilla page is still displayed in the Library.')

        click_window_control('close')

        # Check that Mozilla page is not displayed in the Recent History list.
        open_library_menu('History')

        recent_history_mozilla_exists = exists(recent_history_mozilla_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert recent_history_mozilla_exists is False, 'Mozilla page is not displayed in the Recent History list.'

        # Check that the forgotten page is not auto-completed in the URL bar.
        select_location_bar()
        type('http://127.0.0.1:2000/m', interval=0.1)

        mozilla_autocomplete_exists = exists(mozilla_autocomplete_pattern.similar(0.9), FirefoxSettings.FIREFOX_TIMEOUT)
        assert mozilla_autocomplete_exists is False, 'Mozilla page is not auto-completed in the URL bar.'

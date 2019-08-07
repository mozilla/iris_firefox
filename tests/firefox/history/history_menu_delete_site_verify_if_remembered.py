# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Verify if the deleted page from History is retained in auto-complete.',
        locale=['en-US'],
        test_case_id='174049',
        test_suite_id='2000'
    )
    def run(self, firefox):
        local_server_autocomplete_pattern = Pattern('local_server_autocomplete.png')
        mozilla_bookmark_focus_pattern = Pattern('mozilla_bookmark_focus.png')
        pocket_autocomplete_pattern = Pattern('pocket_autocomplete.png')
        mozilla_autocomplete_pattern = Pattern('mozilla_autocomplete.png').similar(.7)

        # Visit two pages from the same domain at least two times to make sure that auto-fill is working in the URL bar.
        new_tab()

        navigate(LocalWeb.POCKET_TEST_SITE)

        pocket_page_opened = exists(LocalWeb.POCKET_LOGO, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert pocket_page_opened, 'Pocket page opened'

        new_tab()

        navigate(LocalWeb.MOZILLA_TEST_SITE)

        mozilla_page_opened = exists(LocalWeb.MOZILLA_LOGO, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert mozilla_page_opened, 'Mozilla page opened'

        new_tab()

        select_location_bar()
        type('127.0.0.1:2000/p',  interval=0.2)

        pocket_autocomplete_exists = exists(pocket_autocomplete_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert pocket_autocomplete_exists, 'Pocket page is auto-completed successfully.'

        click(NavBar.FORWARD_BUTTON.target_offset(-50, 0), align=Alignment.TOP_LEFT)

        select_location_bar()
        type('127.0.0.1:2000/m', interval=0.2)

        mozilla_autocomplete_exists = exists(mozilla_autocomplete_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert mozilla_autocomplete_exists, 'Mozilla page is auto-completed successfully.'

        close_tab()
        new_tab()

        # Open History and check if is populated with Mozilla page.
        open_history_library_window()

        library_history = exists(Library.HISTORY, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert library_history, 'Library popup window available'

        library_history_location = find(Library.HISTORY)
        bookmarks_region = Region(library_history_location.x, library_history_location.y,
                                  Screen.SCREEN_WIDTH - library_history_location.x,
                                  Screen.SCREEN_HEIGHT - library_history_location.y)

        mozilla_bookmark_focus_exists = exists(mozilla_bookmark_focus_pattern, FirefoxSettings.FIREFOX_TIMEOUT,
                                               region=bookmarks_region)
        assert mozilla_bookmark_focus_exists, 'Mozilla page is displayed in the History list successfully.'

        # Delete Mozilla page.
        right_click(mozilla_bookmark_focus_pattern, region=bookmarks_region)

        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT/3)

        type('d')

        try:
            mozilla_bookmark_focus_vanished = wait_vanish(mozilla_bookmark_focus_pattern,
                                                          FirefoxSettings.FIREFOX_TIMEOUT, region=bookmarks_region)
            assert mozilla_bookmark_focus_vanished, 'Mozilla page was deleted successfully from the history.'
        except FindError:
            raise FindError('Mozilla page is still displayed in the history.')

        click_window_control('close')

        # Check that the local server is still auto-completed in the URL bar.
        select_location_bar()
        type('127')

        local_server_autocomplete_exists = exists(local_server_autocomplete_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert local_server_autocomplete_exists, 'Local server is auto-completed successfully.'

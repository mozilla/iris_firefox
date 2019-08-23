# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Verify if the deleted page from History is not retained in auto-complete.',
        locale=['en-US'],
        test_case_id='216273',
        test_suite_id='2000'
    )
    def run(self, firefox):
        mozilla_bookmark_focus_pattern = Pattern('mozilla_bookmark_focus.png')
        mozilla_autocomplete_pattern = Pattern('mozilla_autocomplete.png').similar(0.7)

        # Visit a page at least two times to make sure that auto-fill is working in the URL bar.
        new_tab()
        navigate(LocalWeb.MOZILLA_TEST_SITE)

        test_page_opened = exists(LocalWeb.MOZILLA_LOGO, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert test_page_opened, 'Test page is opened'

        select_location_bar()
        type('http://127.0.0.1:2000/m')

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

        # Check that the deleted page is not auto-completed in the URL bar.
        select_location_bar()
        type('http://127.0.0.1:2000/m')

        mozilla_autocomplete_exists = exists(mozilla_autocomplete_pattern.similar(0.9), FirefoxSettings.FIREFOX_TIMEOUT)
        assert mozilla_autocomplete_exists is False, 'Mozilla page is not auto-completed in URL bar.'

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Websites can be bookmarked from private browsing.',
        locale=['en-US'],
        test_case_id='4155',
        test_suite_id='2525'
    )
    def run(self, firefox):
        history_dropdown_pattern = Pattern('history_dropdown_button.png')
        restart_browser_pattern = Pattern('restart_browser.png')
        never_remember_history_pattern = Pattern('never_remember_history.png')
        bookmark_button_pattern = LocationBar.STAR_BUTTON_UNSTARRED

        navigate('about:preferences#privacy')

        privacy_page_assert = exists(AboutPreferences.PRIVACY_AND_SECURITY_BUTTON_SELECTED,
                                     FirefoxSettings.FIREFOX_TIMEOUT)
        assert privacy_page_assert is True, 'Privacy page has been accessed.'

        paste('remember')

        try:
            wait(history_dropdown_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
            logger.debug('History dropdown list can be accessed.')
            click(history_dropdown_pattern)
        except FindError:
            raise FindError('History dropdown list can NOT be accessed, aborting.')

        try:
            wait(never_remember_history_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
            logger.debug('Never Remember History option is present in the dropdown list.')
            click(never_remember_history_pattern)
        except FindError:
            raise FindError('Never Remember History option is NOT present in the dropdown list, aborting')

        restart_browser_popup_assert = exists(restart_browser_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert restart_browser_popup_assert is True, 'History option can be changed.'

        click(restart_browser_pattern)

        # wait_for_firefox_restart()

        time.sleep(5)

        firefox_restarted = exists(NavBar.HOME_BUTTON)
        assert firefox_restarted is True, 'Firefox successfully restarted'

        navigate(LocalWeb.MOZILLA_TEST_SITE)

        mozilla_page_assert = exists(LocalWeb.MOZILLA_LOGO, FirefoxSettings.FIREFOX_TIMEOUT)
        assert mozilla_page_assert is True, 'Mozilla page loaded successfully.'

        try:
            wait(bookmark_button_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
            logger.debug('Bookmark star is present on the page.')
            click(bookmark_button_pattern)
        except FindError:
            raise FindError('Bookmark star is not present on the page, aborting.')

        page_bookmarked_assert = exists(Bookmarks.StarDialog.NEW_BOOKMARK, FirefoxSettings.FIREFOX_TIMEOUT)
        assert page_bookmarked_assert is True, 'The page was successfully bookmarked via star button.'

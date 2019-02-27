# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Websites can be bookmarked from private browsing.'
        self.test_case_id = '4155'
        self.test_suite_id = '2525'
        self.locales = ['en-US']

    def run(self):

        history_dropdown_pattern = Pattern('history_dropdown_button.png')
        privacy_page_pattern = Pattern('privacy_page.png')
        restart_browser_pattern = Pattern('restart_browser.png')
        never_remember_history_pattern = Pattern('never_remember_history.png')
        bookmark_button_pattern = LocationBar.STAR_BUTTON_UNSTARRED

        navigate('about:preferences#privacy')

        privacy_page_assert = exists(privacy_page_pattern, 10)
        assert_true(self, privacy_page_assert, 'Privacy page has been accessed.')

        paste('remember')

        try:
            wait(history_dropdown_pattern, 10)
            logger.debug('History dropdown list can be accessed.')
            click(history_dropdown_pattern)
        except FindError:
            raise FindError('History dropdown list can NOT be accessed, aborting.')

        try:
            wait(never_remember_history_pattern, 10)
            logger.debug('Never Remember History option is present in the dropdown list.')
            click(never_remember_history_pattern)
        except FindError:
            raise FindError('Never Remember History option is NOT present in the dropdown list, aborting')

        restart_browser_popup_assert = exists(restart_browser_pattern, 10)
        assert_true(self, restart_browser_popup_assert, 'History option can be changed.')

        click(restart_browser_pattern)
        wait_for_firefox_restart()

        navigate(LocalWeb.MOZILLA_TEST_SITE)

        mozilla_page_assert = exists(LocalWeb.MOZILLA_LOGO, 10)
        assert_true(self, mozilla_page_assert, 'Mozilla page loaded successfully.')

        try:
            wait(bookmark_button_pattern, 10)
            logger.debug('Bookmark star is present on the page.')
            click(bookmark_button_pattern)
        except FindError:
            raise FindError('Bookmark star is not present on the page, aborting.')

        page_bookmarked_assert = exists(Bookmarks.StarDialog.NEW_BOOKMARK, 10)
        assert_true(self, page_bookmarked_assert, 'The page was successfully bookmarked via star button.')

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Websites can be bookmarked from a private window.'
        self.test_case_id = '4176'
        self.test_suite_id = '2525'
        self.locales = ['en-US']

    def run(self):
        new_private_window()

        private_window_displayed = exists(PrivateWindow.private_window_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, private_window_displayed, 'Private browsing window is displayed on the screen')

        navigate(LocalWeb.MOZILLA_TEST_SITE)

        mozilla_page_assert = exists(LocalWeb.MOZILLA_LOGO, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, mozilla_page_assert, 'Mozilla page loaded successfully.')

        star_button_unstarred_displayed = exists(LocationBar.STAR_BUTTON_UNSTARRED, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, star_button_unstarred_displayed, 'Bookmark star is present on the page.')

        click(LocationBar.STAR_BUTTON_UNSTARRED)

        page_bookmarked_assert = exists(Bookmarks.StarDialog.NEW_BOOKMARK, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, page_bookmarked_assert, 'The page was successfully bookmarked from a private window.')

        close_window()

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Websites can be bookmarked from a private window.',
        locale=['en-US'],
        test_case_id='4176',
        test_suite_id='2525'
    )
    def run(self, firefox):
        new_private_window()

        private_window_displayed = exists(PrivateWindow.private_window_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert private_window_displayed is True, 'Private browsing window is displayed on the screen'

        navigate(LocalWeb.MOZILLA_TEST_SITE)

        mozilla_page_assert = exists(LocalWeb.MOZILLA_LOGO, FirefoxSettings.FIREFOX_TIMEOUT)
        assert mozilla_page_assert is True, 'Mozilla page loaded successfully.'

        star_button_unstarred_displayed = exists(LocationBar.STAR_BUTTON_UNSTARRED, FirefoxSettings.FIREFOX_TIMEOUT)
        assert star_button_unstarred_displayed is True, 'Bookmark star is present on the page.'

        click(LocationBar.STAR_BUTTON_UNSTARRED)

        page_bookmarked_assert = exists(Bookmarks.StarDialog.NEW_BOOKMARK, FirefoxSettings.FIREFOX_TIMEOUT)
        assert page_bookmarked_assert is True, 'The page was successfully bookmarked from a private window.'

        close_window()

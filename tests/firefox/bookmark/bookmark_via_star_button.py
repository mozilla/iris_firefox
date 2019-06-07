# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Websites can be bookmarked via star-shaped button.',
        locale=['en-US'],
        test_case_id='163398',
        test_suite_id='2525'
    )
    def run(self, firefox):
        bookmark_button_pattern = LocationBar.STAR_BUTTON_UNSTARRED

        navigate(LocalWeb.MOZILLA_TEST_SITE)

        mozilla_page_assert = exists(LocalWeb.MOZILLA_LOGO, FirefoxSettings.FIREFOX_TIMEOUT)
        assert mozilla_page_assert, 'Mozilla page loaded successfully.'

        try:
            wait(bookmark_button_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
            logger.debug('Bookmark star is present on the page.')
            click(bookmark_button_pattern)
        except FindError:
            raise FindError('Bookmark star is not present on the page, aborting.')

        page_bookmarked_assert = exists(Bookmarks.StarDialog.NEW_BOOKMARK, FirefoxSettings.FIREFOX_TIMEOUT)
        assert page_bookmarked_assert, 'The page was successfully bookmarked via star button.'

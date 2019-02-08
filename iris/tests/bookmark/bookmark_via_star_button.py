# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Websites can be bookmarked via star-shaped button.'
        self.test_case_id = '163398'
        self.test_suite_id = '2525'
        self.locales = ['en-US']

    def run(self):

        bookmark_button_pattern = LocationBar.STAR_BUTTON_UNSTARRED

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

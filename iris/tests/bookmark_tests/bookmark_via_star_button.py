# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'Websites can be bookmarked via star-shaped button.'
        self.test_case_id = '4087'
        self.test_suite_id = '75'

    def run(self):

        bookmark_button_pattern = LocationBar.BOOKMARK_BUTTON

        navigate(LocalWeb.MOZILLA_TEST_SITE)

        try:
            wait(bookmark_button_pattern, 10)
            logger.debug('Bookmark star is present on the page.')
            click(bookmark_button_pattern)
        except FindError:
            raise FindError('Bookmark star is not present on the page, aborting.')

        page_bookmarked_assert = exists('page_bookmarked.png', 10)
        assert_true(self, page_bookmarked_assert, 'The page was successfully bookmarked via star button.')

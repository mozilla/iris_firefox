# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'Tags can be added to bookmarks using the star-shaped button.'
        self.test_case_id = '4145'
        self.test_suite_id = '75'

    def run(self):

        bookmark_button_pattern = LocationBar.BOOKMARK_BUTTON
        tags_field = Pattern('tags_field.png')
        done = Pattern('done_button.png')
        moz_tagged_bookmark = Pattern('moz_sidebar_bookmark.png')

        navigate(LocalWeb.MOZILLA_TEST_SITE)

        mozilla_page_assert = exists(LocalWeb.MOZILLA_LOGO, 10)
        assert_true(self, mozilla_page_assert, 'Mozilla page loaded successfully.')

        try:
            wait(bookmark_button_pattern, 10)
            logger.debug('Bookmark star is present on the page.')
            click(bookmark_button_pattern)
        except FindError:
            raise FindError('Bookmark star is not present on the page, aborting.')

        page_bookmarked_assert = exists(Pattern('page_bookmarked.png'), 10)
        assert_true(self, page_bookmarked_assert, 'The page was successfully bookmarked via star button.')

        try:
            wait(tags_field, 10)
            logger.debug('Tags field can be edit.')
            click(tags_field)
        except FindError:
            raise FindError('Tags field is NOT present on the page, aborting.')

        paste('Iris')

        try:
            wait(done, 10)
            logger.debug('Done button is present on the page.')
            click(done)
        except FindError:
            raise FindError('Done button is NOT present on the page.')

        bookmarks_sidebar('open')

        paste('Iris')

        tagged_bookmark_assert = exists(moz_tagged_bookmark, 10)
        assert_true(self, tagged_bookmark_assert, 'Moz bookmark has been successfully tagged.')

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Bookmarks can be removed from the Bookmarks Sidebar.'
        self.test_case_id = '168933'
        self.test_suite_id = '2525'
        self.locales = ['en-US']

    def setup(self):
        """Test case setup

        Override the setup method to use a pre-canned bookmarks profile.
        """
        BaseTest.setup(self)
        self.profile = Profile.TEN_BOOKMARKS
        return

    def run(self):

        moz_bookmark_pattern = Pattern('moz_sidebar_bookmark.png')
        delete_pattern = Pattern('delete_bookmark.png')

        navigate('about:blank')

        bookmarks_sidebar('open')

        paste('mozilla')

        try:
            wait(moz_bookmark_pattern, 10)
            logger.debug('Moz bookmark is present in the Bookmark sidebar.')
            right_click(moz_bookmark_pattern)
        except FindError:
            raise FindError('Moz bookmark is NOT present in the Bookmark sidebar, aborting.')

        bookmark_options(delete_pattern)

        try:
            deleted_bookmark_assert = wait_vanish(moz_bookmark_pattern, 10)
            assert_true(self, deleted_bookmark_assert,
                        'Moz bookmark is successfully deleted from the Bookmark sidebar.')
        except FindError:
            raise FindError('Moz bookmark can NOT be deleted from the Bookmark sidebar, aborting.')

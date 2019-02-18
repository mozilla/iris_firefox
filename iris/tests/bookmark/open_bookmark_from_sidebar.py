# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Bookmarks can be opened from the Bookmarks Sidebar.'
        self.test_case_id = '168924'
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

        navigate('about:blank')

        bookmarks_sidebar('open')

        paste('mozilla')

        try:
            wait(moz_bookmark_pattern, 10)
            logger.debug('Moz bookmark is present in the Bookmark sidebar.')
            click(moz_bookmark_pattern)
        except FindError:
            raise FindError('Moz bookmark is NOT present in the Bookmark sidebar, aborting.')

        mozilla_page_assert = exists(LocalWeb.MOZILLA_LOGO, 10)
        assert_true(self, mozilla_page_assert, 'Mozilla page loaded successfully.')

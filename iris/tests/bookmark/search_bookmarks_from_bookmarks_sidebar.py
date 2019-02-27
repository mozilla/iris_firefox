# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Searching for bookmarks from the Bookmarks Sidebar works properly.'
        self.test_case_id = '168922'
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
        properties_pattern = Pattern('properties_option.png')
        save_pattern = Pattern('save_bookmark_name.png')

        navigate('about:blank')

        bookmarks_sidebar('open')

        paste('mozilla')

        try:
            wait(moz_bookmark_pattern, 10)
            logger.debug('Moz bookmark is present in the Bookmark sidebar.')
            right_click(moz_bookmark_pattern)
        except FindError:
            raise FindError('Moz bookmark is NOT present in the Bookmark sidebar, aborting.')

        option_assert = exists(properties_pattern, 10)
        assert_true(self, option_assert, 'Properties option is present on the page.')

        click(properties_pattern)

        properties_window_assert = exists(save_pattern, 10)
        assert_true(self, properties_window_assert, 'Properties window is present on the page.')

        for i in range(2):
            type(Key.TAB)

        paste('iris')

        click(save_pattern)

        bookmarks_sidebar('close')

        bookmarks_sidebar('open')

        paste('iris')

        tagged_bookmark_assert = exists(moz_bookmark_pattern, 10)
        assert_true(self, tagged_bookmark_assert, 'Moz bookmark was successfully tagged via bookmark sidebar.')

        click(moz_bookmark_pattern)

        mozilla_page_assert = exists(LocalWeb.MOZILLA_LOGO, 10)
        assert_true(self, mozilla_page_assert, 'Mozilla page loaded successfully.')

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):
    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Bookmarks can be loaded inside the Bookmarks Sidebar.'
        # This feature was removed from Firefox 63 and beyond in bug 1452645.
        self.fx_version = '<=62'
        self.test_case_id = '4162'
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
        save_pattern = Pattern('save_bookmark_name.png')
        access_sidebar_moz_pattern = Pattern('moz_sidebar_bookmark_location_changed.png')
        load_sidebar_bookmark = Pattern('load_sidebar_bookmark.png')

        navigate('about:blank')

        bookmarks_sidebar('open')

        paste('mozilla')

        sidebar_bookmark_assert = exists(moz_bookmark_pattern, 10)
        assert_true(self, sidebar_bookmark_assert, 'Moz bookmark is present in the sidebar.')

        right_click(moz_bookmark_pattern)

        bookmark_options(Pattern('properties_option.png'))

        properties_window_assert = exists(save_pattern, 10)
        assert_true(self, properties_window_assert, 'Properties window is present on the page.')

        click(load_sidebar_bookmark)

        try:
            wait(save_pattern, 10)
            logger.debug('Changes can be saved.')
            click(save_pattern)
        except FindError:
            raise FindError('Can\'t find save button, aborting.')

        amazon_sidebar_assert = exists(access_sidebar_moz_pattern, 10)
        assert_true(self, amazon_sidebar_assert, 'Moz bookmark can be accessed.')

        click(access_sidebar_moz_pattern)

        bookmark_load_in_sidebar_assert = exists(Pattern('moz_bookmark_sidebar_page_title.png'), 10)
        assert_true(self, bookmark_load_in_sidebar_assert,
                    'Moz bookmark is successfully loaded inside the Bookmarks Sidebar.')

        sidebar_scroll_assert = exists(Pattern('sidebar_scroll.png'), 10)
        assert_true(self, sidebar_scroll_assert, 'Horizontal scrollbar is available for the sidebar.')

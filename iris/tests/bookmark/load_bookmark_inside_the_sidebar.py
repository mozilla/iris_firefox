# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):
    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This is a test case that check if a bookmark can be loaded inside the Bookmarks Sidebar.'
        self.fx_version = '<=62'
        self.test_case_id = '4162'
        self.test_suite_id = '75'

    def run(self):

        amazon_home_pattern = Pattern('amazon.png')
        amazon_bookmark_pattern = Pattern('sidebar_bookmark.png')
        save_pattern = Pattern('save_bookmark_name.png')
        access_sidebar_amazon_pattern = Pattern('sidebar_bookmark_location_changed.png')

        navigate('www.amazon.com')

        amazon_banner_assert = exists(amazon_home_pattern, 10)
        assert_true(self, amazon_banner_assert, 'Amazon page has been successfully loaded.')

        try:
            wait(Pattern('amazon_favicon.png'), 15)
            logger.debug('Page is fully loaded and favicon displayed.')
        except FindError:
            logger.error('Page is not fully loaded, aborting.')
            raise FindError

        bookmark_page()

        page_bookmarked_assert = exists(Pattern('page_bookmarked.png'), 10)
        assert_true(self, page_bookmarked_assert, 'Page was bookmarked.')

        navigate('about:blank')

        bookmarks_sidebar('open')

        paste('amazon')

        sidebar_bookmark_assert = exists(amazon_bookmark_pattern, 10)
        assert_true(self, sidebar_bookmark_assert, 'Amazon bookmark is present in the sidebar.')

        right_click(amazon_bookmark_pattern)

        bookmark_options(Pattern('properties_option.png'))

        properties_window_assert = exists(save_pattern, 10)
        assert_true(self, properties_window_assert, 'Properties window is present on the page.')

        click(Pattern('load_sidebar_bookmark.png'))

        try:
            wait(save_pattern, 10)
            logger.debug('Changes can be saved.')
            click(save_pattern)
        except FindError:
            logger.error('Can\'t find save button, aborting.')
            raise FindError

        amazon_sidebar_assert = exists(access_sidebar_amazon_pattern, 10)
        assert_true(self, amazon_sidebar_assert, 'Amazon bookmark can be accessed.')

        click(access_sidebar_amazon_pattern)

        bookmark_load_in_sidebar_assert = exists(Pattern('bookmark_sidebar_page_title.png'), 10)
        assert_true(self, bookmark_load_in_sidebar_assert,
                    'Amazon bookmark is successfully loaded inside the Bookmarks Sidebar.')

        sidebar_scroll_assert = exists(Pattern('sidebar_scroll.png'), 10)
        assert_true(self, sidebar_scroll_assert, 'Horizontal scrollbar is available for the sidebar.')

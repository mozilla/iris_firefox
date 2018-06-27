# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):
    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This is a test case that check if a bookmark can be loaded inside the Bookmarks Sidebar.'

    def run(self):

        amazon_home = 'amazon.png'
        amazon_bookmark = 'sidebar_bookmark.png'
        save = 'save_bookmark_name.png'
        access_sidebar_amazon = 'sidebar_bookmark_location_changed.png'

        navigate('www.amazon.com')

        amazon_banner_assert = exists(amazon_home, 10)
        assert_true(self, amazon_banner_assert, 'Amazon page has been successfully loaded.')

        try:
            wait('amazon_favicon.png', 15)
            logger.debug('Page is fully loaded and favicon displayed.')
        except FindError:
            logger.error('Page is not fully loaded, aborting.')
            raise FindError

        bookmark_page()

        page_bookmarked_assert = exists('page_bookmarked.png', 10)
        assert_true(self, page_bookmarked_assert, 'Page was bookmarked.')

        navigate('about:blank')

        bookmarks_sidebar()

        try:
            wait('bookmark_sidebar.png', 10)
            logger.debug('Sidebar is opened.')
        except FindError:
            logger.error('Sidebar is not opened, aborting.')
            raise FindError

        paste('amazon')

        sidebar_bookmark_assert = exists(amazon_bookmark, 10)
        assert_true(self, sidebar_bookmark_assert, 'Amazon bookmark is present in the sidebar.')

        rightClick(amazon_bookmark)

        bookmark_options('properties_option.png')

        properties_window_assert = exists(save, 10)
        assert_true(self, properties_window_assert, 'Properties window is present on the page.')

        click('load_sidebar_bookmark.png')

        try:
            wait(save, 10)
            logger.debug('Changes can be saved.')
            click(save)
        except FindError:
            logger.error('Can\'t find save button, aborting.')
            raise FindError

        amazon_sidebar_assert = exists(access_sidebar_amazon, 10)
        assert_true(self, amazon_sidebar_assert, 'Amazon bookmark can be accessed.')

        click(access_sidebar_amazon)

        bookmark_load_in_sidebar_assert = exists('bookmark_sidebar_page_title.png', 10)
        assert_true(self, bookmark_load_in_sidebar_assert, 'Amazon bookmark is successfully loaded inside the ' \
                                                           'Bookmarks Sidebar.')

        sidebar_scroll_assert = exists('sidebar_scroll.png', 10)
        assert_true(self, sidebar_scroll_assert, 'Horizontal scrollbar is available for the sidebar.')

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):
    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This is a test case that check if the location of a bookmark can be changed.'

    def run(self):

        amazon_home = 'amazon.png'
        view_bookmarks_toolbar = 'view_bookmarks_toolbar.png'
        active_toolbar = 'toolbar_is_active.png'
        amazon_bookmark = 'amazon_bookmark.png'
        drag_area = 'drag_area.png'
        save = 'save_bookmark_name.png'
        changed_toolbar_bookmark = 'changed_toolbar_bookmark.png'
        bookmark_changed_location = 'bookmark_changed_location.png'
        sidebar_bookmark_location_changed = 'sidebar_bookmark_location_changed.png'

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

        bookmarks_sidebar('open')

        paste('amazon')

        sidebar_bookmark_assert = exists(amazon_bookmark, 10)
        assert_true(self, sidebar_bookmark_assert, 'Amazon bookmark is present in the sidebar.')

        rightClick(amazon_bookmark)

        bookmark_options('properties_option.png')

        properties_window_assert = exists(save, 10)
        assert_true(self, properties_window_assert, 'Properties window is present on the page.')

        type(Key.TAB)

        paste('www.bing.com')

        click(save)

        try:
            wait(sidebar_bookmark_location_changed)
            logger.debug('Changed bookmark is present in Bookmark sidebar.')
            click(sidebar_bookmark_location_changed)
        except FindError:
            logger.error('Can\'t find the bookmark in Bookmark sidebar, aborting.')

        bookmark_location_assert = exists('bing_favicon.png')
        assert_true(self, bookmark_location_assert, 'The URL of the bookmark is successfully modified.')

        navigate('about:blank')

        access_bookmarking_tools(view_bookmarks_toolbar)

        try:
            wait(active_toolbar, 10)
            logger.debug('Toolbar has been activated.')
        except FindError:
            logger.error('Toolbar can not be activated, aborting.')
            raise FindError

        dragDrop(bookmark_changed_location, drag_area, 0.5)

        try:
            wait(changed_toolbar_bookmark, 10)
            logger.debug('Bookmark is present in Bookmark Toolbar section.')
            rightClick(changed_toolbar_bookmark)
        except FindError:
            logger.error('Can\'t find the bookmark in Bookmark Toolbar section, aborting.')
            raise FindError

        bookmark_options('properties_option.png')

        properties_window_assert = exists(save, 10)
        assert_true(self, properties_window_assert, 'Properties window is present on the page.')

        type(Key.TAB)

        paste('www.amazon.com')

        click(save)

        try:
            wait(changed_toolbar_bookmark, 10)
            logger.debug('Bookmark is present in Bookmark Toolbar section.')
            click(changed_toolbar_bookmark)
        except FindError:
            logger.error('Can\'t find the bookmark in Bookmark Toolbar section, aborting.')

        amazon_favicon_assert = exists('amazon_favicon.png', 15)
        assert_true(self, amazon_favicon_assert, 'The URL of the bookmark is successfully modified.')

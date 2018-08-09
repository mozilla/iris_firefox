# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):
    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This is a test case that check if the location of a bookmark can be changed.'
        self.test_case_id = '4149'
        self.test_suite_id = '75'

    def run(self):

        amazon_home_pattern = Pattern('amazon.png')
        view_bookmarks_toolbar_pattern = LibraryMenu.BookmarksOption.BookmarkingTools.VIEW_BOOKMARKS_TOOLBAR
        bookmarks_toolbar_most_visited_pattern = SidebarBookmarks.BookmarksToolbar.MOST_VISITED
        amazon_bookmark_pattern = Pattern('amazon_bookmark.png')
        drag_area_pattern = Pattern('drag_area.png')
        save_pattern = Pattern('save_bookmark_name.png')
        changed_toolbar_bookmark_pattern = Pattern('changed_toolbar_bookmark.png')
        bookmark_changed_location_pattern = Pattern('bookmark_changed_location.png')
        sidebar_bookmark_location_changed_pattern = Pattern('sidebar_bookmark_location_changed.png')

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

        bookmarks_sidebar('open')

        paste('amazon')

        sidebar_bookmark_assert = exists(amazon_bookmark_pattern, 10)
        assert_true(self, sidebar_bookmark_assert, 'Amazon bookmark is present in the sidebar.')

        right_click(amazon_bookmark_pattern)

        bookmark_options(Pattern('properties_option.png'))

        properties_window_assert = exists(save_pattern, 10)
        assert_true(self, properties_window_assert, 'Properties window is present on the page.')

        type(Key.TAB)

        paste('www.bing.com')

        click(save_pattern)

        try:
            wait(sidebar_bookmark_location_changed_pattern)
            logger.debug('Changed bookmark is present in Bookmark sidebar.')
            click(sidebar_bookmark_location_changed_pattern)
        except FindError:
            logger.error('Can\'t find the bookmark in Bookmark sidebar, aborting.')

        bookmark_location_assert = exists(Pattern('bing_favicon.png'))
        assert_true(self, bookmark_location_assert, 'The URL of the bookmark is successfully modified.')

        navigate('about:blank')

        access_bookmarking_tools(view_bookmarks_toolbar_pattern)

        try:
            wait(bookmarks_toolbar_most_visited_pattern, 10)
            logger.debug('Toolbar has been activated.')
        except FindError:
            logger.error('Toolbar can not be activated, aborting.')
            raise FindError

        drag_drop(bookmark_changed_location_pattern, drag_area_pattern, 0.5)

        try:
            wait(changed_toolbar_bookmark_pattern, 10)
            logger.debug('Bookmark is present in Bookmark Toolbar section.')
            right_click(changed_toolbar_bookmark_pattern)
        except FindError:
            logger.error('Can\'t find the bookmark in Bookmark Toolbar section, aborting.')
            raise FindError

        bookmark_options(Pattern('properties_option.png'))

        properties_window_assert = exists(save_pattern, 10)
        assert_true(self, properties_window_assert, 'Properties window is present on the page.')

        type(Key.TAB)

        paste('www.amazon.com')

        click(save_pattern)

        try:
            wait(changed_toolbar_bookmark_pattern, 10)
            logger.debug('Bookmark is present in Bookmark Toolbar section.')
            click(changed_toolbar_bookmark_pattern)
        except FindError:
            logger.error('Can\'t find the bookmark in Bookmark Toolbar section, aborting.')

        amazon_favicon_assert = exists(Pattern('amazon_favicon.png'), 15)
        assert_true(self, amazon_favicon_assert, 'The URL of the bookmark is successfully modified.')

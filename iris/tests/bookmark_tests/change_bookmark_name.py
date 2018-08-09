# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):
    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This is a test case that checks if the name of a bookmark can be changed'
        self.test_case_id = '4148'
        self.test_suite_id = '75'

    def run(self):
        amazon_home_pattern = Pattern('amazon.png')
        amazon_favicon_pattern = Pattern('amazon_favicon.png')
        bookmarks_toolbar_most_visited_pattern = SidebarBookmarks.BookmarksToolbar.MOST_VISITED
        done_pattern = Pattern('done_button.png')
        modified_bookmark_pattern = Pattern('modified_bookmark.png')
        modified_bookmark_2_pattern = Pattern('modified_bookmark_2.png')
        properties_pattern = Pattern('properties_option.png')
        save_pattern = Pattern('save_bookmark_name.png')
        toolbar_bookmark_pattern = Pattern('toolbar_bookmark.png')
        modified_toolbar_bookmark_pattern = Pattern('modified_toolbar_bookmark.png')
        bookmark_button_pattern = LocationBar.BOOKMARK_SELECTED_BUTTON
        view_bookmarks_toolbar_pattern = LibraryMenu.BookmarksOption.BookmarkingTools.VIEW_BOOKMARKS_TOOLBAR

        navigate('www.amazon.com')

        amazon_banner_assert = exists(amazon_home_pattern, 10)
        assert_true(self, amazon_banner_assert, 'Amazon page has been successfully loaded.')

        nav_bar_favicon_assert = exists(amazon_favicon_pattern, 15)
        assert_true(self, nav_bar_favicon_assert, 'Page is fully loaded and favicon displayed.')

        bookmark_page()

        try:
            wait(bookmark_button_pattern, 10)
            logger.debug('Star button is present on the page.')
        except FindError:
            logger.error('Can\'t find the Star button, aborting.')

        # Change the bookmark name fromm the "Edit This Bookmark panel"
        click(bookmark_button_pattern)
        paste('iris')

        button_assert = exists(done_pattern, 10)
        assert_true(self, button_assert, 'Changes can be saved.')

        click(done_pattern)
        bookmarks_sidebar('open')

        bookmark_sidebar_assert = exists(SidebarBookmarks.BOOKMARKS_HEADER, 10)
        assert_true(self, bookmark_sidebar_assert, 'Sidebar is opened.')

        paste('iris')

        bookmark_name_assert = exists(modified_bookmark_pattern, 10)
        assert_true(self, bookmark_name_assert, 'The name of the bookmark is successfully modified.')

        # Change the bookmark name from the Bookmarks Sidebar
        right_click(modified_bookmark_pattern)

        option_assert = exists(properties_pattern, 10)
        assert_true(self, option_assert, 'Properties option is present on the page.')

        click(properties_pattern)

        properties_window_assert = exists(save_pattern, 10)
        assert_true(self, properties_window_assert, 'Properties window is present on the page.')

        paste('iris_sidebar')
        click(save_pattern)

        bookmark_name_sidebar = exists(modified_bookmark_2_pattern, 10)
        assert_true(self, bookmark_name_sidebar, 'The name of the bookmark is successfully modified.')

        # Change the bookmark name from the Bookmarks Toolbar
        access_bookmarking_tools(view_bookmarks_toolbar_pattern)

        try:
            wait(bookmarks_toolbar_most_visited_pattern, 10)
            logger.debug('Toolbar has been activated.')
        except FindError:
            logger.error('Toolbar can not be activated, aborting.')

        drag_drop(modified_bookmark_2_pattern, Pattern('drag_area.png'), 0.5)
        navigate('about:blank')
        bookmarks_sidebar('close')

        toolbar_bookmark_assert = exists(toolbar_bookmark_pattern, 10)
        assert_true(self, toolbar_bookmark_assert, 'Name of the bookmark can be changed from the toolbar.')

        right_click(toolbar_bookmark_pattern)

        option_assert = exists(properties_pattern, 10)
        assert_true(self, option_assert, 'Properties option is present on the page.')

        click(properties_pattern)

        properties_window_assert = exists(save_pattern, 10)
        assert_true(self, properties_window_assert, 'Properties window is present on the page.')

        paste('iris_toolbar')
        click(save_pattern)

        bookmark_name_toolbar = exists(modified_toolbar_bookmark_pattern, 10)
        assert_true(self, bookmark_name_toolbar, 'The name of the bookmark is successfully modified.')

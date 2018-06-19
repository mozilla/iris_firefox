# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):
    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This is a test case that checks if the name of a bookmark can be changed'

    def run(self):
        amazon_home = 'amazon.png'
        amazon_favicon = 'amazon_favicon.png'
        view_bookmarks_toolbar = 'view_bookmarks_toolbar.png'
        active_toolbar = 'toolbar_is_active.png'
        star_button = 'bookmark_star.png'
        done = 'done_button.png'
        modified_bookmark = 'modified_bookmark.png'
        modified_bookmark_2 = 'modified_bookmark_2.png'
        properties = 'properties_option.png'
        save = 'save_bookmark_name.png'
        toolbar_bookmark = 'toolbar_bookmark.png'
        modified_toolbar_bookmark = 'modified_toolbar_bookmark.png'

        navigate('www.amazon.com')

        amazon_banner_assert = exists(amazon_home, 10)
        assert_true(self, amazon_banner_assert, 'Amazon page has been successfully loaded')

        nav_bar_favicon_assert = exists(amazon_favicon, 15)
        assert_true(self, nav_bar_favicon_assert, 'Page is fully loaded and favicon displayed')

        bookmark_page()

        try:
            wait(star_button, 10)
            logger.debug('Star button is present on the page')
        except FindError:
            logger.error('Can\'t find the Star button, aborting')

        # Change the bookmark name fromm the "Edit This Bookmark panel"

        click(star_button)

        paste('iris')

        button_assert = exists(done, 10)
        assert_true(self, button_assert, 'Changes can be saved')

        click(done)

        bookmarks_sidebar()

        bookmark_sidebar_assert = exists('bookmark_sidebar.png', 10)
        assert_true(self, bookmark_sidebar_assert, 'Sidebar is opened')

        paste('iris')

        bookmark_name_assert = exists(modified_bookmark, 10)
        assert_true(self, bookmark_name_assert, 'The name of the bookmark is successfully modified.')

        # Change the bookmark name from the Bookmarks Sidebar

        rightClick(modified_bookmark)

        option_assert = exists(properties, 10)
        assert_true(self, option_assert, 'Properties option is present on the page')

        click(properties)

        properties_window_assert = exists(save, 10)
        assert_true(self, properties_window_assert, 'Properties window is present on the page')

        paste('iris_sidebar')

        click(save)

        bookmark_name_sidebar = exists(modified_bookmark_2, 10)
        assert_true(self, bookmark_name_sidebar, 'The name of the bookmark is successfully modified.')

        # Change the bookmark name from the Bookmarks Toolbar

        access_bookmarking_tools(view_bookmarks_toolbar)

        try:
            wait(active_toolbar, 10)
            logger.debug('Toolbar has been activated')
        except FindError:
            logger.error('Toolbar can not be activated, aborting.')

        dragDrop(modified_bookmark_2, 'drag_area.png', 2)

        navigate('about:blank')

        bookmarks_sidebar()

        toolbar_bookmark_assert = exists(toolbar_bookmark, 10)
        assert_true(self, toolbar_bookmark_assert, 'Name of the bookmark can be changed from the toolbar')

        rightClick(toolbar_bookmark)

        option_assert = exists(properties, 10)
        assert_true(self, option_assert, 'Properties option is present on the page')

        click(properties)

        properties_window_assert = exists(save, 10)
        assert_true(self, properties_window_assert, 'Properties window is present on the page')

        paste('iris_toolbar')

        click(save)

        bookmark_name_toolbar = exists(modified_toolbar_bookmark, 10)
        assert_true(self, bookmark_name_toolbar, 'The name of the bookmark is successfully modified.')









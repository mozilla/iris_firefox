# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):
    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This is a test case that checks if a bookmark can be opened from Bookmarks Toolbar.'
        self.test_case_id='4093'
        self.test_suite_id='75'

    def run(self):
        amazon_home_pattern = Pattern('amazon.png')
        amazon_draggable_pattern = Pattern('amazon_draggable.png')
        drag_area_pattern = Pattern('drag_area.png')
        dragged_bookmark_pattern = Pattern('toolbar_dragged_bookmark.png')
        view_bookmarks_toolbar_pattern = LibraryMenu.BookmarksOption.BookmarkingTools.VIEW_BOOKMARKS_TOOLBAR

        navigate('www.amazon.com')

        amazon_banner_assert = exists(amazon_home_pattern, 10)
        assert_true(self, amazon_banner_assert, 'Amazon page has been successfully loaded.')

        nav_bar_favicon_assert = exists(Pattern('amazon_favicon.png'), 15)
        assert_true(self, nav_bar_favicon_assert, 'Page is fully loaded and favicon displayed.')

        bookmark_page()

        navigate('about:blank')

        access_bookmarking_tools(view_bookmarks_toolbar_pattern)

        bookmarks_sidebar('open')

        paste('amazon')

        drag_drop(amazon_draggable_pattern, drag_area_pattern, 0.5)

        bookmark_drag_assert = exists(dragged_bookmark_pattern, 10)
        assert_true(self, bookmark_drag_assert, 'Bookmark was dragged successfully.')

        bookmarks_sidebar('close')

        amazon_bookmark_sidebar_left_corner_assert = exists(dragged_bookmark_pattern, 10)
        assert_true(self, amazon_bookmark_sidebar_left_corner_assert,
                    'Amazon bookmark can be accessed from the Bookmarks Toolbar.')

        click(dragged_bookmark_pattern)

        nav_bar_favicon_assert = exists(Pattern('amazon_favicon.png'), 15)
        assert_true(self, nav_bar_favicon_assert, 'Page is fully loaded and favicon displayed.')

        amazon_bookmark_toolbar = exists(amazon_home_pattern, 10)
        assert_true(self, amazon_bookmark_toolbar,
                    'Amazon bookmark has been successfully accessed from the Bookmarks Toolbar.')

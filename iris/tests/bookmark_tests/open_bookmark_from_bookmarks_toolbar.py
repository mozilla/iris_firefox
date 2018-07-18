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
        amazon_home = 'amazon.png'
        amazon_draggable = 'amazon_draggable.png'
        drag_area = 'drag_area.png'
        dragged_bookmark = 'toolbar_dragged_bookmark.png'
        view_bookmarks_toolbar = 'view_bookmarks_toolbar.png'

        navigate('www.amazon.com')

        amazon_banner_assert = exists(amazon_home, 10)
        assert_true(self, amazon_banner_assert, 'Amazon page has been successfully loaded.')

        nav_bar_favicon_assert = exists('amazon_favicon.png', 15)
        assert_true(self, nav_bar_favicon_assert, 'Page is fully loaded and favicon displayed.')

        bookmark_page()

        navigate('about:blank')

        access_bookmarking_tools(view_bookmarks_toolbar)

        bookmarks_sidebar('open')

        paste('amazon')

        drag_drop(amazon_draggable, drag_area, 0.5)

        bookmark_drag_assert = exists(dragged_bookmark, 10)
        assert_true(self, bookmark_drag_assert, 'Bookmark was dragged successfully.')

        bookmarks_sidebar('close')

        amazon_bookmark_sidebar_left_corner_assert = exists(dragged_bookmark, 10)
        assert_true(self, amazon_bookmark_sidebar_left_corner_assert,
                    'Amazon bookmark can be accessed from the Bookmarks Toolbar.')

        click(dragged_bookmark)

        nav_bar_favicon_assert = exists('amazon_favicon.png', 15)
        assert_true(self, nav_bar_favicon_assert, 'Page is fully loaded and favicon displayed.')

        amazon_bookmark_toolbar = exists(amazon_home, 10)
        assert_true(self, amazon_bookmark_toolbar,
                    'Amazon bookmark has been successfully accessed from the Bookmarks Toolbar.')

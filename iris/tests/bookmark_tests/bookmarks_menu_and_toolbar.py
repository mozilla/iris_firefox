# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):
    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This is a bunch of test cases that checks if the bookmarks can be added, opened or deleted from ' \
                    'Bookmarks Menu and Bookmarks Toolbar'

    def run(self):
        library = 'library.png'
        bookmarks_menu = 'bookmarks_menu.png'
        bookmarking_tools = 'bookmarking_tools.png'
        view_bookmarks_toolbar = 'view_bookmarks_toolbar.png'
        view_bookmarks_sidebar = 'view_bookmarks_sidebar.png'
        toolbar_enabled = 'toolbar_is_active.png'
        sidebar_enabled = 'sidebar_is_active.png'
        amazon_home = 'amazon.png'
        amazon_draggable = 'amazon_draggable.png'
        menu_bookmark = 'bookmark_from_menu.png'
        drag_area = 'drag_area.png'
        dragged_bookmark = 'toolbar_dragged_bookmark.png'
        delete = 'delete_bookmark.png'

        navigate('www.amazon.com')

        amazon_banner_assert = exists(amazon_home, 10)
        assert_true(self, amazon_banner_assert, 'Amazon page has been successfully loaded')

        nav_bar_favicon_assert = exists('amazon_favicon.png', 15)
        assert_true(self, nav_bar_favicon_assert, 'Page is fully loaded and favicon displayed')

        bookmark_page()

        page_bookmarked_assert = exists('page_bookmarked.png', 10)
        assert_true(self, page_bookmarked_assert, 'Page was bookmarked')

        navigate('about:blank')
        time.sleep(2)

        # Test case 141 - The Bookmarks Toolbar can be enabled from the Bookmarks Menu
        screen = get_screen()
        right_upper_corner = Region(screen.getW() / 2, screen.getY(), screen.getW() / 2, screen.getH() / 2)

        right_upper_corner.click(library)

        bookmark_assert = right_upper_corner.exists(bookmarks_menu, 10)
        assert_true(self, bookmark_assert, 'Bookmarks menu can be accessed')

        right_upper_corner.click(bookmarks_menu)

        bookmark_tool_assert = right_upper_corner.exists(bookmarking_tools, 10)
        assert_true(self, bookmark_tool_assert, 'Bookmarking Tools menu can be accessed')

        right_upper_corner.click(bookmarking_tools)

        bookmark_toolbar_assert = right_upper_corner.exists(view_bookmarks_toolbar, 10)
        assert_true(self, bookmark_toolbar_assert, 'Bookmarks Toolbar can be activated')

        click(view_bookmarks_toolbar)

        expected_4 = exists(toolbar_enabled, 10)
        assert_true(self, expected_4, 'Bookmarks Toolbar has been activated')

        # Test case 145 - Bookmarks can be opened from the Bookmarks Toolbar

        bookmarks_sidebar()

        bookmark_sidebar_assert = exists('bookmark_sidebar.png', 10)
        assert_true(self, bookmark_sidebar_assert, 'Sidebar is opened')

        # search for bookmark named 'amazon'

        paste('amazon')

        time.sleep(1)

        dragDrop(amazon_draggable, drag_area)

        bookmark_drag_assert = exists('bookmark_dragged.png', 10)
        assert_true(self, bookmark_drag_assert, 'Bookmark was dragged successfully')

        bookmarks_sidebar()

        amazon_bookmark_sidebar_left_corner_assert = exists(dragged_bookmark, 10)
        assert_true(self, amazon_bookmark_sidebar_left_corner_assert,
                    'Amazon bookmark can be accessed from the Bookmarks Toolbar')

        click(dragged_bookmark)

        nav_bar_favicon_assert = exists('amazon_favicon.png', 15)
        assert_true(self, nav_bar_favicon_assert, 'Page is fully loaded and favicon displayed')

        amazon_bookmark_toolbar = exists(amazon_home, 10)
        assert_true(self, amazon_bookmark_toolbar,
                    'Amazon bookmark has been successfully accessed from the Bookmarks Toolbar')

        # Test case 143 - The Bookmarks Sidebar can be enabled from the Bookmarks Menu

        click(library)

        click(bookmarks_menu)

        click(bookmarking_tools)

        amazon_bookmark_sidebar_right_corner_assert = right_upper_corner.exists(view_bookmarks_sidebar, 10)
        assert_true(self, amazon_bookmark_sidebar_right_corner_assert, 'Bookmarks Sidebar can be activated')

        click(view_bookmarks_sidebar)

        side_bar_assert = exists(sidebar_enabled, 10)
        assert_true(self, side_bar_assert, 'Bookmarks Sidebar has been activated')

        # Test case 147 - Bookmarks can be opened from the Bookmarks Menu

        navigate('about:blank')

        bookmarks_sidebar()

        try:
            bookmark_sidebar_assert = waitVanish('bookmark_sidebar.png', 10)
            assert_true(self, bookmark_sidebar_assert, 'Bookmark sidebar menu disappeared')
        except FindError:
            logger.error('Bookmark sidebar menu still present')
            raise FindError

        click(library)

        click(bookmarks_menu)

        amazon_bookmark_menu_right_corner_assert = right_upper_corner.exists(menu_bookmark, 10)
        assert_true(self, amazon_bookmark_menu_right_corner_assert,
                    'Amazon bookmark can be accessed from the Bookmarks Menu')

        right_upper_corner.click(menu_bookmark)

        amazon_banner_assert = exists(amazon_home, 10)
        assert_true(self, amazon_banner_assert,
                    'Amazon bookmark has been successfully accessed from the Bookmarks Menu')

        navigate('about:blank')

        rightClick(dragged_bookmark)

        click(delete)

        try:
            delete_bookmark_toolbar_assert = waitVanish(dragged_bookmark, 10)
            assert_true(self, delete_bookmark_toolbar_assert,
                        'Amazon bookmark has been successfully deleted from the Bookmarks Toolbar.')
        except FindError:
            logger.error('Amazon bookmark can not be deleted from the Bookmarks Toolbar.')
            raise FindError

        # Test case 152 - Bookmarks can be removed from the Bookmarks Menu

        click(library)

        click(bookmarks_menu)

        rightClick(menu_bookmark)

        click(delete)

        try:
            delete_bookmark_menu_assert = right_upper_corner.waitVanish(menu_bookmark, 10)
            assert_true(self, delete_bookmark_menu_assert,
                        'Amazon bookmark has been successfully deleted from the Bookmarks Menu.')
        except FindError:
            logger.error('Amazon bookmark can not be deleted from the Bookmarks Menu.')
            raise FindError

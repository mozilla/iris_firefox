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
        url = 'amazon.com'
        url2 = 'about:home'
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
        amazon_in_sidebar = 'amazon'

        navigate(url)

        expected_page = exists(amazon_home, 10)
        assert_true(self, expected_page, 'Amazon page has been successfully loaded')

        bookmark_page()

        time.sleep(2)

        navigate(url2)

        time.sleep(2)

        # Test case 141 - The Bookmarks Toolbar can be enabled from the Bookmarks Menu

        coord = find(library)
        right_upper_corner = Region(coord.x - 500, 0, 500, 500)

        click(library)

        expected_1 = right_upper_corner.exists(bookmarks_menu, 10)
        assert_true(self, expected_1, 'Bookmarks menu can be accessed')

        click(bookmarks_menu)

        expected_2 = right_upper_corner.exists(bookmarking_tools, 10)
        assert_true(self, expected_2, 'Bookmarking Tools menu can be accessed')

        click(bookmarking_tools)

        expected_3 = right_upper_corner.exists(view_bookmarks_toolbar, 10)
        assert_true(self, expected_3, 'Bookmarks Toolbar can be activated')

        click(view_bookmarks_toolbar)

        expected_4 = exists(toolbar_enabled, 10)
        assert_true(self, expected_4, 'Bookmarks Toolbar has been activated')

        # Test case 145 - Bookmarks can be opened from the Bookmarks Toolbar

        bookmarks_sidebar()

        time.sleep(1)

        paste(amazon_in_sidebar)

        time.sleep(1)

        dragDrop(amazon_draggable, drag_area)

        time.sleep(1)

        bookmarks_sidebar()

        expected_5 = exists(dragged_bookmark, 10)
        assert_true(self, expected_5, 'Amazon bookmark can be accessed from the Bookmarks Toolbar')

        click(dragged_bookmark)

        expected_6 = exists(amazon_home, 10)
        assert_true(self, expected_6, 'Amazon bookmark has been successfully accessed from the Bookmarks Toolbar')

        # Test case 143 - The Bookmarks Sidebar can be enabled from the Bookmarks Menu

        click(library)

        click(bookmarks_menu)

        click(bookmarking_tools)

        expected_7 = right_upper_corner.exists(view_bookmarks_sidebar, 10)
        assert_true(self, expected_7, 'Bookmarks Sidebar can be activated')

        click(view_bookmarks_sidebar)

        expected_8 = exists(sidebar_enabled, 10)
        assert_true(self, expected_8, 'Bookmarks Sidebar has been activated')

        # Test case 147 - Bookmarks can be opened from the Bookmarks Menu

        navigate(url2)

        bookmarks_sidebar()

        time.sleep(1)

        click(library)

        click(bookmarks_menu)

        expected_9 = right_upper_corner.exists(menu_bookmark, 10)
        assert_true(self, expected_9, 'Amazon bookmark can be accessed from the Bookmarks Menu')

        right_upper_corner.click(menu_bookmark)

        expected_10 = exists(amazon_home, 10)
        assert_true(self, expected_10, 'Amazon bookmark has been successfully accessed from the Bookmarks Menu')

        navigate(url2)

        rightClick(dragged_bookmark)

        click(delete)

        try:
            expected_11 = waitVanish(dragged_bookmark, 10)
            assert_true(self, expected_11, 'Amazon bookmark has been successfully deleted from the Bookmarks Toolbar.')
        except Exception as error:
            logger.error('Amazon bookmark can not be deleted from the Bookmarks Toolbar.')
            raise error

        # Test case 152 - Bookmarks can be removed from the Bookmarks Menu

        click(library)

        click(bookmarks_menu)

        rightClick(menu_bookmark)

        click(delete)

        try:
            expected_12 = right_upper_corner.waitVanish(menu_bookmark, 10)
            assert_true(self, expected_12, 'Amazon bookmark has been successfully deleted from the Bookmarks Menu.')
        except Exception as error:
            logger.error('Amazon bookmark can not be deleted from the Bookmarks Menu.')
            raise error

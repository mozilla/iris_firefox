# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This is a bunch of test cases that checks if the bookmarks can be bookmarked via URL drag & drop'

    def run(self):

        url = 'about:home'
        url2 = 'amazon.com'
        url3 = 'bing.com'
        library = 'library.png'
        bookmarks_menu = 'bookmarks_menu.png'
        bookmarking_tools = 'bookmarking_tools.png'
        view_bookmarks_toolbar = 'view_bookmarks_toolbar.png'
        toolbar_enabled = 'toolbar_is_active.png'
        sidebar_enabled = 'sidebar_is_active.png'
        draggable_url = 'draggable_url.png'
        draggable_url_2 = 'draggable_url_bing.png'
        toolbar_dragged_bookmark = 'toolbar_dragged_bookmark.png'
        sidebar_bookmarks = 'library_bookmarks.png'
        drag_area = 'drag_area.png'
        drag_area_2 = 'drag_area_bing.png'
        amazon_home = 'amazon.png'
        bing_home = 'bing_home.png'
        bing_bookmark = 'bing_bookmark.png'
        bookmarked_star = 'blue_star.png'

        navigate(url)

        coord = find(library)
        right_upper_corner = Region(coord.x - 500, 0, 500, 500)

        # Test case 142 - Websites can be bookmarked via URL drag & drop onto the Bookmarks Toolbar

        click(library)

        click(bookmarks_menu)

        click(bookmarking_tools)

        expected_1 = right_upper_corner.exists(view_bookmarks_toolbar, 10)
        assert_true(self, expected_1, 'Bookmarks Toolbar can be activated')

        click(view_bookmarks_toolbar)

        expected_2 = exists(toolbar_enabled, 10)
        assert_true(self, expected_2, 'Bookmarks Toolbar has been activated')

        navigate(url2)

        expected_3 = exists(amazon_home, 10)
        assert_true(self, expected_3, 'Amazon has been successfully accessed')

        select_location_bar()

        time.sleep(1)

        type(Key.ESC)

        time.sleep(1)

        dragDrop(draggable_url, drag_area, 2)

        expected_4 = exists(bookmarked_star, 10)
        assert_true(self, expected_4, 'Star-shaped button has changed its color to blue')

        navigate(url)

        expected_5 = exists(toolbar_dragged_bookmark, 10)
        assert_true(self, expected_5, 'Amazon page has been successfully bookmarked via URL onto the Bookmarks Toolbar')

        # Test case 144 - Websites can be bookmarked via URL drag & drop onto the Bookmarks Sidebar

        navigate(url3)

        expected_5 = exists(bing_home, 10)
        assert_true(self, expected_5, 'Bing has been successfully accessed')

        bookmarks_sidebar('open')

        expected_7 = exists(sidebar_enabled, 10)
        assert_true(self, expected_7, 'Bookmarks Sidebar has been activated')

        click(sidebar_bookmarks)

        select_location_bar()

        time.sleep(1)

        dragDrop(draggable_url_2, drag_area_2, 2)

        expected_8 = exists(bookmarked_star, 10)
        assert_true(self, expected_8, 'Star-shaped button has changed its color to blue')

        expected_9 = exists(bing_bookmark, 10)
        assert_true(self, expected_9, 'Bing page has been successfully bookmarked via URL onto the Bookmarks Sidebar')

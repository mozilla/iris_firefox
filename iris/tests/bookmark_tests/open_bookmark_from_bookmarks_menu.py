# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):
    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This is a test case that checks if the bookmarks can be opened from Bookmarks menu.'

    def run(self):
        amazon_home = 'amazon.png'
        bookmarks_menu = 'bookmarks_menu.png'
        menu_bookmark = 'bookmark_from_menu.png'

        right_upper_corner = Region(SCREEN_WIDTH / 2, 0, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

        navigate('www.amazon.com')

        amazon_banner_assert = exists(amazon_home, 10)
        assert_true(self, amazon_banner_assert, 'Amazon page has been successfully loaded.')

        nav_bar_favicon_assert = exists('amazon_favicon.png', 15)
        assert_true(self, nav_bar_favicon_assert, 'Page is fully loaded and favicon displayed.')

        bookmark_page()

        navigate('about:blank')

        open_library_menu(bookmarks_menu)

        amazon_bookmark_menu_right_corner_assert = right_upper_corner.exists(menu_bookmark, 10)
        assert_true(self, amazon_bookmark_menu_right_corner_assert,
                    'Amazon bookmark can be accessed from the Bookmarks Menu.')

        right_upper_corner.click(menu_bookmark)

        amazon_banner_assert = exists(amazon_home, 10)
        assert_true(self, amazon_banner_assert,
                    'Amazon bookmark has been successfully accessed from the Bookmarks Menu.')

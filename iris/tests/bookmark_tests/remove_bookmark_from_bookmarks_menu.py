# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):
    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This is a test case that checks if the bookmarks can be removed from Bookmarks menu.'
        self.test_case_id = '4101'
        self.test_suite_id = '75'

    def run(self):
        amazon_home = 'amazon.png'
        bookmarks_menu = 'bookmarks_menu.png'
        menu_bookmark = 'bookmark_from_menu.png'
        delete = 'delete_bookmark.png'

        right_upper_corner = Region(SCREEN_WIDTH / 2, 0, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

        navigate('www.amazon.com')

        amazon_banner_assert = exists(amazon_home, 10)
        assert_true(self, amazon_banner_assert, 'Amazon page has been successfully loaded.')

        nav_bar_favicon_assert = exists('amazon_favicon.png', 15)
        assert_true(self, nav_bar_favicon_assert, 'Page is fully loaded and favicon displayed.')

        bookmark_page()

        navigate('about:blank')

        open_library_menu(bookmarks_menu)

        try:
            right_upper_corner.wait(menu_bookmark, 10)
            logger.debug('Amazon bookmark is present in the Bookmarks Menu section.')
            right_click(menu_bookmark)
        except FindError:
            raise FindError('Amazon bookmark is not present in the Bookmarks Menu, aborting.')

        bookmark_options(delete)

        try:
            delete_bookmark_menu_assert = right_upper_corner.wait_vanish(menu_bookmark, 10)
            assert_true(self, delete_bookmark_menu_assert,
                        'Amazon bookmark has been successfully deleted from the Bookmarks Menu.')
        except FindError:
            raise FindError('Amazon bookmark can not be deleted from the Bookmarks Menu.')

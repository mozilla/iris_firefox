# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'Bookmarks can be opened from the Bookmarks Library.'

    def run(self):
        url = 'www.amazon.com'
        amazon_home = 'amazon.png'
        library_bookmarks = 'library_bookmarks.png'
        amazon_library = 'amazon_library.png'

        navigate(url)

        amazon_banner_assert = exists(amazon_home, 10)
        assert_true(self, amazon_banner_assert, 'Amazon page has been successfully loaded.')

        nav_bar_favicon_assert = exists('amazon_favicon.png', 15)
        assert_true(self, nav_bar_favicon_assert, 'Page is fully loaded and favicon displayed.')

        bookmark_page()

        navigate('about:blank')

        open_library()

        bookmarks_menu_library_assert = exists(library_bookmarks, 10)
        assert_true(self, bookmarks_menu_library_assert, 'Bookmarks menu has been found.')

        click(library_bookmarks)

        type(Key.ENTER)
        type(Key.DOWN)

        library_bookmark_assert = exists(amazon_library, 10)
        assert_true(self, library_bookmark_assert, 'Amazon bookmark can be accessed in Library section.')

        click(amazon_library)
        type(Key.ENTER)

        amazon_banner_assert = exists(amazon_home, 10)
        assert_true(self, amazon_banner_assert, 'Amazon bookmark has been successfully accessed from Library section.')

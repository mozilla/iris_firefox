# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'Bookmarks can be removed from the Bookmarks Library.'
        self.test_case_id = '4100'
        self.test_suite_id = '75'

    def run(self):
        url = 'www.amazon.com'
        amazon_home_pattern = Pattern('amazon.png')
        library_bookmarks_pattern = Pattern('library_bookmarks.png')
        amazon_library_pattern = Pattern('amazon_library.png')
        delete_pattern = Pattern('delete_bookmark.png')

        navigate(url)

        amazon_banner_assert = exists(amazon_home_pattern, 10)
        assert_true(self, amazon_banner_assert, 'Amazon page has been successfully loaded.')

        nav_bar_favicon_assert = exists(Pattern('amazon_favicon.png'), 15)
        assert_true(self, nav_bar_favicon_assert, 'Page is fully loaded and favicon displayed.')

        bookmark_page()

        navigate('about:blank')

        open_library()

        bookmarks_menu_library_assert = exists(library_bookmarks_pattern, 10)
        assert_true(self, bookmarks_menu_library_assert, 'Bookmarks menu has been found.')

        click(library_bookmarks_pattern)

        type(Key.ENTER)
        type(Key.DOWN)

        try:
            wait(amazon_library_pattern, 10)
            logger.debug('Amazon bookmark can be accessed in Library section.')
            right_click(amazon_library_pattern)
        except FindError:
            raise FindError('Amazon bookmark is not present in Library section, aborting.')

        bookmark_options(delete_pattern)

        try:
            deleted_bookmark_assert = wait_vanish(amazon_library_pattern, 10)
            assert_true(self, deleted_bookmark_assert, 'Amazon bookmark has been removed from the Library.')
        except FindError:
            raise FindError('Amazon bookmark can NOT be removed from the Library, aborting.')

        click_auxiliary_window_control('close')

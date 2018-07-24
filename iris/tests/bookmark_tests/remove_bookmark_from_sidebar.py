# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'Bookmarks can be removed from the Bookmarks Sidebar.'
        self.test_case_id = '4099'
        self.test_suite_id = '75'

    def run(self):
        url = 'www.amazon.com'
        amazon_home = 'amazon.png'
        amazon_bookmark = 'amazon_bookmark.png'
        delete = 'delete_bookmark.png'

        navigate(url)

        amazon_banner_assert = exists(amazon_home, 10)
        assert_true(self, amazon_banner_assert, 'Amazon page has been successfully loaded.')

        nav_bar_favicon_assert = exists('amazon_favicon.png', 15)
        assert_true(self, nav_bar_favicon_assert, 'Page is fully loaded and favicon displayed.')

        bookmark_page()

        navigate('about:blank')

        bookmarks_sidebar('open')

        paste('amazon')

        try:
            wait(amazon_bookmark, 10)
            logger.debug('Amazon bookmark is present in the Bookmark sidebar.')
            right_click(amazon_bookmark)
        except FindError:
            raise FindError('Amazon bookmark is NOT present in the Bookmark sidebar, aborting.')

        bookmark_options(delete)

        try:
            deleted_bookmark_assert = wait_vanish(amazon_bookmark, 10)
            assert_true(self, deleted_bookmark_assert, 'Amazon bookmark is successfully deleted from the '
                                                       'Bookmark sidebar.')
        except FindError:
            raise FindError('Amazon bookmark can NOT be deleted from the Bookmark sidebar, aborting.')

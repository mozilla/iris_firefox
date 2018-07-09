# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'Bookmarks can be opened from the Bookmarks Sidebar.'

    def run(self):
        url = 'www.amazon.com'
        amazon_home = 'amazon.png'
        amazon_bookmark = 'amazon_bookmark.png'

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
            click(amazon_bookmark)
        except FindError:
            raise APIHelperError('Amazon bookmark is NOT present in the Bookmark sidebar, aborting.')

        amazon_banner_assert = exists(amazon_home, 10)
        assert_true(self, amazon_banner_assert, 'Amazon page has been successfully loaded.')

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'Websites can be bookmarked via star-shaped button.'

    def run(self):
        url = 'www.amazon.com'
        amazon_home = 'amazon.png'
        star_button = 'bookmark_star.png'

        navigate(url)

        amazon_banner_assert = exists(amazon_home, 10)
        assert_true(self, amazon_banner_assert, 'Amazon page has been successfully loaded.')

        nav_bar_favicon_assert = exists('amazon_favicon.png', 15)
        assert_true(self, nav_bar_favicon_assert, 'Page is fully loaded and favicon displayed.')

        try:
            wait(star_button, 10)
            logger.debug('Bookmark star is present on the page.')
            click(star_button)
        except FindError:
            raise FindError('Bookmark star is not present on the page, aborting.')

        page_bookmarked_assert = exists('page_bookmarked.png', 10)
        assert_true(self, page_bookmarked_assert, 'The page was successfully bookmarked via star button.')

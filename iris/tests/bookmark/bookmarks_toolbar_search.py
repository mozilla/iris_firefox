# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):
    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'This is a test case that checks if the search bookmark from Bookmarks Toolbar function works.'
        self.test_case_id = '165483'
        self.test_suite_id = '2525'
        self.locales = ['en-US']

    def setup(self):
        """Test case setup

        Override the setup method to use a pre-canned bookmarks profile.
        """
        BaseTest.setup(self)
        self.profile = Profile.TEN_BOOKMARKS
        return

    def run(self):

        search_bookmarks = Pattern('search_bookmarks.png')
        search_star = Pattern('search_star.png')
        searched_bookmark = Pattern('moz_searched_bookmark.png')

        navigate('about:blank')

        open_library_menu('Bookmarks')

        try:
            wait(search_bookmarks, 10)
            logger.debug('Search Bookmarks option is present on the page.')
            click(search_bookmarks)
        except FindError:
            raise FindError('Can\'t find Search Bookmarks option, aborting.')

        star_search_assert = exists(search_star, 10)
        assert_true(self, star_search_assert, 'Star search is present on the page.')

        searched_bookmark_assert = exists(searched_bookmark, 10)
        assert_true(self, searched_bookmark_assert, 'Searched bookmark is present in the Search List.')

        click(searched_bookmark)

        mozilla_page_assert = exists(LocalWeb.MOZILLA_LOGO, 10)
        assert_true(self, mozilla_page_assert, 'Mozilla page loaded successfully.')

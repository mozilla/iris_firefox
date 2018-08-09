# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):
    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This is a test case that checks if the search bookmark from Bookmarks Toolbar function works.'
        self.test_case_id = '116972'
        self.test_suite_id = '75'

    def run(self):
        amazon_favicon_pattern = Pattern('amazon_favicon.png')
        search_bookmarks_pattern = LibraryMenu.BookmarksOption.SEARCH_BOOKMARKS
        search_star_pattern = Pattern('search_star.png')
        searched_bookmark_pattern = Pattern('searched_bookmark.png')
        amazon_home_pattern = Pattern('amazon.png')

        navigate('www.amazon.com')

        nav_bar_favicon_assert = exists(amazon_favicon_pattern, 15)
        assert_true(self, nav_bar_favicon_assert, 'Page is fully loaded and favicon displayed.')

        bookmark_page()

        page_bookmarked_assert = exists(Pattern('page_bookmarked.png'), 10)
        assert_true(self, page_bookmarked_assert, 'Page was bookmarked')

        navigate('about:blank')

        time.sleep(Settings.UI_DELAY_LONG)

        open_library_menu(LibraryMenu.BOOKMARKS_OPTION)

        try:
            wait(search_bookmarks_pattern, 10)
            logger.debug('Search Bookmarks option is present on the page')
            click(search_bookmarks_pattern)
        except FindError:
            logger.error('Can\'t find Search Bookmarks option, aborting.')
            raise FindError

        star_search_assert = exists(search_star_pattern, 10)
        assert_true(self, star_search_assert, 'Star search is present on the page')

        searched_bookmark_assert = exists(searched_bookmark_pattern, 10)
        assert_true(self, searched_bookmark_assert, 'Searched bookmark is present in the Search List')

        click(searched_bookmark_pattern)

        amazon_banner_assert = exists(amazon_home_pattern, 10)
        assert_true(self, amazon_banner_assert, 'Amazon page has been successfully loaded')






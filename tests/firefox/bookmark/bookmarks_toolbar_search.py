# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='This is a test case that checks if the search bookmark from Bookmarks Toolbar function works.',
        locale=['en-US'],
        test_case_id='165483',
        test_suite_id='2525',
        profile=Profiles.TEN_BOOKMARKS
    )
    def run(self, firefox):
        search_bookmarks = Pattern('search_bookmarks.png')
        search_star = Pattern('search_star.png')
        searched_bookmark = Pattern('moz_searched_bookmark.png')

        navigate('about:blank')

        open_library_menu('Bookmarks')

        try:
            wait(search_bookmarks, FirefoxSettings.FIREFOX_TIMEOUT)
            logger.debug('Search Bookmarks option is present on the page.')
            click(search_bookmarks)
        except FindError:
            raise FindError('Can\'t find Search Bookmarks option, aborting.')

        star_search_assert = exists(search_star, FirefoxSettings.FIREFOX_TIMEOUT)
        assert star_search_assert is True, 'Star search is present on the page.'

        searched_bookmark_assert = exists(searched_bookmark, FirefoxSettings.FIREFOX_TIMEOUT)
        assert searched_bookmark_assert is True, 'Searched bookmark is present in the Search List.'

        click(searched_bookmark)

        mozilla_page_assert = exists(LocalWeb.MOZILLA_LOGO, FirefoxSettings.FIREFOX_TIMEOUT)
        assert mozilla_page_assert  is True, 'Mozilla page loaded successfully.'

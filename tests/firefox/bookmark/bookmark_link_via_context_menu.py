# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Links can be bookmarked via context menu.',
        locale=['en-US'],
        test_case_id='4143',
        test_suite_id='2525'
    )
    def run(self, firefox):
        moz_article = 'https://developer.mozilla.org/en-US/docs/Learn'
        moz_page = Pattern('moz_article_page.png')
        bookmark_link = Pattern('bookmark_link.png')
        bookmark_this_link = Pattern('bookmark_this_link.png')
        save_bookmark_link = Pattern('save_bookmark_name.png')
        bookmarked_link = Pattern('bookmarked_link.png')

        navigate(moz_article)

        moz_article_assert = exists(moz_page, FirefoxSettings.FIREFOX_TIMEOUT)
        assert moz_article_assert is True, 'The Moz article page has been successfully loaded.'

        try:
            wait(bookmark_link, FirefoxSettings.FIREFOX_TIMEOUT)
            logger.debug('Link is present on the page.')
            right_click(bookmark_link)
        except FindError:
            raise FindError('Link is not present on the page, aborting.')

        try:
            wait(bookmark_this_link, FirefoxSettings.FIREFOX_TIMEOUT)
            logger.debug('Bookmark this link option is present on the page.')
            click(bookmark_this_link)
        except FindError:
            raise FindError('Bookmark this link option is not present on the page, aborting.')

        try:
            wait(save_bookmark_link, FirefoxSettings.FIREFOX_TIMEOUT)
            logger.debug('Bookmark can be saved.')
            click(save_bookmark_link)
        except FindError:
            raise FindError('Bookmark can not be saved, aborting.')

        navigate('about:blank')

        bookmarks_sidebar('open')

        paste('CSS')

        bookmarked_link_assert = exists(bookmarked_link, FirefoxSettings.FIREFOX_TIMEOUT)
        assert bookmarked_link_assert is True, 'The link has been successfully bookmarked.'

        click(bookmarked_link)

        page_load_assert = exists(moz_page, FirefoxSettings.FIREFOX_TIMEOUT)
        assert page_load_assert is True, 'The page has been successfully loaded.'

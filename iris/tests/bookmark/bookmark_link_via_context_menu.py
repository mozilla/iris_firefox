# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Links can be bookmarked via context menu.'
        self.test_case_id = '4143'
        self.test_suite_id = '2525'
        self.locales = ['en-US']

    def run(self):

        moz_article = 'https://developer.mozilla.org/en-US/docs/Learn'
        moz_page = Pattern('moz_article_page.png')
        bookmark_link = Pattern('bookmark_link.png')
        bookmark_this_link = Pattern('bookmark_this_link.png')
        save_bookmark_link = Pattern('save_bookmark_name.png')
        bookmarked_link = Pattern('bookmarked_link.png')

        navigate(moz_article)

        moz_article_assert = exists(moz_page, 10)
        assert_true(self, moz_article_assert, 'The Moz article page has been successfully loaded.')

        try:
            wait(bookmark_link, 10)
            logger.debug('Link is present on the page.')
            right_click(bookmark_link)
        except FindError:
            raise FindError('Link is not present on the page, aborting.')

        try:
            wait(bookmark_this_link, 10)
            logger.debug('Bookmark this link option is present on the page.')
            click(bookmark_this_link)
        except FindError:
            raise FindError('Bookmark this link option is not present on the page, aborting.')

        try:
            wait(save_bookmark_link, 10)
            logger.debug('Bookmark can be saved.')
            click(save_bookmark_link)
        except FindError:
            raise FindError('Bookmark can not be saved, aborting.')

        navigate('about:blank')

        bookmarks_sidebar('open')

        paste('CSS')

        bookmarked_link_assert = exists(bookmarked_link, 10)
        assert_true(self, bookmarked_link_assert, 'The link has been successfully bookmarked.')

        click(bookmarked_link)

        page_load_assert = exists(moz_page, 10)
        assert_true(self, page_load_assert, 'The page has been successfully loaded.')

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):
    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'Web compatibility test for wikipedia.org'

    def run(self):
        url = 'www.wikipedia.org'
        page_title = 'wikipedia.png'
        iris_text = 'wikipedia_iris.png'
        keyword = 'iris'
        navigate(url)

        try:
            wait(page_title, 10)
            logger.debug('Page is successfully loaded')
        except (FindError, ValueError):
            logger.error('Can\'t find Wikipedia image in page, aborting test.')
            return

        logger.debug('Search in Wikipedia with default English language')
        paste(keyword)
        type(Key.ENTER)

        try:
            wait(iris_text, 10)
            logger.debug('Search is successfully loaded')
        except (FindError, ValueError):
            logger.error('Can\'t find search image in page')

        logger.debug('Scroll down')
        for x in range(10):
            scroll_down()

        scroll_down_assert = exists(iris_text, 1)
        assert_false(self, scroll_down_assert, 'Iris text was found and scroll down was performed')

        logger.debug('Scroll up')
        for x in range(10):
            scroll_up()

        scroll_up_assert = exists(iris_text, 1)
        assert_true(self, scroll_up_assert, 'Scroll was successfully performed')

        logger.debug('Page was scrolled back up')
        navigate_back()
        logger.debug('Navigate back')

        try:
            wait(page_title, 10)
            logger.debug('Page is successfully loaded')
        except (FindError, ValueError):
            logger.error('Can\'t find Wikipedia image in page, aborting test.')
            return
        else:
            logger.debug('Change language to Spanish')
            paste(keyword)
            if Settings.getOS() == Platform.MAC:
                type(Key.TAB)
                time.sleep(1)
                type(Key.DOWN)
                time.sleep(1)
                type(Key.DOWN)
                type(Key.ENTER)
                time.sleep(1)
                type(Key.TAB)
                type(Key.ENTER)
            else:
                type(Key.TAB)
                type(Key.DOWN)
                type(Key.TAB)
                type(Key.ENTER)

            spanish_text_assert = exists('wikipedia_spanish_page.png', 10)
            assert_true(self, spanish_text_assert, 'Wikipedia Spanish page is loaded')

            iris_spanish_search_bar_assert = exists('wikipedia_spanish_search.png', 10)
            assert_true(self, iris_spanish_search_bar_assert, 'Spanish search bar is displayed in page')

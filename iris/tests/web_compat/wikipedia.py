# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):
    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = "Web compability test for wikipedia.org"
        #self.exclude = Platform.ALL

    def run(self):
        url = "www.wikipedia.org"
        page_title = "wikipedia.png"
        iris_text = "wikipedia_iris.png"
        keyword = "iris"
        navigate(url)

        try:
            wait(page_title, 10)
            logger.debug("Page is succesfully loaded")
        except:
            # If we can't find the Wikipedia logo, there is no sense going further
            logger.error("Can't find Wikipedia image in page, aborting test.")
            print "FAIL"
            return

        # Access Wikipedia on English version
        logger.debug("Search in Wikipedia with default English language")
        type(keyword)
        type(Key.ENTER)

        # Test if we get a search result
        try:
            wait(iris_text, 10)
            logger.debug("Search is succesfully loaded")
        except:
            logger.error("Can't find search image in page")
        # Scroll down
        logger.debug("Scroll down")
        for x in range(10):
            scroll_down()
            time.sleep(.25)
        scroll_down_assert = exists(iris_text, 1)
        assert_false(self, scroll_down_assert, 'Iris text was found and scroll down was performed')
        logger.debug("Scroll up")
        for x in range(10):
            scroll_up()
            time.sleep(.25)
        scroll_up_assert = exists(iris_text, 1)
        assert_true(self, scroll_up_assert, 'Scroll was succesfully performed')
        logger.debug("Page was scrolled back up")
        navigate_back()
        logger.debug("Navigate back")
        try:
            wait(page_title, 10)
            logger.debug("Page is succesfully loaded")
        except:
            logger.error("Can't find Wikipedia image in page, aborting test.")
            return
        else:
            logger.debug("Change language to Spanish")
            type(keyword)
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

            # We will replace PASS/FAIL with proper assert functions soon
            iris_text_assert = exists(iris_text, 10)
            assert_true(self, iris_text_assert, 'Text found in page')
            
            # Using text recognition, we can verify if the results are in Spanish
            results_spanish = ['membrana', 'coloreada', 'abertura', 'ojo']
            page_text = get_firefox_region().text()

            # Text recognition sometimes mistranslates words, so let's check that
            # at least one Spanish word appears in the page
            found = False
            for word in results_spanish:
                if exists(word, 5, page_text):
                    found = True
                    break
            assert_true(self, found, 'Found Spanish search results')

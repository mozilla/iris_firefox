# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from test_case import *



class test(base_test):

    def __init__(self, app):
        base_test.__init__(self, app)
        base_test.set_image_path(self, os.path.split(__file__)[0])
        self.assets = os.path.join(os.path.split(__file__)[0], "assets")
        self.meta = "Search Wikipedia and change language"


    def run(self):
        url = "www.wikipedia.org"
        page_title = "wikipedia.png"
        iris_text = "wikipedia_iris.png"
        keyword = "iris"
        navigate(url)

        try:
            wait (page_title, 10)
            logger.debug("Page is succesfully loaded")
        except:
            # If we can't find the Wikipedia logo, there is no sense going further
            logger.error ("Can't find Wikipedia image in page, aborting test.")
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
            print "PASS"
        except:
            # If we can't find the search text, we will fail the test
            # but we can keep running the rest of the tests
            logger.error ("Can't find search image in page")
            print "FAIL"

        #Scroll down
        logger.debug("Scroll down")
        for x in range(10):
            scroll_down()
            time.sleep(.25)
        if exists(iris_text,1):
            logger.debug("Scroll down was not performed")
        else:
            logger.debug("Scroll up")
            for x in range(10):
                scroll_up()
                time.sleep(.25)
        if exists(iris_text,1):
            logger.debug("Page was scrolled back up")
            navigate_back()
            logger.debug("Navigate back")

        try:
            wait (page_title, 10)
            logger.debug("Page is succesfully loaded")
        except:
            # If we can't find the Wikipedia logo, there is no sense going further
            logger.error ("Can't find Wikipedia image in page, aborting test.")
            print "FAIL"
            return
        else:
            logger.debug("Change language to Spanish")
            type(keyword)
            if get_os() == "osx":
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
            if exists(iris_text, 10):
                # Using text recognition, we can verify if the results are in Spanish
                results_spanish = ['membrana', 'coloreada', 'abertura', 'ojo']
                page_text = get_firefox_region().text()

                # Text recognition sometimes mistranslates words, so let's check that
                # at least one Spanish word appears in the page
                found = False
                for word in results_spanish:
                    if word in page_text:
                        found = True
                        break
                if found:
                    logger.debug("Found Spanish search results")
                    print "PASS"
                else:
                    logger.debug("Can not find Spanish search results")
                    print "FAIL"
            else:
                logger.debug("Can't find search image in page")
                print "FAIL"

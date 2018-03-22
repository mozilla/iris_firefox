# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from test_case import *






class test(base_test):

    def __init__(self, app):
        base_test.__init__(self, app)
        base_test.set_image_path(self, os.path.split(__file__)[0])
        self.assets = os.path.join(os.path.split(__file__)[0], "assets")
        self.meta = "Access wikipedia and select english language"


    def run(self):
        url="www.wikipedia.org"
        page_title="wikipedia.png"
        keyword='iris'

        navigate(url)

        try:
            wait (page_title, 10)
        except:
            logger.error ("Can't find Wikipedia image in page, aborting test.")
        if exists(page_title,3):
            logger.debug("Page is succesfully loaded!!")
            #access wikipedia on english version

            logger.debug("Search in wikipedia with default language")
            type(keyword)
            type(Key.ENTER)
                #  wait("iris.png",5)
            time.sleep(3)
                #Scrool down
            logger.debug("Scroll down")
            for x in range(10):
                scroll_down()
            logger.debug("Scroll up")
                #Scrool up
            time.sleep(3)
            for x in range(10):
                scroll_up()
            if exists("iris.png",5):
                logger.debug("Navigate back")
                navigate_back()
                wait(page_title,5)
                logger.debug("Change language")
                type(keyword)
                if get_os() == "osx":
                    print "sistem is osx"
                    type(Key.TAB)
                    time.sleep(2)
                    type(Key.DOWN)
                    time.sleep(2)
                    type(Key.DOWN)
                    time.sleep(2)
                    type(Key.ENTER)
                    type(Key.TAB)
                    type(Key.ENTER)
                else:
                    type(Key.TAB)
                    type(Key.DOWN)
                    type(Key.TAB)
                    type(Key.ENTER)
                if exists("iris.png",5):
                    logger.debug( "Test passed")
                else:
                    logger.debug ("Test failed")
            else:

                logger.debug( "Test failed")




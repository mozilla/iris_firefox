# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from test_case import *




class test(base_test):

    def __init__(self, app):
        base_test.__init__(self, app)
        base_test.set_image_path(self, os.path.split(__file__)[0])
        self.assets = os.path.join(os.path.split(__file__)[0], "assets")
        self.meta = "Web compatibility test for bing.com"


    def run(self):
        url = "www.bing.com"
        search_item = "Barack Obama"
        home = "bing_home.png"
        search_page = "bing_search.png"
        search_field = "search_field.png"
        language = "language.png"
        language_changed = "language_changed.png"
        page_bottom = "page_bottom.png"

        logger.info("Accessing " + url + "...")
        navigate(url)


        if exists(home, 10):
            logger.info(url + " successfully loaded")
            type(search_item)
            type(Key.ENTER)
            time.sleep(3)
            logger.info("Searching " + search_item)

            if exists(search_page, 10):
                result = "PASS"
            else:
                result = "FAIL"

            print result

            if exists(search_field, 10):
                click(search_field)
                type(Key.TAB)
                time.sleep(2)
                type(Key.TAB)
                time.sleep(2)
                type(Key.ENTER)
                time.sleep(2)
                type(Key.TAB)
                time.sleep(2)
                type(Key.ENTER)
                if exists(language, 10):
                    click(language)
                    time.sleep(3)
                    type(Key.TAB)
                    type(Key.DOWN)
                    for i in range(7):
                        type(Key.TAB)
                    time.sleep(2)
                    type(Key.ENTER)
                    time.sleep(1)
                    logger.info("Language has been changed successfully")
                    if exists(language_changed, 10):
                        result = "PASS"
                    else:
                        result = "FAIL"
                    print result
                else:
                    logger.info("Language menu does not exist...")
            else:
                logger.error("Menu is not present on the page...")


            #checking if the scroll up/down works properly

        for i in range(20):
            scroll_down()
        time.sleep(5)
        if exists(page_bottom, 10):
            for i in range(20):
                scroll_up()
            if exists(language_changed, 10):
                result = "PASS"
            else:
                result = "FAIL"
            print result
        else:
            logger.error("The page was not scrolled correctly...")






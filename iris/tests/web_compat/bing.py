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


        # I have turned most of your logging.info statements into
        # logging.debug. We don't want to create any noise in the terminal
        # unless you specifically want to debug, in which case you
        # would start iris with arguments -i DEBUG

        logger.debug("Accessing " + url + "...")
        navigate(url)


        if exists(home, 10):
            logger.info(url + " successfully loaded")
            type(search_item)
            type(Key.ENTER)

            # This call to time.sleep probably not necessary,
            # as you will be calling exists(search_page, 10)
            # which gives you up to 10 seconds for the page to load

            time.sleep(3)
            logger.debug("Searching " + search_item)

            if exists(search_page, 10):
                result = "PASS"
            else:
                result = "FAIL"

            print result

            # This didn't work on Mac, for whatever reasons.
            # Maybe this test case requires us to click on the UI that
            # opens the Bing settings and set the language using
            # the UI controls there?

            # It's always nice to use keyboard shortcuts when we can,
            # but here it seems that the page is pretty fragile

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
                    logger.error("Language menu does not exist")
            else:
                logger.error("Menu is not present on the page")


            #checking if the scroll up/down works properly


        # You can also go directly to the bottom of the page
        # with page_end()
        for i in range(20):
            scroll_down()

        # this call to time.sleep(5) is probably not needed
        # since you will be waiting up to 10 seconds for the
        # next call to exists(page_bottom, 10)
        time.sleep(5)
        if exists(page_bottom, 10):
            for i in range(20):
                scroll_up()

                # You can also use page_home to go to
                # top of page, if you don't want to scroll
            if exists(language_changed, 10):
                result = "PASS"
            else:
                result = "FAIL"
            print result
        else:
            logger.error("The page was not scrolled correctly")


        # For the errors above - "Menu is not present" and
        # "The page was not scrolled correctly" - wouldn't it make
        # sense to turn those into tests as well? They should PASS/FAIL
        # instead of logging an error



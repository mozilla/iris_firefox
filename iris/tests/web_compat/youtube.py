# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from test_case import *



class test(base_test):

    def __init__(self, app):
        base_test.__init__(self, app)
        base_test.set_image_path(self, os.path.split(__file__)[0])
        self.assets = os.path.join(os.path.split(__file__)[0], "assets")
        self.meta = "Web compability test for youtube.com"


    def run(self):
        url="youtube.com"
        youtube_banner="youtube_banner.png"
        youtube_filter="filter_youtube_results.png"
        navigate(url)
        time.sleep(4)
        login_youtube()
        if exists(youtube_banner,10):
            logger.debug("Youtube Search")
            type("lord of the rings")
            type(Key.ENTER)
            if exists(youtube_filter,10):
                logger.debug("Results are displayed")
                time.sleep(3)
                #focus needs to be changed from search bar in order to scrool the page
                type(Key.TAB)
                for i in range(3):
                    scroll_down()
                time.sleep(4)
                logger.debug("Scrooling down")
                #wait scrool action to perform
                time.sleep(3)
                for i in range(4):
                    scroll_up()
                logger.debug("Scrooling up")
                if exists(youtube_filter,10):
                    logger.debug( "Test pass")
                else:
                    logger.debug( "Test failed")
        else:
            logger.debug( "Test failed")


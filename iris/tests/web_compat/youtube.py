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
        self.login_youtube()

        if exists(youtube_banner,10):
            logger.debug("Youtube Search")
            type("lord of the rings")
            type(Key.ENTER)
            if exists(youtube_filter,10):
                logger.debug("Results are displayed")
                time.sleep(3)

                # focus needs to be changed from search bar in order to scroll the page
                type(Key.TAB)
                logger.debug("Scrolling down")
                for i in range(3):
                    scroll_down()
                time.sleep(4)

                # wait scroll action to perform
                time.sleep(3)
                logger.debug("Scrolling up")
                for i in range(4):
                    scroll_up()

                # Soon to be replaced with assert statements, but for now, just print
                if exists(youtube_filter,10):
                    print "PASS"
                else:
                    print "FAIL"
        else:
            logger.debug( "Test failed")
            print "FAIL"

    def login_youtube(self):
        try:
            wait ("youtube_banner.png", 10)
        except:
            logger.error ("Can't find Youtube image in page, aborting test.")
            return

        for i in range(5):
            type(Key.TAB)
        type(Key.ENTER)
        if exists("youtube_sign_in.png",10):
            type(get_credential("Youtube","username"))
            time.sleep(3)
            for i in range(2):
                type(Key.TAB)
            type(Key.ENTER)
            time.sleep(3)
            type(get_credential("Youtube","password"))
            time.sleep(3)
            type(Key.TAB)
            type(Key.ENTER)

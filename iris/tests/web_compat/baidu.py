# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from test_case import *




class test(base_test):

    def __init__(self, app):
        base_test.__init__(self, app)
        base_test.set_image_path(self, os.path.split(__file__)[0])
        self.assets = os.path.join(os.path.split(__file__)[0], "assets")
        self.meta = "Web compability test for baidu.com"


    def run(self):
        url = "www.baidu.com"
        home = "baidu_home.png"
        search_item = "Barack Obama"
        search_page = "baidu_search_page.png"

        logger.debug("Accessing " + url + "...")
        navigate(url)

        if exists(home, 10):
            logger.debug(url + " successfully loaded")
            type(search_item)
            type(Key.ENTER)
            logger.debug("Searching " + search_item)

            if exists(search_page, 10):
                result = "PASS"
            else:
                result = "FAIL"

            print result
        else:
            logger.error(url + " can not be accessed...")


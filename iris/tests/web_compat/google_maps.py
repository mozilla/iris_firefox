# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from test_case import *



class test(base_test):

    def __init__(self, app):
        base_test.__init__(self, app)
        base_test.set_image_path(self, os.path.split(__file__)[0])
        self.assets = os.path.join(os.path.split(__file__)[0], "assets")
        self.meta = "Web compatibility test for maps.google.com"


    def run(self):
        url = "maps.google.com"
        navigate(url)

        # Check that the page is successfully loaded.
        if exists("googleMapsSearchBar.png", 20):
            # Type 'Mediterranean Sea' in the search bar.
            click("googleMapsSearchBar.png")
            paste("Mediterranean Sea")
            time.sleep(0.5)
            type(Key.ENTER)

            try:
                wait("googleMapsItemSearched.png", 20)
                logger.debug("Item searched found")
                print "PASS"
            except:
                logger.error ("Can't find the item searched in the page, aborting test.")
                print "FAIL"
                return
        else:
            print "FAIL"
        return

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from test_case import *



class test(base_test):

    def __init__(self, app):
        base_test.__init__(self, app)
        self.meta = "Web compability test for facebook.com--Login"


    def run(self):
        url="www.facebook.com"

        navigate(url)

        time.sleep(5)

        login_site("Facebook")
        time.sleep(3)

        print ("Hello world!")
        return

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
import random
from test_case import *

class test(base_test):

    def __init__(self, app):
        base_test.__init__(self, app)
        base_test.set_image_path(self, os.path.split(__file__)[0])
        self.assets = os.path.join(os.path.split(__file__)[0], "assets")
        self.meta = "Web compability test for linkedin.com"

    def run(self):
        url="www.linkedin.com"
        navigate(url)

        # Check that the login page is loaded.
        if exists("linkedinLoginPage.png", 10):
            print "PASS"
            #  Login to linkedin.
            login_linkedin("Linkedin")

            time.sleep(5)

            #  Check that user successfully logged in.
            if exists("linkedinHomePage.png", 10):
                print "PASS"
                click("linkedinPostButton")
                time.sleep(2)
                # Posting a message with a random character at the end. Same message cannot be posted twice, an error is thrown.
                paste("This is a test message " +random.choice('abcdefghijklmnopqrstuvwxyz'))
                click("linkedinPostButton")
                time.sleep(2)

                # Check that the message has been posted.
                if exists("linkedinMessageIsPosted", 10):
                    print "PASS"
                    # Scroll down.
                    for number in range(30):
                        type(text=Key.DOWN)

                    time.sleep(2)

                    # Scroll up.
                    for number in range(30):
                        type(text=Key.UP)

                    print "PASS"
                else:
                    print "FAIL"
            else:
                print "FAIL"
        else:
            print "FAIL"

        click("linkedinMenu.png")
        click("linkedinSignOut.png")

        time.sleep(2)

        # Check that user is successfully logged out.
        if exists("linkedinLoginPage.png", 10):
            print "PASS"
        return

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
        self.enable = False

    def run(self):
        url="www.linkedin.com"
        navigate(url)

        # Check that the login page is loaded.
        if exists("linkedinLoginPage.png", 10):
            #  Login to linkedin.
            if exists("linkedinEmailField.png", 10):
                click("linkedinEmailField.png")
                login_site("Linkedin")
                dont_save_password()
            else:
                print "FAIL"

            #  Check that user successfully logged in.
            if exists("linkedinHomePage.png", 10):
                click("linkedinPostButton")
                time.sleep(2)
                # Posting a message with a random character at the end. Same message cannot be posted twice, an error is thrown.
                paste("This is a test message " +random.choice('abcdefghijklmnopqrstuvwxyz'))
                click("linkedinPostButton")

                # Check that the message has been posted.
                if exists("linkedinMessageIsPosted", 10):
                    # Scroll down.
                    for number in range(30):
                        scroll_down()

                    time.sleep(2)

                    # Scroll up.
                    for number in range(30):
                        scroll_down()

                    print "PASS"
                else:
                    print "FAIL"
            else:
                print "FAIL"
        else:
            print "FAIL"

        click("linkedinMenu.png")
        click("linkedinSignOut.png")

        # Check that user is successfully logged out.
        if exists("linkedinLoginPage.png", 10):
            print "PASS"
        return

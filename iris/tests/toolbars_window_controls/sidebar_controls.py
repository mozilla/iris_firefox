# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *



class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.assets = os.path.join(os.path.split(__file__)[0], "assets")
        self.meta = "This is a test of the sidebar controls"


    def run(self):
        bookmarks_sidebar()
        if exists("x_button_sidebar.png", 10):
            print "Sidebar was opened successfully"
            hover("x_button_sidebar.png")
            if exists("x_button_sidebar_hovered.png", 10):
                print "Hover state displayed properly"
                click("x_button_sidebar_hovered.png")
                if waitVanish("sidebar_title.png", 10):
                    print "Sidebar was closed successfully"
                    result = "PASS"
                else:
                    print "Sidebar is still open"
                    result = "FAIL"
            else:
                result = "FAIL"
        else:
            print "Sidebar is not open"
            result = "FAIL"

        print result

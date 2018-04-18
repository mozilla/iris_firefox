# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from test_case import *



class test(base_test):

    def __init__(self, app):
        base_test.__init__(self, app)
        base_test.set_image_path(self, os.path.split(__file__)[0])
        self.assets = os.path.join(os.path.split(__file__)[0], "assets")
        self.meta = "This is a test of the 'About Firefox' window controls"


    def run(self):
        # Helper function in general.py
        open_library()
        time.sleep(1)

        if exists("library_title.png", 10):
            print "The library was opened successfully"
            print "PASS"

            maximize_window()
            time.sleep(1)
            if exists("library_restore_button.png", 10):
                print "The library was maximized successfully"
                print "PASS"
            else:
                print "The library was not maximized"
                print "FAIL"
                return

            minimize_window()
            time.sleep(1)
            if exists("library_maximize_button.png", 10):
                print "The library was restored successfully"
                print "PASS"
            else:
                print "The library was not restored"
                print "FAIL"
                return

            minimize_window()
            time.sleep(1)
            if waitVanish("library_title.png", 10):
                print "PASS"
                logger.debug("window successfully minimized")
            else:
                print "FAIL"
                logger.error("window not minimized, aborting test")
                return

            restore_window_from_taskbar()

        else:
            print "The library was not opened"
            print "FAIL"

        close_auxiliary_window()
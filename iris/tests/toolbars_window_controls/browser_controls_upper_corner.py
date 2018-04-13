# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from test_case import *



class test(base_test):

    def __init__(self, app):
        base_test.__init__(self, app)
        base_test.set_image_path(self, os.path.split(__file__)[0])
        self.assets = os.path.join(os.path.split(__file__)[0], "assets")
        self.meta = "This is a test case that checks that the upper corner browser controls work as expected"


    def run(self):
        url = "about:home"
        navigate(url)

        if exists("browser_controls_upper_corner.png", 10):
            hover("window_controls_minimize.png")
            time.sleep(0.5)
            if exists("hover_minimize_control.png", 10):
                print "PASS"
                logger.debug("hover over the 'minimize' controler works correctly")
            else:
                print "FAIL"
                logger.debug("hover over the 'minimize' controler doesn't work correctly")
            hover("window_controls_restore.png")
            time.sleep(0.5)
            if exists("hover_restore_control.png", 10):
                print "PASS"
                logger.debug("hover over the 'restore' controler works correctly")
            else:
                print "FAIL"
                logger.debug("hover over the 'restore' controler doesn't work correctly")
            hover("window_controls_close.png")
            time.sleep(0.5)
            if exists("hover_close_control.png", 10):
                print "PASS"
                logger.debug("hover over the 'close' controler works correctly")
            else:
                print "FAIL"
                logger.debug("hover over the 'close' controler doesn't work correctly")
            time.sleep(0.5)
            # Restore window
            minimize_window()
            hover("window_controls_maximize.png")
            time.sleep(0.5)
            if exists("hover_maximize_control.png", 10):
                print "PASS"
                logger.debug("hover over the 'maximize' controler works correctly")
                logger.debug("window successfully restored")
            else:
                print "FAIL"
                logger.debug("hover over the 'maximize' controler doesn't work correctly")
            #Minimize window
            minimize_window()
            time.sleep(0.5)
            if waitVanish("hamburger_menu.png", 10):
                print "PASS"
                logger.debug("window successfully minimized")
            else:
                print "FAIL"
                logger.error("window not minimized, aborting test")
                return
            # Focus on Firefox and open the browser again
            type(text=Key.TAB, modifier=KeyModifier.ALT)
            maximize_window()
            time.sleep(0.5)
            if exists("hamburger_menu.png", 10):
                print "PASS"
                logger.debug("window successfully maximized")
            else:
                print "FAIL"
                logger.error("window not in view, aborting test.")
                return
            # Close the window
            if exists("hamburger_menu.png", 10):
                close_window()
                time.sleep(0.5)
                type(Key.ENTER)
                time.sleep(0.5)
                if waitVanish("hamburger_menu.png", 10):
                    print "PASS"
                    logger.debug("window successfully closed")
                else:
                    print "FAIL"
                    logger.error("window not closed, aborting test")
                    return
            else:
                 print "FAIL"
                 logger.error("Can't find the 'hamburger menu' in the page, aborting test.")
                 return
        else:
            print "FAIL"



        


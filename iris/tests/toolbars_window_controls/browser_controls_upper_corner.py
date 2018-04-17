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

            if get_os() == "win":
                hover("window_controls_restore.png")
                time.sleep(0.5)
                if exists("hover_restore_control.png", 10):
                    print "PASS"
                    logger.debug("hover over the 'restore' controler works correctly")
                else:
                    print "FAIL"
                    logger.debug("hover over the 'restore' controler doesn't work correctly")
            else:
                hover("window_controls_maximize.png")
                time.sleep(0.5)
                if exists("hover_maximize_control.png", 10):
                    print "PASS"
                    logger.debug("hover over the 'maximize' controler works correctly")
                else:
                    print "FAIL"
                    logger.debug("hover over the 'maximize' controler doesn't work correctly")

            hover("window_controls_close.png")
            time.sleep(0.5)
            if exists("hover_close_control.png", 10):
                print "PASS"
                logger.debug("hover over the 'close' controler works correctly")
            else:
                print "FAIL"
                logger.debug("hover over the 'close' controler doesn't work correctly")
            time.sleep(0.5)

            if get_os() == "win":
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
            else:
                 # Maximize window
                 hover("window_controls_maximize.png")
                 time.sleep(0.5)
                 click("window_controls_maximize.png")
                 time.sleep(0.5)
                 keyDown(Key.ALT)
                 hover("window_controls_restore.png")
                 keyUp(Key.ALT)
                 time.sleep(0.5)
                 if exists("hover_restore_control.png", 10):
                     print "PASS"
                     logger.debug("hover over the 'restore' controler works correctly")
                     logger.debug("window successfully maximized")
                 else:
                     print "FAIL"
                     logger.debug("hover over the 'restore' controler doesn't work correctly")

            if get_os() == "win":
                 if exists("hamburger_menu.png", 10):
                     #Minimize window
                     minimize_window()
                     time.sleep(0.5)
                     if waitVanish("hamburger_menu.png", 10):
                         print "PASS"
                         logger.debug("window successfully minimized")
                     else:
                         print "FAIL"
                         logger.error("window not minimized, aborting test")
                 else:
                     print "FAIL"
                     logger.error("Can't find the 'hamburger menu' in the page, aborting test.")
            else:
                # Minimize window
                if exists("hamburger_menu.png", 10):
                    click("window_controls_minimize.png")
                    time.sleep(3)
                    if waitVanish("hamburger_menu.png", 10):
                        print "PASS"
                        logger.debug("window successfully minimized")
                    else:
                        print "FAIL"
                        logger.error("window not minimized, aborting test")
                else:
                    print "FAIL"
                    logger.error("Can't find the 'hamburger menu' in the page, aborting test.")

            # Focus on Firefox and open the browser again
            type(text=Key.TAB, modifier=KeyModifier.ALT)
            if get_os() == "win":
                maximize_window()
                time.sleep(0.5)
            else:
                time.sleep(0.5)

            if exists("hamburger_menu.png", 10):
                print "PASS"
                logger.debug("window successfully opened again")
            else:
                print "FAIL"
                logger.error("window not in view, aborting test.")

            # Close the window
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
        else:
            print "FAIL"
            logger.error("Can't find the upper corner controls in the page, aborting test.")





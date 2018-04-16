# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from test_case import *


class test(base_test):

    def __init__(self, app):
        base_test.__init__(self, app)
        base_test.set_image_path(self, os.path.split(__file__)[0])
        self.assets = os.path.join(os.path.split(__file__)[0], "assets")
        self.meta = "This is a test case that checks that the 'drag space' can be activated properly"

    def run(self):
        url = "about:home"
        navigate(url)

        # Open Customize from the Hamburger Menu
        click_hamburger_menu_option("Customize")

        # Check that the customize page is opened by searcing for text "overflow menu"
        try:
            wait("overflow menu", 10)
            print "PASS"
            logger.debug("customize page present")
        except:
            print "FAIL"
            logger.error("Can't find overflow menu text, aborting test.")
            return
        else:
            if exists("customize_page_drag_space_disabled.png", 10) and exists("drag_space_disabled.png", 10):
                click("drag_space_disabled.png")
                if exists(Pattern("customize_page_drag_space_enabled.png").similar(0.98), 10) and exists("drag_space_enabled.png", 10):
                    print "PASS"
                    logger.debug("'drag space' successfully activated in the 'Customize' page")
                else:
                    print "FAIL"
                    logger.error("'drag space' not properly activated, aborting test")
                    return
            else:
                print "FAIL"
                logger.error("'Customize' page is not correctly displayed before 'drag space' is enabled, aborting test")
                return
            close_customize_page()

            # Check that changes persist in a new tab
            new_tab()
            if exists(Pattern("drag_space_enabled_new_tab.png").similar(0.98), 10):
                print "PASS"
                logger.debug("'drag space' successfully activated in a new tab")
            else:
                print "FAIL"
                logger.debug("'drag space' not correctly activated in a new tab, aborting test")
                return

            if exists("hamburger_menu.png", 10):
                # Minimize window
                minimize_window()
                if waitVanish("hamburger_menu.png", 10):
                    print "PASS"
                    logger.debug("window successfully minimized")
                else:
                    print "FAIL"
                    logger.error("window not minimized, aborting test")
                    return
            else:
                print "FAIL"
                logger.error("Can't find the 'hamburger menu' in the page, aborting test.")
                return

            # Focus on Firefox and open the browser again
            restore_window_from_taskbar()
            maximize_window()
            if exists("hamburger_menu.png", 10):
                print "PASS"
                logger.debug("window in view again")
            else:
                print "FAIL"
                logger.error("window not in view, aborting test.")
                return

            # Restore window (applies to Windows and Linux)
            if get_os() =="osx":
                print "Window size restore not applicable on OSX"
            else:
                if exists("window_controls_restore.png", 10):
                    minimize_window()
                    if exists("window_controls_maximize.png", 10):
                        print "PASS"
                        logger.debug("window successfully restored")
                        # Maximize window
                        maximize_window()
                        if exists("window_controls_restore.png", 10):
                            print "PASS"
                            logger.debug("window successfully maximized")
                        else:
                            print "FAIL"
                            logger.error("window not maximized, aborting test")
                            return
                    else:
                        print "FAIL"
                        logger.error("window not restored, aborting test")
                        return
                else:
                    print "FAIL"
                    logger.error("the window control 'restore' not visible, aborting test.")
                    return

            # Close the window
            if exists("hamburger_menu.png", 10):
                close_window()
                time.sleep(0.5)
                type(Key.ENTER)
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




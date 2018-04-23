# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from test_case import *


class test(base_test):

    def __init__(self, app):
        base_test.__init__(self, app)
        base_test.set_image_path(self, os.path.split(__file__)[0])
        self.assets = os.path.join(os.path.split(__file__)[0], "assets")
        self.meta = "This is a test case that checks if the Web Console controls work as expected"

    def run(self):

        url = "about:home"
        navigate(url)

        open_web_console()

        dock_button = "dock_to_side.png"
        dock_button_activated = "dock_to_side_activated.png"
        separate_window_button = "separate_window.png"
        close_dev_tools_button = "close_dev_tools.png"
        menu = "hamburger_menu.png"
        dev_tools_window = "dev_tools_window.png"

        buttons = [dock_button, separate_window_button, close_dev_tools_button]

        a = 0
        found = False
        for i in buttons:
            if exists(i, 3):
                a = a + 1
            if a == len(buttons):
                logger.debug("Buttons has been found")
                found = True

        if found:
            # Check if the labels are displayed when the cursor hovers over the buttons.
            screen = get_screen()
            buttons_region = Sikuli.Region(screen.getW()/2, screen.getH()/2, screen.getW()/2, screen.getH()/2)

            hover(dock_button)

            dock_message = 'Dock to side'

            if buttons_region.exists(dock_message, 10):
                logger.debug("'Dock to side of browser window' label is displayed")
                print "PASS"
            else:
                logger.error("'Dock to side of browser window' is not displayed")
                print "FAIL"

            hover(separate_window_button)

            separate_window_message = 'Show in'

            if buttons_region.exists(separate_window_message, 10):
                logger.debug("'Show in separate window' label is displayed")
                print "PASS"
            else:
                logger.error("Show in separate window' is not displayed")
                print "FAIL"

            hover(close_dev_tools_button)

            close_message = 'Close'

            if buttons_region.exists(close_message, 10):
                logger.debug("'Close Developer Tools' label is displayed")
                print "PASS"
            else:
                logger.error("Close Developer Tools' is not displayed")
                print "FAIL"

            # Checking the buttons functionality.
            coord = find(menu)
            right_uper_corner = Sikuli.Region(coord.x - 300, 0, 300, 300)

            click(dock_button)
            if right_uper_corner.exists(dock_button_activated, 5):
                logger.debug("Dock to side button works !!!")
                print "PASS"
            else:
                logger.error("Dock to side doesn't work")
                print "FAIL"

            click(separate_window_button)
            if exists(dev_tools_window, 10):
                logger.debug("Show in separate window button works !!!")
                print "PASS"
            else:
                logger.error("Show in separate window button doesn't work")
                print "FAIL"

            # Here is necessary to return back at the initial state in order to verify the close button functionality.
            click(dock_button_activated)

            click(close_dev_tools_button)
            if waitVanish(dock_button_activated, 10):
                logger.debug("Web Console has been closed !")
                print "PASS"
            else:
                logger.error("The Web Console can not be closed!! Aborting..")
                print "FAIL"
        else:
            logger.error("Buttons has not been found")
            print "FAIL"

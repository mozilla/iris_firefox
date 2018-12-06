# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'This test will verify if Pyautogui mouse is working properly in a framebuffer environment.'
        self.exclude = Platform.MAC, Platform.WINDOWS

    def run(self):

        navigate(LocalWeb.MOZILLA_TEST_SITE)

        # Check mouse movement in a full screen environment
        try:
            pyautogui.moveTo(300, 300)
            mouse_position = pyautogui.position()
        except:
            raise Exception('Pyautogui error!!')

        else:
            if mouse_position[0] == 300 and mouse_position[1] == 300:
                logger.info('[MoveTo]Mouse successfully moved to  position x= ' + str(mouse_position[0]) + ' y=' + str(
                    mouse_position[1]))
            else:
                logger.error('Invalid mouse position!' + ' x=' +
                             str(mouse_position[0]) + ' y=' + str(mouse_position[1]))
                exit(1)

        # Check mouse movement only in Y axis
        try:
            pyautogui.moveTo(None, 700)
            mouse_position = pyautogui.position()
        except:
            raise Exception('Pyautogui error!!')
        else:
            if mouse_position[0] == 300 and mouse_position[1] == 700:
                logger.info('[MoveTo]Mouse succesfully changed to position x=' + str(mouse_position[0]) + ' y=' +
                            str(mouse_position[1]))
            else:
                logger.error('Invalid mouse position!' + 'x=' + str(mouse_position[0]) + ' y=' + str(mouse_position[1]))
                exit(1)

        # Move the mouse down 50 pixels
        try:
            pyautogui.moveRel(0, 50)
            mouse_position = pyautogui.position()
        except:
            raise Exception('Pyautogui error!!')

        else:
            if mouse_position[0] == 300 and mouse_position[1] == 750:
                logger.info(
                    '[MoveRel]Mouse succesfully moved to position x=' + str(mouse_position[0]) + ' y=' + str(
                        mouse_position[1]))
            else:
                logger.error(
                    'Invalid mouse position!' + ' x=' + str(mouse_position[0]) + ' y=' + str(mouse_position[1]))
                exit(1)

        # Mouse Click on specific coordonates
        try:
            pyautogui.click(x=850, y=850)
            mouse_position = pyautogui.position()
        except:
            raise Exception('Pyautogui error!!')

        else:
            if mouse_position[0] == 850 and mouse_position[1] == 850:
                logger.info(
                    '[Click]Mouse succesfully moved to position x=' + str(mouse_position[0]) + ' y=' + str(
                        mouse_position[1]))
            else:
                logger.error('Invalid mouse position!' + 'x=' + str(mouse_position[0]) + ' y=' + str(mouse_position[1]))
                exit(1)

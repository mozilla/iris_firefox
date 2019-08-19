# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description="This test will verify if PyAutoGUI mouse is working properly in a frame buffer environment."
    )
    def run(self, firefox):
        try:
            pyautogui.moveTo(300, 300)
            mouse_position = pyautogui.position()
        except:
            raise Exception('PyAutoGUI error.')

        else:
            if mouse_position[0] == 300 and mouse_position[1] == 300:
                logger.debug(
                    'Mouse successfully moved to position ({}, {}).'.format(mouse_position[0], mouse_position[1]))
            else:
                logger.error('Invalid mouse position: ({}, {}).'.format(mouse_position[0], mouse_position[1]))
                exit(1)

        try:
            pyautogui.moveTo(None, 700)
            mouse_position = pyautogui.position()
        except:
            raise Exception('PyAutoGUI error.')
        else:
            if mouse_position[0] == 300 and mouse_position[1] == 700:
                logger.debug(
                    'Mouse successfully changed to position ({}, {}).'.format(mouse_position[0], mouse_position[1]))
            else:
                logger.error('Invalid mouse position: ({}, {}).'.format(mouse_position[0], mouse_position[1]))
                exit(1)

        try:
            pyautogui.moveRel(0, 50)
            mouse_position = pyautogui.position()
        except:
            raise Exception('PyAutoGUI error.')

        else:
            if mouse_position[0] == 300 and mouse_position[1] == 750:
                logger.debug(
                    'Mouse successfully moved to position ({}, {}).'.format(mouse_position[0], mouse_position[1]))
            else:
                logger.error(
                    'Invalid mouse position: ({}, {}).'.format(mouse_position[0], mouse_position[1]))
                exit(1)

        try:
            pyautogui.click(x=850, y=850)
            mouse_position = pyautogui.position()
        except:
            raise Exception('PyAutoGUI error.')

        else:
            if mouse_position[0] == 850 and mouse_position[1] == 850:
                logger.debug(
                    'Mouse successfully moved to position ({}, {}).'.format(mouse_position[0], mouse_position[1]))
            else:
                logger.error('Invalid mouse position:({}, {}).'.format(mouse_position[0], mouse_position[1]))
                exit(1)

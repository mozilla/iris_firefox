# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'This test verifies if Pyautogui/MSS screenshot and image search are working properly in a ' \
                    'framebuffer environment.'
        self.exclude = Platform.MAC, Platform.WINDOWS

    def run(self):

        # Image sccreenshot with pyautogui
        try:
            image = pyautogui.screenshot()
        except:
            raise Exception('Error occured while taking screenshot with pyautogui on full screen ')
        else:
            if image:
                logger.info('Pyautogui Screenshot succesfully created  for full screen region')
            else:
                logger.error('Invalid Screenshot object')
                exit(1)

        # Image screenshot with pyautogui
        try:
            image = pyautogui.screenshot(region=(0, 0, 300, 400))
        except:
            raise Exception('Error occured while taking screenshot with pyautogui on a specific region ')
        else:
            if image:
                logger.info('Pyautogui Screenshot succesfully created  for a specific region')
            else:
                logger.error('Invalid Screenshot object')
                exit(1)

        # Image search in full screen with MSS
        try:
            sct = mss.mss()
            monitor = {"top": 0, "left": 0, "width": SCREEN_WIDTH, "height": SCREEN_HEIGHT}
            image = sct.grab(monitor)
        except:
            raise Exception('Error occured while taking screenshot with MSS!!!!')
        else:
            if image:
                logger.info('MSS Screenshot succesfully created  for full screen region')
            else:
                logger.error('MSS Screenshot created  on full screen FAILED!!!')
                exit(1)

        # Image search in a specific screen region with MSS
        try:
            sct = mss.mss()
            monitor = {"top": SCREEN_HEIGHT / 2, "left": SCREEN_WIDTH / 2, "width": SCREEN_WIDTH / 2,
                       "height": SCREEN_HEIGHT / 2}
            image = sct.grab(monitor)
        except:
            raise Exception('Error occured while taking screenshot with MSS!!!!')
        else:
            if image:
                logger.info('MSS Screenshot succesfully created for a specific region')
            else:
                logger.error('MSS Screenshot created on specific region FAILED!!!!')
                exit(1)

        # Image search in full screen with Pyautogui

        navigate(LocalWeb.MOZILLA_TEST_SITE)

        expected_1 = exists(LocalWeb.MOZILLA_LOGO, 10)
        if expected_1:
            logger.info('Image search in full screen screenshot succeed ')
        else:
            logger.error('Image search in full screen screenshot failed!!!')
            exit(1)

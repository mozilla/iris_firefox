# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


import mss

from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='This test verifies if PyAutoGUI/MSS screenshot and image search are working properly in a '
                    'frame buffer environment.',
        locale=['en-US']
    )
    def run(self, firefox):

        try:
            image = pyautogui.screenshot()
        except:
            raise Exception('Error occurred while taking screenshot with PyAutoGUI on full screen.')
        else:
            if image:
                logger.info('PyAutoGUI Screenshot successfully created  for full screen region.')
            else:
                logger.error('Invalid Screenshot object.')
                exit(1)

        try:
            image = pyautogui.screenshot(region=(0, 0, 300, 400))
        except:
            raise Exception('Error occurred while taking screenshot with PyAutoGUI on a specific region ')
        else:
            if image:
                logger.info('PyAutoGUI Screenshot successfully created  for a specific region')
            else:
                logger.error('Invalid Screenshot object')
                exit(1)

        try:

            sct = mss.mss()
            monitor = {"top": 0, "left": 0, "width": int(Screen().width), "height": int(Screen().height)}
            image = sct.grab(monitor)
        except:
            raise Exception('Error occurred while taking screenshot with MSS!!!!')
        else:
            if image:
                logger.info('MSS Screenshot successfully created  for full screen region')
            else:
                logger.error('MSS Screenshot created  on full screen FAILED!!!')
                exit(1)

        try:
            sct = mss.mss()
            monitor = {"top": int(Screen().height / 2), "left": int(Screen().width / 2),
                       "width": int(Screen().width / 2),
                       "height": int(Screen().height / 2)}
            image = sct.grab(monitor)
        except:
            raise Exception('Error occurred while taking screenshot with MSS!!!!')
        else:
            if image:
                logger.info('MSS Screenshot successfully created for a specific region')
            else:
                logger.error('MSS Screenshot created on specific region FAILED!!!!')
                exit(1)

        navigate(LocalWeb.MOZILLA_TEST_SITE)
        expected_1 = exists(LocalWeb.MOZILLA_LOGO, 10)
        if expected_1:
            logger.info('Image search in full screen screenshot succeed ')
        else:
            logger.error('Image search in full screen screenshot failed!!!')
            exit(1)

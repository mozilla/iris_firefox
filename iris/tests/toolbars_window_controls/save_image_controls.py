# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This is a test of the Save Image dialog controls'

    def run(self):
        url = 'cdn2.collective-evolution.com/assets/uploads/2009/09/url.jpeg'
        test_image = 'sleepy_head_nose.png'
        save_as = 'save_as.png'

        navigate(url)
        try:
            wait(test_image, 5)
        except:
            raise FindError('Test Image not loaded')
        else:
            rightClick(test_image, 1)

        # wait a moment to ensure the context menu is responisve
        time.sleep(1)
        type(Key.DOWN)
        type(Key.DOWN)
        type(Key.DOWN)
        type(Key.ENTER)

        expected_1 = exists(save_as, 10)
        assert_true(self, expected_1, 'Save Image dialog is present')

        if Settings.getOS() == Platform.MAC:
            click_cancel_button()
        else:
            close_auxiliary_window()

        try:
            expected_2 = waitVanish(save_as, 5)
            assert_true(self, expected_2, 'Save Image dialog was closed')
        except:
            raise FindError('Save Image dialog is still present')

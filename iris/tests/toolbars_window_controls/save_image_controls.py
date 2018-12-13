# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'This is a test of the Save Image dialog controls'
        self.test_case_id = '118803'
        self.test_suite_id = '1998'
        self.locales = ['en-US']

    def run(self):
        url = self.get_web_asset_path('overworked.jpeg')
        test_pattern = Pattern('sleepy_head_nose.png')
        save_as_pattern = Pattern('save_as.png')

        navigate(url)
        try:
            wait(test_pattern, 5)
        except FindError:
            raise FindError('Test Image not loaded')
        else:
            right_click(test_pattern, 1)

        time.sleep(Settings.UI_DELAY)
        type(Key.DOWN)
        type(Key.DOWN)
        type(Key.DOWN)
        type(Key.ENTER)

        expected_1 = exists(save_as_pattern, 10)
        assert_true(self, expected_1, 'Save Image dialog is present')

        if Settings.get_os() == Platform.WINDOWS:
            click_window_control('close')
        else:
            if Settings.is_linux():
                click_window_control('maximize')
            click_cancel_button()

        try:
            expected_2 = wait_vanish(save_as_pattern, 5)
            assert_true(self, expected_2, 'Save Image dialog was closed')
        except FindError:
            raise FindError('Save Image dialog is still present')

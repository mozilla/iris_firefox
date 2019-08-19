# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description='This is a test of the Save Image dialog controls.',
        locale=['en-US'],
        test_case_id='118803',
        test_suite_id='1998'
    )
    def run(self, firefox):
        test_pattern = Pattern('sleepy_head_nose.png')
        save_as_pattern = Pattern('save_as.png')

        url = PathManager.get_web_asset_dir('overworked.jpeg')

        navigate(url)

        test_pattern_found = exists(test_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert test_pattern_found, 'Test page are loaded and image displays'

        right_click(test_pattern, 1)
        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)
        type(Key.DOWN)
        type(Key.DOWN)
        type(Key.DOWN)
        type(Key.ENTER)

        assert exists(save_as_pattern, FirefoxSettings.FIREFOX_TIMEOUT), 'Save Image dialog is present.'

        if OSHelper.is_windows():
            click_window_control('close')
        else:
            if OSHelper.is_linux():
                click_window_control('maximize')
            click_cancel_button()

        try:
            assert wait_vanish(save_as_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT), 'Save Image dialog was closed.'
        except FindError:
            raise FindError('Save Image dialog is still present.')

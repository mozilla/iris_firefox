# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='This test case adds links using \'CTRL\' + \'ENTER\' keys',
        locale=['en-US'],
        test_case_id='119484',
        test_suite_id='1902'

    )
    def run(self, firefox):
        cnn_tab_pattern = Pattern('cnn_tab.png')
        facebook_tab_pattern = Pattern('facebook_tab.png')

        region = Region(0, 0, Screen().width / 2, Screen().height / 3)

        select_location_bar()
        paste('cnn')

        key_down(Key.CTRL)
        type(Key.ENTER)
        key_up(Key.CTRL)

        close_content_blocking_pop_up()

        expected = region.exists(LocalWeb.CNN_LOGO, FirefoxSettings.HEAVY_SITE_LOAD_TIMEOUT)
        assert expected, 'CNN page successfully loaded .'

        new_tab()

        select_location_bar()
        type('facebook')

        key_down(Key.CTRL)
        type(Key.ENTER)
        key_up(Key.CTRL)

        expected = region.exists(facebook_tab_pattern, FirefoxSettings.HEAVY_SITE_LOAD_TIMEOUT)
        assert expected, 'Facebook page successfully loaded.'

        previous_tab()
        select_location_bar()

        key_down(Key.CTRL)
        type(Key.ENTER)
        key_up(Key.CTRL)

        expected = region.exists(cnn_tab_pattern, FirefoxSettings.HEAVY_SITE_LOAD_TIMEOUT)
        assert expected, 'CNN page successfully reloaded.'

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
from targets.firefox.fx_testcase import *



class Test(FirefoxTest):
    extra = pytest.mark.EXTRINFO(
        channel='beta',
        # exclude='osx',
        # profile='new',
        # fx_version="63",
        test_case_id="119484",
        test_suite_id="1902",
    )

    details = pytest.mark.VALUES(
        description="This test case adds links using \'CTRL\' + \'ENTER\' keys",
        locale='[en-US]',
        values=extra
    )


    def test_run(self):
        cnn_tab_pattern = Pattern('cnn_tab.png')
        cnn_icon_pattern = Pattern('cnn_icon@2x.png')
        facebook_tab_pattern = Pattern('facebook_tab.png')

        # maximize_window()
        screen=Screen().screen_region

        region = Region(0, 0, screen.width/2, screen.height / 3)

        # Navigate to the 'CNN' page using the 'CTRL' + 'ENTER' keys starting from the name of the page.
        select_location_bar()
        paste('cnn')

        key_down(Key.CTRL)
        type(Key.ENTER)
        # key_up(Key.CTRL)


        # close_content_blocking_pop_up()

        expected = region.exists(cnn_icon_pattern, 10)
        print ('EXPECTED IS',expected)
        assert  expected, 'CNN page successfully loaded .'

        print('URAAAA')

        # In a new tab, navigate to the 'Facebook' page using the 'CTRL' + 'ENTER' keys starting from the name of
        # the page.
        new_tab()

        select_location_bar()
        type('facebook')

        key_down(Key.CTRL)
        type(Key.ENTER)
        key_up(Key.CTRL)

        expected = region.exists(facebook_tab_pattern, 10)
        assert  expected, 'Facebook page successfully loaded.'

        # Navigate to the previous tab and press 'CTRL'/'CMD' + 'ENTER' keys in the address bar.
        previous_tab()
        select_location_bar()

        key_down(Key.CTRL)
        type(Key.ENTER)
        key_up(Key.CTRL)

        expected = region.exists(cnn_tab_pattern, 10)
        assert  expected, 'CNN page successfully reloaded.'

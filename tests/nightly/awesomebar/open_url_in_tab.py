# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.nightly.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='This test case opens an URL in a new tab when the \'browser.search.openintab\' preference is ' 
                    'set to true.',
        locale=['en-US'],
        test_case_id='117527',
        test_suite_id='1902'
    )
    def run(self, firefox):
        search_settings_pattern = Pattern('search_settings.png')

        region = Screen().new_region(0, 0, Screen.SCREEN_WIDTH, 2 * Screen.SCREEN_HEIGHT / 3)

        change_preference('browser.search.openintab', True)

        select_location_bar()
        paste('about:newtab')
        type(Key.ENTER)

        expected = region.exists(search_settings_pattern, 10)
        assert expected, 'The \'about:newtab\' page successfully loaded.'

        select_location_bar()
        paste(LocalWeb.FIREFOX_TEST_SITE)
        type(Key.ENTER)

        # Link is opened in the same tab.
        expected = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert expected, 'Page successfully loaded, firefox logo found.'

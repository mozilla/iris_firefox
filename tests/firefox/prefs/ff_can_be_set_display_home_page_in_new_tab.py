# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Firefox can be set to display Firefox Home in new tabs ',
        locale=['en-US'],
        test_case_id='2241',
        test_suite_id='161472'
    )
    def run(self, firefox):
        new_tab_preferences_pattern = Pattern('new_tab_preferences.png')
        default_setting_home_pattern = Pattern('default_new_tab_setting_home.png')

        navigate('about:preferences#home')

        preferences_page_opened = exists(new_tab_preferences_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert preferences_page_opened, 'The about:preferences page is successfully loaded.'

        new_tab_preferences_location = find(new_tab_preferences_pattern)
        new_tab_preferences_width, new_tab_preferences_height = new_tab_preferences_pattern.get_size()
        new_tab_section_region = Region(new_tab_preferences_location.x, new_tab_preferences_location.y,
                                        new_tab_preferences_width*10, new_tab_preferences_height*2)

        home_option_displayed = exists(default_setting_home_pattern, FirefoxSettings.FIREFOX_TIMEOUT,
                                       new_tab_section_region)
        assert home_option_displayed, 'The options for "New Tabs" section are displayed and selected.'

        new_tab()

        home_page_loaded = exists(Utils.TOP_SITES, FirefoxSettings.FIREFOX_TIMEOUT)
        assert home_page_loaded, 'The Firefox Home page is successfully loaded.'

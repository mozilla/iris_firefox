# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Home pages can be successfully restored to default',
        locale=['en-US'],
        test_case_id='2241',
        test_suite_id='143548'
    )
    def run(self, firefox):
        homepage_preferences_pattern = Pattern('homepage_preferences.png')
        default_setting_home_pattern = Pattern('default_new_tab_setting_home.png')
        custom_url_option_pattern = Pattern('custom_url_option.png')
        url_field_pattern = Pattern('url_field.png')

        navigate('about:preferences#home')

        preferences_page_opened = exists(homepage_preferences_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert preferences_page_opened, 'The about:preferences page is successfully loaded.'

        homepage_preferences_location = find(homepage_preferences_pattern)
        homepage_preferences_width, homepage_preferences_height = homepage_preferences_pattern.get_size()
        homepage_section_region = Region(homepage_preferences_location.x, homepage_preferences_location.y,
                                         homepage_preferences_width*3, int(homepage_preferences_height*1.5))

        home_option_displayed = exists(default_setting_home_pattern, FirefoxSettings.FIREFOX_TIMEOUT,
                                       homepage_section_region)
        assert home_option_displayed, 'The options for "Home" section are displayed.'

        click(default_setting_home_pattern, region=homepage_section_region)

        custom_option_displayed = exists(custom_url_option_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert custom_option_displayed, 'The \'Custom\' option for "Home" section is displayed.'

        click(custom_url_option_pattern)

        custom_option_displayed = exists(url_field_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert custom_option_displayed, 'The \'Paste a URL...\' field is displayed.'

        click(url_field_pattern)

        time.sleep(Settings.DEFAULT_UI_DELAY)

        paste(LocalWeb.FIREFOX_TEST_SITE)
        type(Key.ENTER)

        click(NavBar.HOME_BUTTON)

        home_page_displayed = exists(LocalWeb.FIREFOX_IMAGE, FirefoxSettings.FIREFOX_TIMEOUT)
        assert home_page_displayed, 'The Home Page is customized'

        navigate_back()

        preferences_page_opened = exists(homepage_preferences_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert preferences_page_opened, 'The about:preferences page is successfully loaded.'

        restore_defaults_region = Region(Screen.SCREEN_WIDTH/4, 0, Screen.SCREEN_WIDTH, Screen.SCREEN_HEIGHT/4)

        restore_defaults_displayed = exists('Restore Defaults', FirefoxSettings.FIREFOX_TIMEOUT,
                                            restore_defaults_region)
        assert restore_defaults_displayed, 'The \'Restore Defaults\' button is displayed.'

        click('Restore Defaults')

        home_option_displayed = exists(default_setting_home_pattern, FirefoxSettings.FIREFOX_TIMEOUT,
                                       homepage_section_region)
        assert home_option_displayed, 'The fields beneath are automatically changed to the Default settings.'

        quit_firefox()

        firefox.start(url='', image=NavBar.HOME_BUTTON)

        home_page_displayed = exists(Utils.TOP_SITES, FirefoxSettings.FIREFOX_TIMEOUT)
        assert home_page_displayed, 'The browser opens with the about:home page displayed.'

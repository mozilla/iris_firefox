# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Current opened pages can be set as home pages',
        locale=['en-US'],
        test_case_id='2241',
        test_suite_id='143546'
    )
    def run(self, firefox):
        homepage_preferences_pattern = Pattern('homepage_preferences.png')
        default_setting_home_pattern = Pattern('default_new_tab_setting_home.png')
        custom_url_option_pattern = Pattern('custom_url_option.png')
        use_current_page_option_pattern = Pattern('use_current_page_option.png')
        use_bookmark_option_pattern = Pattern('use_bookmark_option.png')
        url_field_pattern = Pattern('url_field.png')

        navigate(LocalWeb.FIREFOX_TEST_SITE)

        test_page_opened = exists(LocalWeb.FIREFOX_LOGO, FirefoxSettings.FIREFOX_TIMEOUT)
        assert test_page_opened, 'The test page was opened'

        new_tab()

        navigate(LocalWeb.MOZILLA_TEST_SITE)

        test_page_opened = exists(LocalWeb.MOZILLA_LOGO, FirefoxSettings.FIREFOX_TIMEOUT)
        assert test_page_opened, 'The test page was opened'

        new_tab()

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

        bookmark_option_displayed = exists(url_field_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert bookmark_option_displayed, 'The \'Paste a URL... \' field is displayed.'

        url_field_location = find(url_field_pattern)

        bookmark_option_displayed = exists(use_bookmark_option_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert bookmark_option_displayed, 'The \'Use bookmark...\' button is displayed.'

        custom_option_displayed = exists(use_current_page_option_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert custom_option_displayed, 'The \'Use current pages\' button is displayed.'

        click(use_current_page_option_pattern)

        click(url_field_location)

        edit_select_all()
        copy_to_clipboard()

        time.sleep(Settings.DEFAULT_UI_DELAY)

        field_populated = get_clipboard()
        assert 'http://127.0.0.1:2000/firefox/|http://127.0.0.1:2000/mozilla/' in field_populated, \
            'The field is populated with all the URLs of the pages that are opened. The URLs are separated by \"|\"'

        navigate(LocalWeb.POCKET_TEST_SITE)

        test_page_opened = exists(LocalWeb.POCKET_TEST_SITE, FirefoxSettings.FIREFOX_TIMEOUT)
        assert test_page_opened, 'The test page was opened'

        previous_tab()

        close_tab()

        select_tab('1')

        navigate(LocalWeb.FOCUS_TEST_SITE)

        test_page_opened = exists(LocalWeb.FOCUS_IMAGE, FirefoxSettings.FIREFOX_TIMEOUT)
        assert test_page_opened, 'The test page was opened'

        quit_firefox()

        firefox.start(url='', image=NavBar.HOME_BUTTON)

        home_page_displayed = exists(LocalWeb.FIREFOX_LOGO, FirefoxSettings.FIREFOX_TIMEOUT)
        assert home_page_displayed, 'The site chosen in step 3 is now the homepage..'

        next_tab()

        home_page_displayed = exists(LocalWeb.MOZILLA_LOGO, FirefoxSettings.FIREFOX_TIMEOUT)
        assert home_page_displayed, 'The site chosen in step 3 is now the homepage..'

        next_tab()

        home_page_displayed = exists(LocalWeb.FIREFOX_LOGO, FirefoxSettings.FIREFOX_TIMEOUT)
        assert home_page_displayed, 'None of the pages opened in step 4 are displayed'

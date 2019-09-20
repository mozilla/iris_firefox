# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Home pages can be customized ',
        locale=['en-US'],
        test_case_id='2241',
        test_suite_id='161463',
        profile=Profiles.TEN_BOOKMARKS
    )
    def run(self, firefox):
        homepage_preferences_pattern = Pattern('homepage_preferences.png')

        navigate('about:preferences#home')

        preferences_page_opened = exists(homepage_preferences_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert preferences_page_opened, 'The about:preferences page is successfully loaded.'

        homepage_preferences_location = find(homepage_preferences_pattern)
        homepage_section_width, homepage_preferences_height = homepage_preferences_pattern.get_size()
        homepage_section_region = Region(homepage_preferences_location.x, homepage_preferences_location.y,
                                         homepage_section_width * 3, homepage_preferences_height)

        home_option_displayed = exists('Firefox Home', FirefoxSettings.FIREFOX_TIMEOUT, homepage_section_region)
        assert home_option_displayed, 'The options for "Home" section are displayed.'

        click('Firefox Home')

        time.sleep(Settings.DEFAULT_UI_DELAY_LONG)

        homepage_section_region = Region(homepage_preferences_location.x + homepage_section_width,
                                         homepage_preferences_location.y, homepage_section_width * 2,
                                         homepage_preferences_height * 4)

        custom_option_displayed = exists('Custom', FirefoxSettings.FIREFOX_TIMEOUT, homepage_section_region)
        assert custom_option_displayed, 'The \'Custom\' option for "Home" section is displayed.'

        click('Custom')

        time.sleep(Settings.DEFAULT_UI_DELAY_LONG)

        custom_option_displayed = exists('Paste', FirefoxSettings.FIREFOX_TIMEOUT, homepage_section_region)
        assert custom_option_displayed, 'The \'Paste a URL...\' field is displayed.'

        click('Paste')

        time.sleep(Settings.DEFAULT_UI_DELAY)

        paste(LocalWeb.FIREFOX_TEST_SITE)
        type(Key.ENTER)

        quit_firefox()

        firefox.start(url='', image=NavBar.HOME_BUTTON)

        home_page_displayed = exists(LocalWeb.FIREFOX_IMAGE, FirefoxSettings.FIREFOX_TIMEOUT)
        assert home_page_displayed, 'The site chosen in step 3 is now the homepage..'

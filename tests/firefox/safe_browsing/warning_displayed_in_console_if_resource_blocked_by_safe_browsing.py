# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description=' User could see warning in Web Console if any resource loading is blocked by Safe Browsing '
                    '(iframe, a page, image) Bug 1344645 ',
        test_case_id='50351',
        test_suite_id='69',
        locale=['en-US'],
    )
    def run(self, firefox):
        console_element_picker_pattern = Pattern('console_element_picker.png')
        testsafebrowsing_tab_pattern = Pattern('testsafebrowsing_tab.png')
        mozilla_tab_logo_pattern = Pattern('mozilla_tab_logo.png')

        home_button_displayed = exists(NavBar.HOME_BUTTON, FirefoxSettings.FIREFOX_TIMEOUT)
        assert home_button_displayed, 'The Home button displayed'

        home_button_location = find(NavBar.HOME_BUTTON)
        home_button_width, home_button_height = NavBar.HOME_BUTTON.get_size()
        tabs_region = Region(0, 0, Screen.SCREEN_WIDTH, home_button_height * 4)
        warning_frame_location = Location(home_button_location.x, home_button_location.y + home_button_height * 4)

        open_web_console()

        web_console_opened = exists(console_element_picker_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert web_console_opened, 'Web Console opened'

        console_element_picker_location = find(console_element_picker_pattern)
        console_element_picker_width, console_element_picker_height = console_element_picker_pattern.get_size()
        console_region = Region(console_element_picker_location.x, console_element_picker_location.y,
                                Screen.SCREEN_WIDTH - console_element_picker_width, console_element_picker_height * 10)

        navigate('https://www.mozilla.org/en-US/')

        mozilla_page_opened = exists(mozilla_tab_logo_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert mozilla_page_opened, 'Mozilla page opened'

        no_warnings_displayed = exists('was blocked by Safe Browsing.', FirefoxSettings.FIREFOX_TIMEOUT, console_region)
        assert no_warnings_displayed is False, 'No warning page or message'

        navigate('http://testsafebrowsing.appspot.com/s/malware_in_iframe.html')

        testsafebrowsing_page_loaded = exists(testsafebrowsing_tab_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT,
                                              tabs_region)
        assert testsafebrowsing_page_loaded, 'The testsafebrowsing page loaded'

        click(warning_frame_location)

        edit_select_all()

        edit_copy()

        text_displayed = get_clipboard().replace('\n', '').replace('\r', '')
        assert 'Visiting this website may harm your computer' in text_displayed, 'The Red warning page and warning ' \
                                                                                 'message displayed'

        console_warning_displayed = exists('The resource at “http://testsafebrowsing.appspot.com/s/malware.html” was '
                                           'blocked by Safe Browsing.', FirefoxSettings.FIREFOX_TIMEOUT, console_region)
        assert console_warning_displayed, 'The resource at “http://testsafebrowsing.appspot.com/s/malware.html” was ' \
                                          'blocked by Safe Browsing. warning message displayed'

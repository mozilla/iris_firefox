# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Firefox can be successfully set to keep cookies for a specific session',
        test_case_id='143634',
        test_suite_id='2241',
        locale=['en-US'],
        blocked_by={'id': '', 'platform': OSPlatform.ALL}
    )
    def run(self, firefox):
        reddit_tab_loaded_pattern = Pattern("reddit_tab_loaded.png")
        browser_privacy_hover_pattern = Pattern("browser_privacy_hover.png")
        manage_data_button_pattern = Pattern("manage_data_button.png")
        delete_cookies_option_pattern = Pattern("delete_cookies_checkbox.png")
        empty_dialog_pattern = Pattern("no_sites_listed_window.png")

        scroll_length = Screen.SCREEN_WIDTH // 3
        if OSHelper.is_linux():
            scroll_length = 5
        if OSHelper.is_mac():
            scroll_length = 10

        navigate("https://www.reddit.com")

        reddit_tab_loaded = exists(reddit_tab_loaded_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert reddit_tab_loaded, "Reddit site is loaded"

        navigate("about:preferences#privacy")

        browser_privacy_label_exists = exists(browser_privacy_hover_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert browser_privacy_label_exists, "Privacy page is loaded"
        hover(browser_privacy_hover_pattern)

        delete_cookies_option_found = scroll_until_pattern_found(delete_cookies_option_pattern, scroll,
                                                                 (-scroll_length,), 5)
        assert delete_cookies_option_found, "Delete cookies checkbox is found"
        click(delete_cookies_option_pattern)

        firefox.restart('about:preferences#privacy', browser_privacy_hover_pattern)

        click(NavBar.RELOAD_BUTTON)

        browser_privacy_label_exists = exists(browser_privacy_hover_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert browser_privacy_label_exists, "Privacy page is loaded"
        hover(browser_privacy_hover_pattern)

        manage_data_button_found = scroll_until_pattern_found(manage_data_button_pattern, scroll, (-scroll_length,),
                                                              timeout=1)
        assert manage_data_button_found, 'Manage data can be opened'

        time.sleep(0.5)  # to prevent clicking on wrong location due to fast execution

        manage_data_button_exists = exists(manage_data_button_pattern)
        assert manage_data_button_exists, 'Button is reached.'

        click(manage_data_button_pattern)

        empty_dialog_exists = exists(empty_dialog_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert empty_dialog_exists, "The dialog is opened and it is empty"

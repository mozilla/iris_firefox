# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description="Pop-up windows can be enabled/disabled",
        test_case_id="159259",
        test_suite_id="2241",
        locale=["en-US"],
    )
    def run(self, firefox):
        browser_privacy_hover_pattern = Pattern("browser_privacy_hover.png")
        block_popups_setting_pattern = Pattern("block_popup_settings.png")
        popup_blocked_pattern = Pattern("popups_blocked_message.png")
        facebook_login_pattern = Pattern("facebook_login_icon.png")
        facebook_login_window_pattern = Pattern("facebook_login_popup.png")
        log_in_button_pattern = Pattern("log_in_button.png")
        pinterest_tab_pattern = Pattern("pinterest_tab.png")

        scroll_length = Screen.SCREEN_WIDTH // 3
        if OSHelper.is_linux():
            scroll_length = 5
        if OSHelper.is_mac():
            scroll_length = 10

        navigate("about:preferences#privacy")

        browser_privacy_label_exists = exists(browser_privacy_hover_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert browser_privacy_label_exists, "Privacy page is loaded"
        hover(browser_privacy_hover_pattern)

        block_popups_setting_found = scroll_until_pattern_found(
            block_popups_setting_pattern, scroll, (-scroll_length,), timeout=1
        )
        assert block_popups_setting_found, "The option is selected by default."

        new_tab()

        navigate("pinterest.com")

        site_loaded = exists(pinterest_tab_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert site_loaded, "Site is loaded"

        log_in_button_exists = exists(log_in_button_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert log_in_button_exists, "Login is available"

        click(log_in_button_pattern)

        facebook_login_is_available = exists(facebook_login_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert facebook_login_is_available, "Login via facebook is available"

        click(facebook_login_pattern)

        popups_blocked_message_displayed = exists(popup_blocked_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert popups_blocked_message_displayed, (
            "A yellow banner is displayed underneath the URL bar with the "
            'message "Firefox prevented this site from opening a pop-up window"'
        )
        previous_tab()
        click(block_popups_setting_pattern)

        next_tab()
        click(NavBar.RELOAD_BUTTON)

        site_reloaded = exists(pinterest_tab_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert site_reloaded, "Site is loaded"

        log_in_button_exists = exists(log_in_button_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert log_in_button_exists, "Login is available"

        click(log_in_button_pattern)

        facebook_login_is_available = exists(facebook_login_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert facebook_login_is_available, "Login via facebook is available"

        click(facebook_login_pattern)

        popups_blocked_message_not_displayed = not exists(popup_blocked_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        login_window_opened = exists(facebook_login_window_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert popups_blocked_message_not_displayed and login_window_opened, "The sign in pop-up window is displayed."

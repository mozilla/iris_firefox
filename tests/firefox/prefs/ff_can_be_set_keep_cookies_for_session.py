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
    )
    def run(self, firefox):
        custom_level_option_pattern = Pattern("custom_level_option.png")
        drop_down_default_pattern = Pattern("default_drop_down.png")
        all_cookies_option_pattern = Pattern("all_cookies_option.png")
        reddit_tab_loaded_pattern = Pattern("reddit_tab_loaded.png")
        manage_permissions_pattern = Pattern("manage_permissions.png")
        manage_data_pattern = Pattern("manage_data_button.png")
        empty_dialog_pattern = Pattern("empty_permissions_list.png")
        allow_for_session_button_pattern = Pattern("allow_for_label_button.png")
        reddit_label_pattern = Pattern("reddit_label.png")

        scroll_step = 100
        if OSHelper.is_linux():
            scroll_step = 3
        if OSHelper.is_mac():
            scroll_step = 20

        navigate("about:preferences#privacy")

        hover_location = Location(Screen.SCREEN_WIDTH/2, Screen.SCREEN_HEIGHT/2)
        hover(hover_location)

        custom_level_option_exists = scroll_until_pattern_found(custom_level_option_pattern, scroll, (-scroll_step,), 5)
        assert custom_level_option_exists, "Custom option exists"
        time.sleep(Settings.DEFAULT_UI_DELAY_LONG)
        custom_level_option_loc = find(custom_level_option_pattern)

        click(custom_level_option_pattern)

        drop_down_default_exists = exists(drop_down_default_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert drop_down_default_exists, "Drop-down is available"

        click(drop_down_default_pattern)

        all_cookies_option_exists = exists(all_cookies_option_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert all_cookies_option_exists, "Option is present"

        click(all_cookies_option_pattern)

        new_tab()
        navigate("https://www.reddit.com")

        reddit_tab_loaded = exists(reddit_tab_loaded_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert reddit_tab_loaded, "Reddit site is loaded"

        previous_tab()

        scroll_down((-scroll_step), 5)

        manage_permissions_exists = exists(manage_permissions_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert manage_permissions_exists, "Cookies menu can be opened"

        click(manage_permissions_pattern)

        empty_dialog_exists = exists(empty_dialog_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert empty_dialog_exists, "The dialog is opened and it is empty"

        paste("https://www.reddit.com")

        allow_for_session_button = exists(allow_for_session_button_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert allow_for_session_button, "Allow for session button is active"

        click(allow_for_session_button_pattern)

        click(AboutPreferences.Privacy.Exceptions.SAVE_CHANGES_BUTTON)

        close_tab()

        click(NavBar.RELOAD_BUTTON)
        time.sleep(0.5)  # to prevent exists call before page reload

        reddit_tab_loaded = exists(reddit_tab_loaded_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert reddit_tab_loaded, "Reddit site is loaded"

        new_tab()
        navigate("about:preferences#privacy")

        hover(custom_level_option_loc)
        scroll_down((-scroll_step), 5)

        manage_data_exists = exists(manage_data_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert manage_data_exists, "Manage data button is still on the screen"

        click(manage_data_pattern)

        reddit_label_exists = exists(reddit_label_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert reddit_label_exists, "Reddit page is displayed on the list"

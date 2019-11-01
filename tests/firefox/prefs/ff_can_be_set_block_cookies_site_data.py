# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Firefox can be successfully set to block cookies and site data',
        test_case_id='143655',
        test_suite_id='2241',
        locale=['en-US'],
    )
    def run(self, firefox):
        save_changes_button_pattern = AboutPreferences.Privacy.Exceptions.SAVE_CHANGES_BUTTON

        browser_privacy_hover_pattern = Pattern('browser_privacy_hover.png')
        standard_security_level_pattern = Pattern('standard_sec_level.png')
        manage_data_button_pattern = Pattern('manage_data_button.png')
        manage_permissions_pattern = Pattern("manage_permissions.png")
        empty_dialog_pattern = Pattern("empty_permissions_list.png")
        empty_sites_pattern = Pattern("empty_site_list.png")
        block_button_pattern = Pattern("block_button.png")
        reddit_tab_loaded_pattern = Pattern("reddit_tab_loaded.png")
        remove_all_button_pattern = Pattern('remove_all_button.png')
        clear_now_dialog_button_pattern = Pattern('clear_now_button.png')
        cookies_cleared_pattern = Pattern('cookies_are_fully_cleared.png')
        reddit_label_in_list_pattern = Pattern('reddit_label_in_list.png')

        scroll_length = Screen.SCREEN_WIDTH // 3
        if OSHelper.is_linux():
            scroll_length = 5
        if OSHelper.is_mac():
            scroll_length = 10

        navigate('about:preferences#privacy')

        browser_privacy_label_exists = exists(browser_privacy_hover_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert browser_privacy_label_exists, "Privacy page is loaded"

        standard_security_level_exists = exists(standard_security_level_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert standard_security_level_exists, "The option \"Standard\" is set"

        hover(browser_privacy_hover_pattern)

        manage_data_button_found = scroll_until_pattern_found(manage_data_button_pattern, scroll, (-scroll_length,),
                                                              timeout=1)
        assert manage_data_button_found, 'Manage data can be opened'

        time.sleep(Settings.DEFAULT_UI_DELAY)  # to prevent clicking on wrong location due to fast execution
        click(manage_data_button_pattern)

        empty_dialog_exists = not exists(empty_sites_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert empty_dialog_exists, "The dialog is opened and it is contains only addons site"

        type(Key.ESC)  # dismiss current window

        manage_permissions_exists = exists(manage_permissions_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert manage_permissions_exists, "Cookies menu can be opened"

        click(manage_permissions_pattern)

        empty_dialog_exists = exists(empty_dialog_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert empty_dialog_exists, "The dialog is opened and it is not empty"

        paste("https://www.reddit.com")

        block_button_exists = exists(block_button_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert block_button_exists, "Permission for site can be denied"

        click(block_button_pattern)
        click(save_changes_button_pattern)

        new_tab()
        navigate("https://www.reddit.com")

        reddit_tab_loaded = exists(reddit_tab_loaded_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert reddit_tab_loaded, "Reddit site is loaded"

        previous_tab()
        click(NavBar.RELOAD_BUTTON)
        hover(browser_privacy_hover_pattern)

        manage_data_button_found = scroll_until_pattern_found(manage_data_button_pattern, scroll, (-scroll_length,),
                                                              timeout=1)
        assert manage_data_button_found, 'Manage data can be opened'

        time.sleep(Settings.DEFAULT_UI_DELAY)  # to prevent clicking on wrong location due to fast execution
        click(manage_data_button_pattern)

        reddit_label_not_in_list = not exists(reddit_label_in_list_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert reddit_label_not_in_list, "https://www.reddit.com/ is NOT displayed on that list"

        remove_all_button_exists = exists(remove_all_button_pattern)
        assert remove_all_button_exists, "Remove all button is present"

        click(remove_all_button_pattern)

        try:
            all_records_deleted = wait_vanish(reddit_label_in_list_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
            assert all_records_deleted, "All records was successfully deleted"
        except FindError:
            raise

        save_changes_button_exists = exists(save_changes_button_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert save_changes_button_exists, 'Save button is shown'

        click(save_changes_button_pattern)

        confirmation_dialog_exists = exists(clear_now_dialog_button_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert confirmation_dialog_exists, "Clear all cookies and site data pop-up is displayed"

        type(Key.ENTER)  # accept cookies clearing

        cookies_are_cleared = exists(cookies_cleared_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert cookies_are_cleared, "All the cookies and site data are deleted."

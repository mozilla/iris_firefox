# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Cookies and Site Data can be managed via the "Managed Cookies and Site Data" panel.',
        test_case_id='143633',
        test_suite_id='2241',
        locale=['en-US'],
    )
    def run(self, firefox):
        manage_data_button_pattern = Pattern('manage_data_button.png')
        manage_cookies_dialog_title_pattern = Pattern('manage_cookies_title.png')
        site_with_cookies_pattern = Pattern('site_with_cookies.png')
        remove_button_highlighted_pattern = Pattern('remove_button_highlighted.png')
        remove_all_button_pattern = Pattern('remove_all_button.png')
        clear_now_dialog_button_pattern = Pattern('clear_now_button.png')
        save_changes_button_pattern = Pattern('save_changes_button.png')
        cookies_cleared_pattern = Pattern('cookies_are_fully_cleared.png')
        scroll_length = Screen.SCREEN_WIDTH // 3

        navigate('about:preferences#privacy')

        manage_data_button_found = scroll_until_pattern_found(manage_data_button_pattern, scroll, (-scroll_length,),
                                                              timeout=Settings.DEFAULT_AUTO_WAIT_TIMEOUT)
        assert manage_data_button_found, 'Manage data can be opened'

        manage_data_button_exists = exists(manage_data_button_pattern)
        assert manage_data_button_exists, 'Button is reached.'

        click(manage_data_button_pattern, Settings.DEFAULT_CLICK_DELAY)

        manage_cookies_dialog_opened = exists(manage_cookies_dialog_title_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert manage_cookies_dialog_opened, 'The "Manage Cookies and Site Data" subdialog opened.'

        site_with_cookies_pattern_exists = exists(site_with_cookies_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert site_with_cookies_pattern_exists, "The site is highlighted."

        click(site_with_cookies_pattern)

        remove_button_highlighted = exists(remove_button_highlighted_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert remove_button_highlighted, "Remove button highlighted after click"

        remove_all_button_exists = exists(remove_all_button_pattern)
        assert remove_all_button_exists, "Remove all button is present"

        click(remove_all_button_pattern)

        try:
            all_records_deleted = wait_vanish(site_with_cookies_pattern, Settings.DEFAULT_AUTO_WAIT_TIMEOUT)
            assert all_records_deleted, "All records was successfully deleted"
        except FindError:
            raise

        save_changes_button_exists = exists(save_changes_button_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert save_changes_button_exists, 'Save button is shown'

        click(save_changes_button_pattern)

        confirmation_dialog_exists = exists(clear_now_dialog_button_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert confirmation_dialog_exists, "Clear all cookies and site data pop-up is displayed"

        click(clear_now_dialog_button_pattern)

        cookies_are_cleared = exists(cookies_cleared_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert cookies_are_cleared, "All the cookies and site data are deleted."
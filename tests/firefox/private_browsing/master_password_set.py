# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Master Password can be set in Private Browsing',
        test_case_id='101671',
        test_suite_id='1826',
        locale=['en-US'],
    )
    def run(self, firefox):
        change_master_password_popup_pattern = Pattern('change_master_password_popup.png')
        preferences_privacy_find_field_pattern = Pattern('preferences_privacy_find_field.png').similar(0.6)
        master_password_box_is_checked_pattern = Pattern('master_password_box_is_checked.png')
        master_password_box_is_unchecked_pattern = Pattern('master_password_box_is_unchecked.png')
        ok_button_available_in_change_master_password_pattern = \
            Pattern('ok_button_available_in_change_master_password.png')
        button_ok_password_change_succeeded_pattern = Pattern('button_ok_password_change_succeeded.png')
        password_change_succeeded_pattern = Pattern('password_change_succeeded.png')
        remove_button_available_in_change_master_password_pattern = \
            Pattern('remove_button_available_in_change_master_password_pattern.png')
        master_password_deleted_pattern = Pattern('master_password_deleted.png')
        remove_master_password_popup_pattern = Pattern('remove_master_password_popup.png')

        new_private_window()

        private_window_is_loaded = exists(PrivateWindow.private_window_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert private_window_is_loaded is True, 'Private windows is loaded'

        navigate('about:preferences#privacy')

        navigated_to_preferences = exists(preferences_privacy_find_field_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert navigated_to_preferences is True, 'Preferences/privacy page successfully loaded.'

        paste('Use a master password')

        unchecked_use_master_password_checkbox_exists = exists(master_password_box_is_unchecked_pattern,
                                                               FirefoxSettings.FIREFOX_TIMEOUT)
        assert unchecked_use_master_password_checkbox_exists is True, 'Master Password checkbox is unchecked.'

        click(master_password_box_is_unchecked_pattern)

        change_master_password_popup = exists(change_master_password_popup_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert change_master_password_popup is True, 'Master password popup exist'

        type('123')
        type(Key.TAB)
        type('123')

        ok_button_available_in_change_master_password = \
            exists(ok_button_available_in_change_master_password_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert ok_button_available_in_change_master_password is True, 'Button OK is available'

        hover(ok_button_available_in_change_master_password_pattern)
        click(ok_button_available_in_change_master_password_pattern)

        password_change_succeeded = exists(password_change_succeeded_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert password_change_succeeded, 'Password change succeeded.'

        available_button_ok_password_change_succeeded = exists(button_ok_password_change_succeeded_pattern,
                                                               FirefoxSettings.FIREFOX_TIMEOUT)
        #  location to prevent multiple occurrences of OK button
        assert available_button_ok_password_change_succeeded is True, 'Button OK is available.'

        type(Key.ENTER)

        master_password_box_is_checked = exists(master_password_box_is_checked_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert master_password_box_is_checked is True, 'Master password checkbox is checked'

        close_window()

        #  enter normal mode
        new_tab()

        new_tab_is_opened = exists(Tabs.NEW_TAB_HIGHLIGHTED, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert new_tab_is_opened is True, 'New tab is opened'

        navigate('about:preferences#privacy')

        navigated_to_preferences = exists(preferences_privacy_find_field_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert navigated_to_preferences is True, 'Preferences/privacy page successfully loaded.'

        paste('Use a Master Password')

        checked_use_master_password_checkbox_exists = exists(master_password_box_is_checked_pattern,
                                                             FirefoxSettings.FIREFOX_TIMEOUT)
        assert checked_use_master_password_checkbox_exists is True, 'Master Password checkbox is unchecked.'

        click(master_password_box_is_checked_pattern)

        #  deactivate master password
        remove_master_password_popup = exists(remove_master_password_popup_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert remove_master_password_popup is True, 'Master password popup exist'

        type('123')
        type(Key.TAB)

        remove_button_available_in_change_master_password = \
            exists(remove_button_available_in_change_master_password_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert remove_button_available_in_change_master_password is True, 'Button remove is available'

        hover(remove_button_available_in_change_master_password_pattern)
        click(remove_button_available_in_change_master_password_pattern)

        master_password_deleted = exists(master_password_deleted_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert master_password_deleted is True, 'Master password deleted.'

        available_button_ok_password_change_succeeded = exists(button_ok_password_change_succeeded_pattern,
                                                               FirefoxSettings.FIREFOX_TIMEOUT)
        assert available_button_ok_password_change_succeeded is True, 'Button OK is available.'

        hover(button_ok_password_change_succeeded_pattern)
        click(button_ok_password_change_succeeded_pattern)

        unchecked_use_master_password_checkbox_exists = exists(master_password_box_is_unchecked_pattern,
                                                               FirefoxSettings.FIREFOX_TIMEOUT)
        assert unchecked_use_master_password_checkbox_exists is True, 'Master Password checkbox is unchecked.'

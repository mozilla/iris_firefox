# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Master Password can be removed using Private Browsing',
        test_case_id='101672',
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
        private_browsing_tab_logo_pattern = Pattern('private_browsing_tab_logo.png')
        remove_master_password_popup_pattern = Pattern('remove_master_password_popup.png')

        #  set master password in normal mode
        new_tab()

        new_tab_is_opened = exists(Tabs.NEW_TAB_HIGHLIGHTED, FirefoxSettings.FIREFOX_TIMEOUT)
        assert new_tab_is_opened is True, 'New tab is opened'

        navigate('about:preferences#privacy')

        navigated_to_preferences = exists(preferences_privacy_find_field_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert navigated_to_preferences is True, 'Preferences/privacy page successfully loaded.'

        paste('Use a Master Password')

        unchecked_use_master_password_checkbox_exists = exists(master_password_box_is_unchecked_pattern,
                                                               FirefoxSettings.FIREFOX_TIMEOUT)
        assert unchecked_use_master_password_checkbox_exists is True, 'Master Password checkbox is unchecked.'

        click(master_password_box_is_unchecked_pattern)

        #  deactivate master password
        change_master_password_popup = exists(change_master_password_popup_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert change_master_password_popup is True, 'Master password popup exist'

        type('123')
        type(Key.TAB)
        type('123')

        ok_button_available_in_change_master_password = exists(ok_button_available_in_change_master_password_pattern,
                                                               FirefoxSettings.FIREFOX_TIMEOUT)
        assert ok_button_available_in_change_master_password is True, 'Button OK is available'

        click(ok_button_available_in_change_master_password_pattern)

        password_change_succeeded = exists(password_change_succeeded_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert password_change_succeeded is True, 'Password change succeeded.'

        available_button_ok_password_change_succeeded = exists(button_ok_password_change_succeeded_pattern,
                                                               FirefoxSettings.FIREFOX_TIMEOUT)
        assert available_button_ok_password_change_succeeded is True, 'Button OK is available.'

        type(Key.ENTER)

        master_password_box_is_checked = exists(master_password_box_is_checked_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert master_password_box_is_checked is True, 'Master password is set in Normal Browsing tab.'

        #  Change master password in Private mode
        new_private_window()

        private_browsing_tab_logo = exists(private_browsing_tab_logo_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert private_browsing_tab_logo is True, 'A new private window is successfully loaded.'

        navigate('about:preferences#privacy')

        navigated_to_preferences = exists(preferences_privacy_find_field_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert navigated_to_preferences is True, 'Preferences/privacy page successfully loaded.'

        click(preferences_privacy_find_field_pattern)

        paste('Use a master password')

        checked_use_master_password_checkbox_exists = exists(master_password_box_is_checked_pattern,
                                                             FirefoxSettings.FIREFOX_TIMEOUT)
        assert checked_use_master_password_checkbox_exists is True, 'Master Password checkbox is checked.'

        click(master_password_box_is_checked_pattern)

        #  remove Master password in Private mode
        remove_master_password_popup = exists(remove_master_password_popup_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert remove_master_password_popup is True, 'Master password popup exist'

        type('123')
        type(Key.TAB)

        remove_button_available_in_change_master_password = \
            exists(remove_button_available_in_change_master_password_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert remove_button_available_in_change_master_password is True, 'Button remove is available'

        click(remove_button_available_in_change_master_password_pattern)

        master_password_deleted = exists(master_password_deleted_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert master_password_deleted is True, 'Master password deleted.'

        available_button_ok_password_change_succeeded = exists(button_ok_password_change_succeeded_pattern,
                                                               FirefoxSettings.FIREFOX_TIMEOUT)
        assert available_button_ok_password_change_succeeded is True, 'Button OK is available.'

        click(button_ok_password_change_succeeded_pattern)

        unchecked_use_master_password_checkbox_exists = exists(master_password_box_is_unchecked_pattern,
                                                               FirefoxSettings.FIREFOX_TIMEOUT)
        assert unchecked_use_master_password_checkbox_exists is True, 'Master Password checkbox is ' \
                                                                      'unchecked in Private Browsing tab.'

        close_window()

        #  access preferences from Normal Browsing tab
        new_tab()

        new_tab_is_opened = exists(Tabs.NEW_TAB_HIGHLIGHTED, FirefoxSettings.FIREFOX_TIMEOUT)
        assert new_tab_is_opened is True, 'New tab is opened'

        navigate('about:preferences#privacy')

        navigated_to_preferences = exists(preferences_privacy_find_field_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert navigated_to_preferences is True, 'Preferences/privacy page successfully loaded.'

        paste('Use a Master Password')

        unchecked_use_master_password_checkbox_exists = exists(master_password_box_is_unchecked_pattern,
                                                               FirefoxSettings.FIREFOX_TIMEOUT)
        assert unchecked_use_master_password_checkbox_exists is True, 'Master Password checkbox is ' \
                                                                      'unchecked in Normal Browsing tab.'

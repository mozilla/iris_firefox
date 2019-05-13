# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):
    def __init__(self):
        BaseTest.__init__(self)
        self.meta = '[1427248] Set prefs do not cause the master password to be disabled after reset.'
        self.test_case_id = '245730'
        self.test_suite_id = '3063'
        self.locale = ['en-US']

    def run(self):
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
        form_address = self.get_asset_path('form.html')

        navigate('about:preferences#privacy')

        navigated_to_preferences = exists(preferences_privacy_find_field_pattern, 20)
        assert_true(self, navigated_to_preferences, 'Preferences/privacy page successfully loaded.')

        paste('Use a master password')

        unchecked_use_master_password_checkbox_exists = exists(master_password_box_is_unchecked_pattern, 20)
        assert_true(self, unchecked_use_master_password_checkbox_exists, 'Master Password checkbox is unchecked.')

        hover(master_password_box_is_unchecked_pattern, 0.2)

        click(master_password_box_is_unchecked_pattern)

        change_master_password_popup = exists(change_master_password_popup_pattern, 20)
        assert_true(self, change_master_password_popup, 'Master password popup exist')

        type('123')
        type(Key.TAB)
        type('123')

        ok_button_available_in_change_master_password = \
            exists(ok_button_available_in_change_master_password_pattern, 30)
        assert_true(self, ok_button_available_in_change_master_password, 'Button OK is available')

        hover(ok_button_available_in_change_master_password_pattern, 0.2)

        click(ok_button_available_in_change_master_password_pattern)

        password_change_succeeded = exists(password_change_succeeded_pattern, 20)
        assert_true(self, password_change_succeeded, 'Password change succeeded.')

        available_button_ok_password_change_succeeded = exists(button_ok_password_change_succeeded_pattern, 30)
        #  location to prevent multiple occurrences of OK button
        assert_true(self, available_button_ok_password_change_succeeded, 'Button OK is available.')

        type(Key.ENTER)

        master_password_box_is_checked = exists(master_password_box_is_checked_pattern, 30)
        assert_true(self, master_password_box_is_checked, 'Master password checkbox is checked')


        time.sleep(1234)

        # deactivate
        navigate('about:preferences#privacy')

        navigated_to_preferences = exists(preferences_privacy_find_field_pattern, 20)
        assert_true(self, navigated_to_preferences, 'Preferences/privacy page successfully loaded.')

        paste('Use a Master Password')

        checked_use_master_password_checkbox_exists = exists(master_password_box_is_checked_pattern, 20)
        assert_true(self, checked_use_master_password_checkbox_exists, 'Master Password checkbox is unchecked.')

        hover(master_password_box_is_checked_pattern, 0.2)

        click(master_password_box_is_checked_pattern)




        #  deactivate master password
        change_master_password_popup = exists(change_master_password_popup_pattern, 20)
        assert_true(self, change_master_password_popup, 'Master password popup exist')

        type('123')
        type(Key.TAB)

        remove_button_available_in_change_master_password = \
            exists(remove_button_available_in_change_master_password_pattern, 30)
        assert_true(self, remove_button_available_in_change_master_password, 'Button remove is available')

        hover(remove_button_available_in_change_master_password_pattern, 0.2)

        click(remove_button_available_in_change_master_password_pattern)

        master_password_deleted = exists(master_password_deleted_pattern, 20)
        assert_true(self, master_password_deleted, 'Master password deleted.')

        available_button_ok_password_change_succeeded = exists(button_ok_password_change_succeeded_pattern, 30)
        assert_true(self, available_button_ok_password_change_succeeded, 'Button OK is available.')

        hover(button_ok_password_change_succeeded_pattern, 0.2)

        click(button_ok_password_change_succeeded_pattern)

        unchecked_use_master_password_checkbox_exists = exists(master_password_box_is_unchecked_pattern, 20)
        assert_true(self, unchecked_use_master_password_checkbox_exists, 'Master Password checkbox is unchecked.')

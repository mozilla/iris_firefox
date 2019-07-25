# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description='[1427248] Set prefs do not cause the master password to be disabled after reset.',
        locale=['en-US'],
        test_case_id='245730',
        test_suite_id='3063'
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
        name_form_pattern = Pattern('name_form.png')
        password_form_pattern = Pattern('password_form.png').similar(.6)
        save_login_button_pattern = Pattern('save_login_button.png')
        saved_logins_button_pattern = Pattern('saved_logins_button.png')
        saved_logins_list_available_pattern = Pattern('saved_logins_list_available.png')
        master_password_required_popup_pattern = Pattern('master_password_required_popup.png')
        remove_master_password_popup_pattern = Pattern('remove_master_password_popup.png')

        test_form_1 = self.get_asset_path('test_1_sign_in.htm')
        test_form_2 = self.get_asset_path('test_2_sign_in.htm')

        if OSHelper.is_linux():
            scroll_length = -10
        else:
            scroll_length = -25

        change_preference('signon.autofillForms', 'false')  # prevent autocomplete in site #2

        # saving password for site #1
        navigate(test_form_1)

        name_form_displayed = exists(name_form_pattern)
        assert name_form_displayed, 'Test form #1 displayed.'

        click(name_form_pattern)

        paste('user1')

        restore_firefox_focus()

        password_form_displayed = exists(password_form_pattern)
        assert password_form_displayed, 'The website is successfully displayed.'

        click(password_form_pattern)

        paste('test')
        type(Key.ENTER)

        save_login_button_available = exists(save_login_button_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert save_login_button_available, 'Save login button is available'

        click(save_login_button_pattern, 1)

        # saving password for site #2
        navigate(test_form_2)

        name_form_displayed = exists(name_form_pattern)
        assert name_form_displayed, 'Test form #2 displayed.'

        click(name_form_pattern)

        paste('user2')

        restore_firefox_focus()

        password_form_displayed = exists(password_form_pattern)
        assert password_form_displayed, 'The website is successfully displayed.'

        click(password_form_pattern)

        paste('test')
        type(Key.ENTER)

        save_login_button_available = exists(save_login_button_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert save_login_button_available, 'Save login button is available'

        click(save_login_button_pattern, 1)

        navigate('about:preferences#privacy')

        navigated_to_preferences = exists(preferences_privacy_find_field_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert navigated_to_preferences, 'Preferences/privacy page successfully loaded.'

        paste('Use a master password')

        unchecked_use_master_password_checkbox_exists = exists(master_password_box_is_unchecked_pattern,
                                                               FirefoxSettings.FIREFOX_TIMEOUT)
        assert unchecked_use_master_password_checkbox_exists, 'Master Password checkbox is unchecked.'

        hover(master_password_box_is_unchecked_pattern)

        click(master_password_box_is_unchecked_pattern)

        change_master_password_popup = exists(change_master_password_popup_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert change_master_password_popup, 'Master password popup exist'

        type('123')
        type(Key.TAB)
        type('123')

        ok_button_available_in_change_master_password = \
            exists(ok_button_available_in_change_master_password_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert ok_button_available_in_change_master_password, 'Button OK is available'

        hover(ok_button_available_in_change_master_password_pattern)

        click(ok_button_available_in_change_master_password_pattern)

        password_change_succeeded = exists(password_change_succeeded_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert password_change_succeeded, 'Password change succeeded.'

        available_button_ok_password_change_succeeded = exists(button_ok_password_change_succeeded_pattern,
                                                               FirefoxSettings.FIREFOX_TIMEOUT)
        assert available_button_ok_password_change_succeeded, 'Button OK is available.'

        type(Key.ENTER)

        master_password_box_is_checked = exists(master_password_box_is_checked_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert master_password_box_is_checked, 'Master password checkbox is checked'

        change_preference('security.enterprise_roots.enabled', 'true')

        firefox.restart(url='about:preferences#privacy',
                        image=LocalWeb.ABOUT_PREFERENCES_PRIVACY_ADDRESS)

        saved_logins_button_exists = scroll_until_pattern_found(saved_logins_button_pattern, Mouse().scroll,
                                                                (0, scroll_length,), 30, 1)
        assert saved_logins_button_exists, 'Saved logins button exists'

        click(saved_logins_button_pattern, 1)

        enter_master_password = exists(master_password_required_popup_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert enter_master_password, 'Enter master password successfully loaded.'

        type('123')
        type(Key.ENTER)

        saved_logins_list_available = exists(saved_logins_list_available_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert saved_logins_list_available, 'All saved logins are displayed.'

        change_preference('security.enterprise_roots.enabled', 'false')

        firefox.restart(url='about:preferences#privacy',
                        image=LocalWeb.ABOUT_PREFERENCES_PRIVACY_ADDRESS)

        scroll_until_pattern_found(saved_logins_button_pattern, scroll, (scroll_length,), 30, 1)

        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)

        saved_logins_button_exists = exists(saved_logins_button_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert saved_logins_button_exists, 'Saved logins button exists'

        click(saved_logins_button_pattern, 1)

        enter_master_password = exists(master_password_required_popup_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert enter_master_password, 'Enter master password successfully loaded.'

        type('123')
        type(Key.ENTER)

        saved_logins_list_available = exists(saved_logins_list_available_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert saved_logins_list_available, 'All saved logins are displayed.'

        type(Key.ESC)

        # deactivate
        new_tab()
        navigate('about:preferences#privacy')

        navigated_to_preferences = exists(preferences_privacy_find_field_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert navigated_to_preferences, 'Preferences/privacy page successfully loaded.'

        paste('Use a Master Password')

        checked_use_master_password_checkbox_exists = exists(master_password_box_is_checked_pattern,
                                                             FirefoxSettings.FIREFOX_TIMEOUT)
        assert checked_use_master_password_checkbox_exists, 'Master Password checkbox is unchecked.'

        click(master_password_box_is_checked_pattern)

        #  deactivate master password
        remove_master_password_popup = exists(remove_master_password_popup_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert remove_master_password_popup is True, 'Master password popup exist'

        type('123')
        type(Key.TAB)

        remove_button_available_in_change_master_password = \
            exists(remove_button_available_in_change_master_password_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert remove_button_available_in_change_master_password, 'Button remove is available'

        hover(remove_button_available_in_change_master_password_pattern)

        click(remove_button_available_in_change_master_password_pattern)

        master_password_deleted = exists(master_password_deleted_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert master_password_deleted, 'Master password deleted.'

        available_button_ok_password_change_succeeded = exists(button_ok_password_change_succeeded_pattern,
                                                               FirefoxSettings.FIREFOX_TIMEOUT)
        assert available_button_ok_password_change_succeeded, 'Button OK is available.'

        hover(button_ok_password_change_succeeded_pattern)

        click(button_ok_password_change_succeeded_pattern)

        unchecked_use_master_password_checkbox_exists = exists(master_password_box_is_unchecked_pattern,
                                                               FirefoxSettings.FIREFOX_TIMEOUT)
        assert unchecked_use_master_password_checkbox_exists, 'Master Password checkbox is unchecked.'

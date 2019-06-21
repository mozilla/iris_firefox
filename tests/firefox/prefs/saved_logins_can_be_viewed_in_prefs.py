# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Saved logins can be successfully viewed via the "Saved logins" panel',
        locale=['en-US'],
        test_case_id='143602',
        test_suite_id='2241',
    )
    def run(self, firefox):
        name_field_pattern = Pattern('name_field.png')
        password_field_pattern = Pattern('password_field.png')
        save_login_button_pattern = Pattern('save_login_button.png')
        saved_logins_button_pattern = Pattern('saved_logins_button.png')
        first_saved_login_pattern = Pattern('name0_login.png').similar(0.95)
        last_saved_login_pattern = Pattern('name9_login.png').similar(0.95)
        login_form = self.get_asset_path('form.html')
        ui_timeout = 1

        scroll_length = Screen.SCREEN_HEIGHT // 10
        if OSHelper.is_linux():
            scroll_length = 3
        elif OSHelper.is_mac():
            scroll_length = 5

        navigate(login_form)

        for i in range(10):
            name_field_located = exists(name_field_pattern)
            assert name_field_located, 'Name field is located'

            click(name_field_pattern)
            edit_select_all()
            paste(f'name{i}')

            password_field_located = exists(password_field_pattern)
            assert password_field_located, 'Password field is located'

            if OSHelper.is_linux():
                type(Key.TAB)
            else:
                click(password_field_pattern)
            edit_select_all()
            paste(f'password{i}')

            type(Key.ENTER)

            save_login_popup_appeared = exists(save_login_button_pattern)
            assert save_login_popup_appeared, '"Save login" popup appeared'

            click(save_login_button_pattern)

        navigate('about:preferences#privacy')
        preferences_opened = exists(AboutPreferences.PRIVACY_AND_SECURITY_BUTTON_SELECTED)
        assert preferences_opened, 'The about:preferences page is successfully loaded.'

        saved_logins_button_displayed = scroll_until_pattern_found(saved_logins_button_pattern, scroll,
                                                                   (-scroll_length,), timeout=ui_timeout)
        assert saved_logins_button_displayed, 'Saved logins button is displayed'

        click(saved_logins_button_pattern)

        saved_logins_opened = exists(first_saved_login_pattern)
        assert saved_logins_opened, 'Saved logins sub-window is opened. The list is successfully populated'

        hover(first_saved_login_pattern)
        all_logins_saved = scroll_until_pattern_found(last_saved_login_pattern, scroll, (-scroll_length,))
        assert all_logins_saved, 'All logins are saved and may be scrolled'

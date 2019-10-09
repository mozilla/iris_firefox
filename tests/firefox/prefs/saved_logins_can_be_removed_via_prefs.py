# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description='Saved logins can be successfully removed via the "Saved logins" panel',
        locale=["en-US"],
        test_case_id="148535",
        test_suite_id="2241",
    )
    def run(self, firefox):
        name_field_pattern = Pattern("name_field.png")
        password_field_pattern = Pattern("password_field.png")
        save_login_button_pattern = Pattern("save_login_button.png")
        saved_logins_button_pattern = Pattern("saved_logins_button.png")
        first_saved_login_pattern = Pattern("name0_login.png").similar(0.95)
        last_saved_login_pattern = Pattern("name9_login.png").similar(0.95)
        remove_password_pattern = Pattern("remove_password.png")
        remove_confirm_pattern = Pattern("remove_confirmation.png")
        login_form = self.get_asset_path("form.html")

        navigate(login_form)
        name_field_displayed = exists(
            name_field_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert name_field_displayed, "Login form is opened"

        click(name_field_pattern)

        paste("name0")

        password_field_displayed = exists(password_field_pattern)
        assert password_field_displayed, "Password field is reachable"

        click(password_field_pattern)

        paste("password0")
        type(Key.ENTER)

        save_login_button_appeared = exists(save_login_button_pattern)
        assert save_login_button_appeared, '"Save login" button appeared'

        click(save_login_button_pattern)

        name_field_displayed = exists(
            name_field_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert name_field_displayed, "Login form is opened"

        click(name_field_pattern)

        paste("name9")

        password_field_displayed = exists(password_field_pattern)
        assert password_field_displayed, "Password field is reachable"

        click(password_field_pattern)

        paste("password9")
        type(Key.ENTER)

        save_login_button_appeared = exists(save_login_button_pattern)
        assert save_login_button_appeared, '"Save login" button appeared'

        click(save_login_button_pattern)

        navigate("about:preferences#privacy")
        preferences_opened = exists(
            AboutPreferences.PRIVACY_AND_SECURITY_BUTTON_SELECTED
        )
        assert preferences_opened, "The about:preferences page is successfully loaded."

        type(Key.TAB)  # change focus for correct scroll

        saved_logins_button_displayed = scroll_until_pattern_found(
            saved_logins_button_pattern,
            type,
            (Key.DOWN,),
            50,
            timeout=FirefoxSettings.TINY_FIREFOX_TIMEOUT // 2,
        )
        assert saved_logins_button_displayed, "Saved logins button is displayed"

        time.sleep(Settings.DEFAULT_UI_DELAY_LONG * 2)

        saved_logins_exists = exists(
            saved_logins_button_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert saved_logins_exists, "Saved logins button is fixed after scroll."

        saved_logins_location = find(saved_logins_button_pattern)

        saved_click_location = Location(
            saved_logins_location.x + 5, saved_logins_location.y + 5
        )

        click(saved_click_location)

        saved_logins_opened = exists(first_saved_login_pattern.similar(0.7))
        assert (
            saved_logins_opened
        ), "Saved logins sub-window is opened. The list is successfully populated"

        second_login_saved = exists(last_saved_login_pattern.similar(0.7))
        assert (
            second_login_saved
        ), "Second login was saved. The list is successfully populated. "

        credentials_can_be_removed = exists(remove_password_pattern)
        assert credentials_can_be_removed, '"Remove" button is reachable'

        click(remove_password_pattern)

        confirmation_window_available = exists(
            remove_confirm_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert confirmation_window_available, "Entry can be removed"

        click(remove_confirm_pattern)

        close_tab()

        saved_logins_button_displayed = exists(saved_logins_button_pattern)
        assert saved_logins_button_displayed, "Saved logins button is displayed"

        click(saved_logins_button_pattern)

        time.sleep(FirefoxSettings.SHORT_FIREFOX_TIMEOUT)

        last_login_not_deleted = exists(last_saved_login_pattern)
        assert last_login_not_deleted, "Last login was not deleted"

        first_login_deleted = wait_vanish(
            first_saved_login_pattern.exact(), FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert first_login_deleted, "Login was successfully deleted"

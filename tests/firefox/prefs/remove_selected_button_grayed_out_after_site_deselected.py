# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description="The 'Remove Selected' button is not grayed out after a website is deselected.",
        test_case_id="145301",
        test_suite_id="2241",
        locale=["en-US"],
        blocked_by={"id": "4504", "platform": [OSPlatform.WINDOWS, OSPlatform.MAC]},
    )
    def run(self, firefox):
        manage_data_button = Pattern("manage_data_button_highlighted.png")
        manage_cookies_and_site_data_pop_up = Pattern("manage_cookies_and_site_data_pop_up.png")
        select_a_site_from_manage_data_pop_up = Pattern("select_a_site_from_manage_data_pop_up.png")
        remove_selected_button_disabled = Pattern("remove_selected_button_disabled.png")
        remove_selected_button_enabled = Pattern("remove_selected_button_enabled.png")
        cancel_button_manage_cookies_site_data = Pattern("cancel_button_manage_cookies_site_data.png")
        site_column_in_site_data = Pattern("site_column_in_site_data.png")

        navigate("about:preferences")
        page_loaded = exists(AboutPreferences.PRIVACY_AND_SECURITY_BUTTON_NOT_SELECTED, FirefoxSettings.FIREFOX_TIMEOUT)
        assert page_loaded, "about:preferences page couldn't loaded."

        click(AboutPreferences.FIND_IN_OPTIONS)
        paste('Manage Data')

        manage_data_button_exists = exists(manage_data_button, FirefoxSettings.FIREFOX_TIMEOUT)
        assert manage_data_button_exists, "manage data button not found in #aboutpreference's search result."

        click(manage_data_button, duration=1)
        manage_cookies_and_site_data_pop_up_exists = exists(manage_cookies_and_site_data_pop_up,
                                                            FirefoxSettings.FIREFOX_TIMEOUT)
        assert manage_cookies_and_site_data_pop_up_exists, "Manage Cookies and Site Data pop-up couldn't be displayed."

        remove_selected_button_location = find(remove_selected_button_disabled)
        remove_selected_button_width, remove_selected_button_height = remove_selected_button_disabled.get_size()

        remove_selected_button_region = Region(
            remove_selected_button_location.x - remove_selected_button_width / 8,
            remove_selected_button_location.y - remove_selected_button_height / 4,
            remove_selected_button_width * 1.25,
            remove_selected_button_height * 1.5
        )

        self.verify_remove_selected_button_is_disabled(remove_selected_button_disabled,
                                                       select_a_site_from_manage_data_pop_up)
        click(select_a_site_from_manage_data_pop_up)

        remove_selected_button_enabled_exists = exists(remove_selected_button_enabled,
                                                       FirefoxSettings.TINY_FIREFOX_TIMEOUT,
                                                       region=remove_selected_button_region)
        assert remove_selected_button_enabled_exists, "Remove Selected button couldn't be enabled."

        # Verifying "Remove Selected" button enabled
        click(remove_selected_button_enabled)
        selected_site_could_not_be_removed = exists(select_a_site_from_manage_data_pop_up,
                                                    FirefoxSettings.FIREFOX_TIMEOUT)
        assert selected_site_could_not_be_removed is False, \
            "Selected Site couldn't removed as 'Remove Selected' button is not enabled."

        # Close and reopen site data
        click(cancel_button_manage_cookies_site_data)
        manage_data_button_exists = exists(manage_data_button, FirefoxSettings.FIREFOX_TIMEOUT)
        assert manage_data_button_exists, "manage data button not found in #aboutpreference's search result."
        click(manage_data_button,duration=1)
        manage_cookies_and_site_data_pop_up_exists = exists(manage_cookies_and_site_data_pop_up,
                                                            FirefoxSettings.FIREFOX_TIMEOUT)
        assert manage_cookies_and_site_data_pop_up_exists, "Manage Cookies and Site Data pop-up couldn't be displayed."
        click(select_a_site_from_manage_data_pop_up)
        click(site_column_in_site_data)

        self.verify_remove_selected_button_is_disabled(remove_selected_button_disabled,
                                                       select_a_site_from_manage_data_pop_up)

    @staticmethod
    def verify_remove_selected_button_is_disabled(remove_selected_button_disabled,
                                                  select_a_site_from_manage_data_pop_up):
        """ Check if "Remove Selected" button is disabled - Click on Remove Selected disabled button,
            selected site couldn't be deleted. Hence button is disabled.

            :param remove_selected_button_disabled: String or Pattern.
            :param select_a_site_from_manage_data_pop_up: String or Pattern.
            :return: None.
            """
        click(remove_selected_button_disabled)
        selected_site_could_not_be_removed = exists(select_a_site_from_manage_data_pop_up,
                                                    FirefoxSettings.FIREFOX_TIMEOUT)
        assert selected_site_could_not_be_removed, "Selected Site removed as 'Remove Selected' button is not disabled."

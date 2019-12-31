# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description="Firefox Home Content - Search bar can be enabled/disabled",
        test_case_id="161665",
        test_suite_id="2241",
        locale=["en-US"]
    )
    def run(self, firefox):
        web_search_options_pattern = Pattern("web_search_options.png")
        google_logo_content_search_field_pattern = Pattern("google_logo_content_search_field.png")

        navigate("about:preferences#home")

        preferences_page_opened = exists(web_search_options_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert preferences_page_opened, "The about:preferences page is successfully loaded."

        web_search_option_location = find(web_search_options_pattern)
        web_search_option_width, web_search_option_height = web_search_options_pattern.get_size()
        web_search_option_region = Region(
            web_search_option_location.x - web_search_option_width,
            web_search_option_location.y,
            web_search_option_width * 2,
            web_search_option_height,
        )

        web_search_selected = exists(
            AboutPreferences.CHECKED_BOX, FirefoxSettings.FIREFOX_TIMEOUT, web_search_option_region
        )
        assert web_search_selected, "The option is selected by default."

        navigate("about:home")

        google_logo_content_search_field = exists(
            google_logo_content_search_field_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert google_logo_content_search_field is True, "The search bar is displayed on top of the Homepage."

        navigate("about:newtab")

        google_logo_content_search_field = exists(
            google_logo_content_search_field_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert google_logo_content_search_field is True, "The search bar is displayed on top of the New Tab page."

        navigate("about:preferences#home")

        preferences_page_opened = exists(web_search_options_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert preferences_page_opened, "The about:preferences page is successfully loaded."

        web_search_selected = exists(
            AboutPreferences.CHECKED_BOX, FirefoxSettings.FIREFOX_TIMEOUT, web_search_option_region
        )
        assert web_search_selected, "The option is selected by default."

        click(AboutPreferences.CHECKED_BOX, region=web_search_option_region)

        web_search_selected = exists(
            AboutPreferences.UNCHECKED_BOX, FirefoxSettings.FIREFOX_TIMEOUT, web_search_option_region
        )
        assert web_search_selected, "The options is not selected anymore."

        navigate("about:home")

        google_logo_content_search_field = exists(google_logo_content_search_field_pattern,
                                                  FirefoxSettings.FIREFOX_TIMEOUT)
        assert google_logo_content_search_field is False, "The search bar is not displayed anymore on the Home page."

        navigate("about:newtab")

        google_logo_content_search_field = exists(google_logo_content_search_field_pattern,
                                                  FirefoxSettings.FIREFOX_TIMEOUT)
        assert google_logo_content_search_field is False, "The search bar is not displayed anymore on the New Tab page."

        new_window()

        google_logo_content_search_field = exists(google_logo_content_search_field_pattern,
                                                  FirefoxSettings.FIREFOX_TIMEOUT)
        assert google_logo_content_search_field is False, "The search bar is not displayed anymore in the New Window."

        new_private_window()

        private_window_opened = exists(PrivateWindow.private_window_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert private_window_opened, "Private window opened"

        google_logo_content_search_field = exists(google_logo_content_search_field_pattern)
        assert google_logo_content_search_field, (
            "The search bar is not displayed anymore in the New " "Private Window."
        )

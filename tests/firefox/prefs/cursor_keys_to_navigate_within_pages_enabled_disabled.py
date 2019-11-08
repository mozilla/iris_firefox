# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description="The 'Always use the cursor keys to navigate withing pages' "
                    "checkbox can be successfully enabled / disabled",
        locale=["en-US"],
        test_case_id="143584",
        test_suite_id="2241",
    )
    def run(self, firefox):
        cursor_keys_to_navigate_checkbox_pattern = Pattern(
            "always use the cursor keys to navigate.png"
        ).similar(0.6)
        general_prefs_section_pattern = Pattern("general_preferences_section.png")
        soap_wiki_local_text_with_cursor = Pattern("soap_wiki_local_text_with_cursor.png")
        soap_wiki_local_text_without_cursor_reference = Pattern("soap_wiki_local_text_without_cursor_reference.png")
        soap_wiki_local_text_without_cursor = Pattern("soap_wiki_local_text_without_cursor.png")

        box_width, box_height = AboutPreferences.UNCHECKED_BOX.get_size()

        navigate("about:preferences#general")

        general_prefs_section_opened = exists(
            general_prefs_section_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT
        )
        assert (
            general_prefs_section_opened
        ), "'General' section in 'Preferences' couldn't be opened"

        paste("cursor keys to navigate")

        cursor_keys_to_navigate_checkbox_available = exists(
            cursor_keys_to_navigate_checkbox_pattern
        )
        assert (
            cursor_keys_to_navigate_checkbox_available
        ), "'Always use the cursor keys to navigate within pages' checkbox is not available " \
           "in 'General' preferences section"

        cursor_keys_to_navigate_location = find(
            cursor_keys_to_navigate_checkbox_pattern
        )

        cursor_keys_to_navigate_width, cursor_keys_to_navigate_height = (
            cursor_keys_to_navigate_checkbox_pattern.get_size()
        )
        cursor_keys_to_navigate_region = Region(
            cursor_keys_to_navigate_location.x - box_width * 2,
            cursor_keys_to_navigate_location.y - box_height,
            cursor_keys_to_navigate_width + box_width * 2,
            cursor_keys_to_navigate_height + box_height * 2
        )

        cursor_keys_to_navigate_unchecked = exists(
            AboutPreferences.UNCHECKED_BOX, region = cursor_keys_to_navigate_region
        )
        assert (
            cursor_keys_to_navigate_unchecked
        ), "'Always use the cursor keys to navigate within pages' checkbox is checked"

        click(AboutPreferences.UNCHECKED_BOX, region = cursor_keys_to_navigate_region)

        cursor_keys_to_navigate_checked = exists(
            AboutPreferences.CHECKED_BOX, region = cursor_keys_to_navigate_region
        )
        assert (
            cursor_keys_to_navigate_checked
        ), "'Always use the cursor keys to navigate within pages' checkbox is unchecked"

        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)

        wiki_opened = exists(
            LocalWeb.SOAP_WIKI_SOAP_LABEL, FirefoxSettings.SITE_LOAD_TIMEOUT
        )
        assert wiki_opened, "'Wiki' page couldn't opened"

        soap_local_text_location = find(
            soap_wiki_local_text_without_cursor_reference
        )

        soap_local_text_width, soap_local_text_height = (
            soap_wiki_local_text_without_cursor_reference.get_size()
        )
        soap_local_text_location_region = Region(
            soap_local_text_location.x,
            soap_local_text_location.y - box_width / 2,
            soap_local_text_width,
            soap_local_text_height + box_width
        )

        click(soap_wiki_local_text_without_cursor_reference)
        cursor_keys_appears_on_click = exists(soap_wiki_local_text_with_cursor, FirefoxSettings.SHORT_FIREFOX_TIMEOUT,
                                              region = soap_local_text_location_region)
        assert cursor_keys_appears_on_click, "The cursor keys (the '|' symbol) does not appear in the text"

        # Move cursor key out of text
        for x in range(8):
            type(Key.RIGHT)

        cursor_keys_should_not_appears_on_click = exists(soap_wiki_local_text_without_cursor,
                                                       FirefoxSettings.SHORT_FIREFOX_TIMEOUT,
                                                       region = soap_local_text_location_region)
        assert cursor_keys_should_not_appears_on_click, "The cursor keys (the '|' symbol) is still appearing " \
                                                        "in the referenced text"

        navigate("about:preferences#general")

        general_prefs_section_opened = exists(
            general_prefs_section_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT
        )
        assert (
            general_prefs_section_opened
        ), "'General' section in 'Preferences' couldn't be opened"

        paste("cursor keys to navigate")

        cursor_keys_to_navigate_checkbox_available = exists(
            cursor_keys_to_navigate_checkbox_pattern
        )
        assert (
            cursor_keys_to_navigate_checkbox_available
        ), "'Always use the cursor keys to navigate within pages' checkbox is not available " \
           "in 'General' preferences section"

        cursor_keys_to_navigate_checked = exists(
            AboutPreferences.CHECKED_BOX, region = cursor_keys_to_navigate_region
        )
        assert (
            cursor_keys_to_navigate_checked
        ), "'Always use the cursor keys to navigate within pages' checkbox is unchecked"

        click(AboutPreferences.CHECKED_BOX, region = cursor_keys_to_navigate_region)

        cursor_keys_to_navigate_unchecked = exists(
            AboutPreferences.UNCHECKED_BOX, region = cursor_keys_to_navigate_region
        )
        assert (
            cursor_keys_to_navigate_unchecked
        ), "'Always use the cursor keys to navigate within pages' checkbox is checked"

        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)

        wiki_opened = exists(
            LocalWeb.SOAP_WIKI_SOAP_LABEL, FirefoxSettings.SITE_LOAD_TIMEOUT
        )
        assert wiki_opened, "'Wiki' page couldn't opened"

        click(soap_wiki_local_text_without_cursor_reference)

        cursor_keys_does_not_appears_on_click = exists(soap_wiki_local_text_without_cursor,
                                                       FirefoxSettings.SHORT_FIREFOX_TIMEOUT,
                                                       region = soap_local_text_location_region)
        assert cursor_keys_does_not_appears_on_click, "The cursor keys (the '|' symbol) appear in the text"

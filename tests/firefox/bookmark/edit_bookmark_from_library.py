# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description="Edit a bookmark from Library",
        locale=["en-US"],
        test_case_id="169268",
        test_suite_id="2525",
        profile=Profiles.TEN_BOOKMARKS,
    )
    def run(self, firefox):
        location_field_pattern = Pattern("location_field_label.png")
        name_field_pattern = Pattern("name_bookmark_field.png").similar(0.7)
        tags_field_pattern = Pattern("tags_field_label.png")
        keyword_field_pattern = Pattern("keyword_field_label.png")
        bookmark_new_name_pattern = Pattern("bookmark_new_name.png")
        linkedin_logo = Pattern("linkedin_logo.png")

        open_library()

        library_opened = exists(linkedin_logo)
        assert library_opened is True, "Bookmarks library is opened"

        click(linkedin_logo)

        name_field_displayed = exists(name_field_pattern)
        assert name_field_displayed is True, "Name field is displayed"

        fields_location = find(name_field_pattern)
        fields_width, fields_height = name_field_pattern.get_size()
        fields_region = Region(
            fields_location.x - fields_width,
            fields_location.y,
            fields_width * 10,
            fields_height * 15,
        )

        click(name_field_pattern, region=fields_region)

        edit_select_all()

        paste("New Name")

        location_field_displayed = exists(location_field_pattern, region=fields_region)
        assert location_field_displayed is True, "Location field is displayed"

        click(location_field_pattern, region=fields_region)

        edit_select_all()
        paste("http://wikipedia.org/")

        tags_field_displayed = exists(tags_field_pattern, region=fields_region)
        assert tags_field_displayed is True, "Tags field is displayed"

        click(tags_field_pattern, region=fields_region)

        edit_select_all()
        paste("tags, test")

        keyword_field_displayed = exists(
            keyword_field_pattern.similar(0.7), region=fields_region
        )
        assert keyword_field_displayed is True, "Keywords field is displayed"

        click(keyword_field_pattern, region=fields_region)

        edit_select_all()
        paste("test")

        type(Key.ENTER)

        close_tab()

        open_library()

        library_opened = exists(Library.TITLE)
        assert library_opened is True, "Library window is reopened"

        new_name_bookmark_created = exists(bookmark_new_name_pattern)
        assert new_name_bookmark_created is True, '"New Name" bookmark exists'

        click(bookmark_new_name_pattern)

        name_field_displayed = exists(name_field_pattern)
        assert name_field_displayed is True, "Name field is displayed"

        click(name_field_pattern)

        name_is_edited = copy_to_clipboard()
        time.sleep(Settings.DEFAULT_UI_DELAY)
        assert name_is_edited == "New Name", "Bookmark's name is edited"

        type(Key.TAB)

        location_edited = copy_to_clipboard()
        time.sleep(Settings.DEFAULT_UI_DELAY)
        assert (
            location_edited == "http://wikipedia.org/"
        ), "Bookmark's location is edited"

        type(Key.TAB)

        tags_edited = copy_to_clipboard()
        time.sleep(Settings.DEFAULT_UI_DELAY)
        assert tags_edited == "tags, test", "Bookmark's tags are edited"

        if OSHelper.is_mac():
            type(Key.TAB)
        else:
            [type(Key.TAB) for _ in range(2)]

        keyword_edited = copy_to_clipboard()
        time.sleep(Settings.DEFAULT_UI_DELAY)
        assert keyword_edited == "test", "Bookmark's keywords are edited"

        close_window_control("auxiliary")

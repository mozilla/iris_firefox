# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Edit a bookmark from Library'
        self.test_case_id = '169268'
        self.test_suite_id = '2525'
        self.locale = ['en-US']
        self.profile = Profile.TEN_BOOKMARKS

    def setup(self):
        BaseTest.setup(self)
        self.profile = Profile.TEN_BOOKMARKS

    def run(self):
        location_field_pattern = Pattern('location_field_label.png')
        name_field_pattern = Pattern('name_bookmark_field.png').similar(0.85)
        tags_field_pattern = Pattern('tags_field_label.png')
        keyword_field_pattern = Pattern('keyword_field_label.png')
        bookmark_new_name_pattern = Pattern('bookmark_new_name.png')
        edited_name_pattern = Pattern('edited_bookmark_name_library.png')
        edited_tags_pattern = Pattern('edited_bookmark_tags_library.png')
        edited_location_pattern = Pattern('edited_bookmark_location_library.png')
        edited_keyword_pattern = Pattern('edited_bookmark_keyword_library.png')
        linkedin_logo = Pattern('linkedin_logo.png')

        open_library()

        library_opened = exists(linkedin_logo)
        assert_true(self, library_opened, 'Bookmarks library is opened')

        click(linkedin_logo)

        name_field_displayed = exists(name_field_pattern)
        assert_true(self, name_field_displayed, 'Name field is displayed')

        fields_location = find(name_field_pattern)
        fields_region = Region(0, fields_location.y, SCREEN_WIDTH * 2 // 3, SCREEN_HEIGHT * 2 // 3)

        click(name_field_pattern, in_region=fields_region)

        edit_select_all()
        paste('New Name')

        location_field_displayed = exists(location_field_pattern, in_region=fields_region)
        assert_true(self, location_field_displayed, 'Location field is displayed')

        click(location_field_pattern, in_region=fields_region)

        edit_select_all()
        paste('http://wikipedia.org/')

        tags_field_displayed = exists(tags_field_pattern, in_region=fields_region)
        assert_true(self, tags_field_displayed, 'Tags field is displayed')

        click(tags_field_pattern, in_region=fields_region)

        edit_select_all()
        paste('tags, test')

        keyword_field_displayed = exists(keyword_field_pattern.similar(0.7), in_region=fields_region)
        assert_true(self, keyword_field_displayed, 'Keywords field is displayed')

        click(keyword_field_pattern, in_region=fields_region)

        edit_select_all()
        paste('test')

        type(Key.ENTER)

        close_tab()

        open_library()

        library_opened = exists(Library.TAGS)
        assert_true(self, library_opened, 'Library window is reopened')

        new_name_bookmark_created = exists(bookmark_new_name_pattern)
        assert_true(self, new_name_bookmark_created, '"New Name" bookmark exists')

        bookmark_name_location = find(bookmark_new_name_pattern)
        fields_region = Region(0, bookmark_name_location.y, SCREEN_WIDTH * 2 // 3, SCREEN_HEIGHT * 2 // 3)

        click(bookmark_new_name_pattern)

        name_field_displayed = exists(name_field_pattern)
        assert_true(self, name_field_displayed, 'Name field is displayed')

        click(name_field_pattern)

        edit_select_all()
        name_is_edited = exists(edited_name_pattern, in_region=fields_region)
        assert_true(self, name_is_edited, 'Bookmark\'s name is edited')

        location_field_displayed = exists(location_field_pattern, in_region=fields_region)
        assert_true(self, location_field_displayed, 'Location field is displayed')

        click(location_field_pattern, in_region=fields_region)

        edit_select_all()
        location_edited = exists(edited_location_pattern)
        assert_true(self, location_edited, 'Bookmark\'s location is edited')

        tags_edited = exists(edited_tags_pattern.similar(0.7))
        assert_true(self, tags_edited, 'Bookmark\'s tags are edited')

        keyword_field_displayed = exists(keyword_field_pattern, in_region=fields_region)
        assert_true(self, keyword_field_displayed, 'Keywords field is displayed')

        click(keyword_field_pattern, in_region=fields_region)

        edit_select_all()
        keyword_edited = exists(edited_keyword_pattern)
        assert_true(self, keyword_edited, 'Bookmark\'s keywords are edited')

        close_tab()

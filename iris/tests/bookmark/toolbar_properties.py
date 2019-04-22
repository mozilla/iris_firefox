# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = '\'Properties\' from \'Bookmarks Toolbar\''
        self.test_case_id = '164376'
        self.test_suite_id = '2525'
        self.locales = ['en-US']

    def setup(self):
        BaseTest.setup(self)
        self.profile = Profile.TEN_BOOKMARKS
        return

    def run(self):
        getting_started_toolbar_bookmark_pattern = Pattern('toolbar_bookmark_icon.png')
        renamed_toolbar_bookmark_pattern = Pattern('renamed_toolbar_bookmark.png')
        properties_popup_save_button_pattern = Pattern('save_bookmark_name.png')
        properties_keyword_field_pattern = Pattern('keyword_field.png')
        bookmark_properties_option = Pattern('properties_option.png')
        keyword_modified_pattern = Pattern('keyword_modified.png')
        properties_tags_field_pattern = Pattern('tags_field.png')
        name_modified_pattern = Pattern('name_modified.png')
        tags_modified_pattern = Pattern('tags_modified.png')

        open_bookmarks_toolbar()

        bookmarks_folder_available_in_toolbar = exists(getting_started_toolbar_bookmark_pattern)
        assert_true(self, bookmarks_folder_available_in_toolbar, 'The \'Bookmarks Toolbar\' is enabled.')

        right_click(getting_started_toolbar_bookmark_pattern)

        properties_option_available = exists(bookmark_properties_option, Settings.SHORT_FIREFOX_TIMEOUT)
        assert_true(self, properties_option_available,
                    '\'Properties\' option in available in context menu after right-click at the bookmark in toolbar.')

        click(bookmark_properties_option)

        properties_opened = exists(properties_popup_save_button_pattern, Settings.SHORT_FIREFOX_TIMEOUT)
        assert_true(self, properties_opened, 'Properties for \'Getting Started\' window is opened.')

        paste('New Name')

        name_modified = exists(name_modified_pattern)
        assert_true(self, name_modified, 'Another value successfully entered into the \'Name\' field')

        keyword_field_available = exists(properties_keyword_field_pattern, Settings.SHORT_FIREFOX_TIMEOUT)
        assert_true(self, keyword_field_available, '\'Keyword\' field is available in properties window.')

        click(properties_keyword_field_pattern)

        paste('test')

        keyword_edited = exists(keyword_modified_pattern)
        assert_true(self, keyword_edited, 'Another value successfully entered into the \'Keyword\' field')

        tags_field_available = exists(properties_tags_field_pattern)
        assert_true(self, tags_field_available, '\'Tags\' field is available in properties window.')

        click(properties_tags_field_pattern)

        paste('Tag')

        tags_edited = exists(tags_modified_pattern)
        assert_true(self, tags_edited, 'Another value successfully entered into the \'Tags\' field')

        click(properties_popup_save_button_pattern)

        bookmark_renamed = exists(renamed_toolbar_bookmark_pattern, Settings.SHORT_FIREFOX_TIMEOUT)
        assert_true(self, bookmark_renamed, 'The bookmark information is correctly updated.')

        restart_firefox(self,
                        self.browser.path,
                        self.profile_path,
                        self.base_local_web_url)

        bookmark_renamed = exists(renamed_toolbar_bookmark_pattern, Settings.SHORT_FIREFOX_TIMEOUT)
        assert_true(self, bookmark_renamed, 'The bookmark name persists modified after restarting Firefox.')

        right_click(renamed_toolbar_bookmark_pattern)

        click(bookmark_properties_option)

        properties_opened = exists(properties_popup_save_button_pattern, Settings.SHORT_FIREFOX_TIMEOUT)
        assert_true(self, properties_opened, 'Properties for \'Getting Started\' window is opened.')

        assert_true(self, keyword_edited, '\'Keyword\' value persists modified after restarting Firefox.')
        assert_true(self, tags_edited, '\'Tags\' value persists modified after restarting Firefox.')
        
        type(Key.ESC)

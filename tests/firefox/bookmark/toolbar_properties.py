# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='\'Properties\' from \'Bookmarks Toolbar\'',
        locale=['en-US'],
        test_case_id='164376',
        test_suite_id='2525',
        profile=Profiles.TEN_BOOKMARKS,
    )
    def run(self, firefox):
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
        assert bookmarks_folder_available_in_toolbar is True, 'The \'Bookmarks Toolbar\' is enabled.'

        right_click(getting_started_toolbar_bookmark_pattern)

        properties_option_available = exists(bookmark_properties_option, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert properties_option_available is True, '\'Properties\' option in available in context menu after ' \
                                                    'right-click at the bookmark in toolbar.'

        click(bookmark_properties_option)

        properties_opened = exists(properties_popup_save_button_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert properties_opened is True, 'Properties for \'Getting Started\' window is opened.'

        paste('New Name')

        name_modified = exists(name_modified_pattern)
        assert name_modified is True, 'Another value successfully entered into the \'Name\' field'

        keyword_field_available = exists(properties_keyword_field_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert keyword_field_available is True, '\'Keyword\' field is available in properties window.'

        click(properties_keyword_field_pattern)

        paste('test')

        keyword_edited = exists(keyword_modified_pattern)
        assert keyword_edited is True, 'Another value successfully entered into the \'Keyword\' field'

        tags_field_available = exists(properties_tags_field_pattern)
        assert tags_field_available is True, '\'Tags\' field is available in properties window.'

        click(properties_tags_field_pattern)

        paste('Tag')

        tags_edited = exists(tags_modified_pattern)
        assert tags_edited is True, 'Another value successfully entered into the \'Tags\' field'

        click(properties_popup_save_button_pattern)

        bookmark_renamed = exists(renamed_toolbar_bookmark_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert bookmark_renamed is True, 'The bookmark information is correctly updated.'

        firefox.restart()

        bookmark_renamed = exists(renamed_toolbar_bookmark_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert bookmark_renamed is True, 'The bookmark name persists modified after restarting Firefox.'

        right_click(renamed_toolbar_bookmark_pattern)

        click(bookmark_properties_option)

        properties_opened = exists(properties_popup_save_button_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert properties_opened is True, 'Properties for \'Getting Started\' window is opened.'

        keyword_edited = exists(keyword_modified_pattern)
        assert keyword_edited is True, '\'Keyword\' value persists modified after restarting Firefox.'

        tags_edited = exists(tags_modified_pattern)
        assert tags_edited is True, '\'Tags\' value persists modified after restarting Firefox.'
        
        type(Key.ESC)

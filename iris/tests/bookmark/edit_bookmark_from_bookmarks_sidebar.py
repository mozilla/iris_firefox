# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):
    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Edit a bookmark from Bookmarks Sidebar'
        self.test_case_id = '168937'
        self.test_suite_id = '2525'
        self.locales = ['en-US']
        self.blocked_by = {'id': '1527258', 'platform': Platform.WINDOWS}

    def run(self):
        properties_option_pattern = Pattern('properties_option.png')
        new_modified_bookmark_pattern = Pattern('bookmark_modified.png')
        name_before_editing_pattern = Pattern('name_field.png')
        location_before_editing_pattern = Pattern('location_field.png')
        tags_before_editing_pattern = Pattern('tags_field.png')
        keyword_before_editing_pattern = Pattern('keyword_field.png')
        name_after_editing_pattern = Pattern('name_saved.png')
        location_after_editing_pattern = Pattern('location_saved.png')
        tags_after_editing_pattern = Pattern('tags_saved.png')
        keyword_after_editing_pattern = Pattern('keyword_saved.png')

        if Settings.is_mac():
            other_bookmarks_pattern = Pattern('bookmarks_toolbar.png')
            bookmark_getting_started_pattern = Pattern('bookmark_from_sidebar.png')
        else:
            other_bookmarks_pattern = Library.BOOKMARKS_TOOLBAR
            properties_window_pattern = Pattern('properties_window.png')
            bookmark_getting_started_pattern = Pattern('toolbar_bookmark_icon.png')

        bookmarks_sidebar('open')

        bookmarks_sidebar_menu_exists = exists(SidebarBookmarks.BOOKMARKS_HEADER, Settings.FIREFOX_TIMEOUT)
        assert_true(self, bookmarks_sidebar_menu_exists, 'Bookmarks Sidebar is correctly displayed')

        other_bookmarks_exists = exists(other_bookmarks_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, other_bookmarks_exists, 'Other bookmarks section exists')

        click(other_bookmarks_pattern)

        bookmark_getting_started_exists = exists(bookmark_getting_started_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, bookmark_getting_started_exists, 'Getting started bookmark exists')

        right_click(bookmark_getting_started_pattern)

        properties_option_exists = exists(properties_option_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, properties_option_exists, 'Properties option exists')

        click(properties_option_pattern)

        if not Settings.is_mac():
            properties_window_exists = exists(properties_window_pattern, Settings.FIREFOX_TIMEOUT)
            assert_true(self, properties_window_exists, 'Properties for "Getting Started" window is opened')
        else:
            properties_window_exists = exists(name_before_editing_pattern, Settings.FIREFOX_TIMEOUT)
            assert_true(self, properties_window_exists, 'Properties for "Getting Started" window is opened')

        name_before_exists = exists(name_before_editing_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, name_before_exists, 'Name field exists')

        location_before_exists = exists(location_before_editing_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, location_before_exists, 'Location field exists')

        tags_before_exists = exists(tags_before_editing_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, tags_before_exists, 'Tags field exists')

        keyword_before_exists = exists(keyword_before_editing_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, keyword_before_exists, 'Keyword field exists')

        paste('New Name')
        type(Key.TAB)

        paste('wikipedia.org')
        type(Key.TAB)

        paste('Tag')

        if Settings.is_mac():
            type(Key.TAB)
        else:
            [type(Key.TAB) for _ in range(2)]

        paste('test')

        type(Key.ENTER)

        new_modified_bookmark_exists = exists(new_modified_bookmark_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, new_modified_bookmark_exists, 'New modified bookmark exists')

        right_click(new_modified_bookmark_pattern)

        properties_option_exists = exists(properties_option_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, properties_option_exists, 'Properties option exists')

        click(properties_option_pattern)

        name_after_exists = exists(name_after_editing_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, name_after_exists, 'Name field changes are correctly saved')

        type(Key.TAB)

        location_after_exists = exists(location_after_editing_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, location_after_exists, 'Location field changes are correctly saved')

        type(Key.TAB)

        tags_after_exists = exists(tags_after_editing_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, tags_after_exists, 'Tags field changes are correctly saved')

        if Settings.is_mac():
            type(Key.TAB)
        else:
            [type(Key.TAB) for _ in range(2)]

        keyword_after_exists = exists(keyword_after_editing_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, keyword_after_exists, 'Keyword field changes are correctly saved')

        type(Key.ENTER)

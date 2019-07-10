# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Edit a bookmark from Bookmarks Sidebar',
        locale=['en-US'],
        test_case_id='168937',
        test_suite_id='2525',
        blocked_by={'id': '1527258', 'platform': OSPlatform.WINDOWS}
    )
    def run(self, firefox):
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

        if OSHelper.is_mac():
            other_bookmarks_pattern = Pattern('bookmarks_toolbar.png')
            bookmark_getting_started_pattern = Pattern('bookmark_from_sidebar.png')
        else:
            other_bookmarks_pattern = Library.BOOKMARKS_TOOLBAR
            properties_window_pattern = Pattern('properties_window.png')
            bookmark_getting_started_pattern = Pattern('toolbar_bookmark_icon.png')

        bookmarks_sidebar('open')

        bookmarks_sidebar_menu_exists = exists(SidebarBookmarks.BOOKMARKS_HEADER, FirefoxSettings.FIREFOX_TIMEOUT)
        assert bookmarks_sidebar_menu_exists is True, 'Bookmarks Sidebar is correctly displayed'

        other_bookmarks_exists = exists(other_bookmarks_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert other_bookmarks_exists is True, 'Other bookmarks section exists'

        click(other_bookmarks_pattern)

        bookmark_getting_started_exists = exists(bookmark_getting_started_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert bookmark_getting_started_exists is True, 'Getting started bookmark exists'

        right_click(bookmark_getting_started_pattern)

        properties_option_exists = exists(properties_option_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert properties_option_exists is True, 'Properties option exists'

        click(properties_option_pattern)

        if not OSHelper.is_mac():
            properties_window_exists = exists(properties_window_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
            assert properties_window_exists is True, 'Properties for "Getting Started" window is opened'
        else:
            properties_window_exists = exists(name_before_editing_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
            assert properties_window_exists is True, 'Properties for "Getting Started" window is opened'

        name_before_exists = exists(name_before_editing_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert name_before_exists is True, 'Name field exists'

        location_before_exists = exists(location_before_editing_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert location_before_exists is True, 'Location field exists'

        tags_before_exists = exists(tags_before_editing_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert tags_before_exists is True, 'Tags field exists'

        keyword_before_exists = exists(keyword_before_editing_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert keyword_before_exists is True, 'Keyword field exists'

        paste('New Name')
        type(Key.TAB)

        paste('wikipedia.org')
        type(Key.TAB)

        paste('Tag')

        if OSHelper.is_mac():
            type(Key.TAB)
        else:
            [type(Key.TAB) for _ in range(2)]

        paste('test')

        type(Key.ENTER)

        new_modified_bookmark_exists = exists(new_modified_bookmark_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert new_modified_bookmark_exists is True, 'New modified bookmark exists'

        right_click(new_modified_bookmark_pattern)

        properties_option_exists = exists(properties_option_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert properties_option_exists is True, 'Properties option exists'

        click(properties_option_pattern)

        name_after_exists = exists(name_after_editing_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert name_after_exists is True, 'Name field changes are correctly saved'

        type(Key.TAB)

        location_after_exists = exists(location_after_editing_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert location_after_exists is True, 'Location field changes are correctly saved'

        type(Key.TAB)

        tags_after_exists = exists(tags_after_editing_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert tags_after_exists is True, 'Tags field changes are correctly saved'

        if OSHelper.is_mac():
            type(Key.TAB)
        else:
            [type(Key.TAB) for _ in range(2)]

        keyword_after_exists = exists(keyword_after_editing_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert keyword_after_exists is True, 'Keyword field changes are correctly saved'

        type(Key.ENTER)

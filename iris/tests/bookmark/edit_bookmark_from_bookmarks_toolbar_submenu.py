# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Edit a bookmark from the Bookmarks Toolbar submenu'
        self.test_case_id = '163491'
        self.test_suite_id = '2525'
        self.locales = ['en-US']
        self.exclude = [Platform.MAC]
        self.blocked_by = {'id': '1527258', 'platform': Platform.WINDOWS}

    def setup(self):
        BaseTest.setup(self)
        self.profile = Profile.TEN_BOOKMARKS
        return

    def run(self):
        firefox_menu_bookmarks_pattern = Pattern('firefox_menu_bookmarks.png')
        firefox_menu_bookmarks_toolbar_pattern = Pattern('firefox_menu_bookmarks_toolbar.png')
        firefox_menu_most_visited_pattern = Pattern('firefox_menu_most_visited.png')
        getting_started_pattern = Pattern('getting_started_top_menu.png')
        properties_option_pattern = Pattern('properties_option.png')
        name_field_pattern = Pattern('name_field.png')
        keyword_edited_pattern = Pattern('keyword_edited.png')
        location_edited_pattern = Pattern('location_edited.png')
        name_edited_pattern = Pattern('name_edited.png')
        tags_edited_pattern = Pattern('tags_edited.png')

        open_firefox_menu()

        firefox_menu_bookmarks_exists = exists(firefox_menu_bookmarks_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, firefox_menu_bookmarks_exists, 'Firefox menu > Bookmarks exists')

        click(firefox_menu_bookmarks_pattern)

        bookmarks_toolbar_folder_exists = exists(firefox_menu_bookmarks_toolbar_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, bookmarks_toolbar_folder_exists, 'Firefox menu > Bookmarks > Bookmarks Toolbar folder exists')

        click(firefox_menu_bookmarks_toolbar_pattern)

        most_visited_folder_exists = exists(firefox_menu_most_visited_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, most_visited_folder_exists, 'Firefox menu > Bookmarks > Bookmarks Toolbar > Most Visited '
                                                      'folder exists')

        getting_started_exists = exists(getting_started_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, getting_started_exists, 'Firefox menu > Bookmarks > Bookmarks Toolbar > Getting Started '
                                                  'bookmark exists')

        right_click(getting_started_pattern)

        properties_option_exists = exists(properties_option_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, properties_option_exists, 'Properties option exists')

        click(properties_option_pattern)

        bookmark_properties_opened = exists(name_field_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, bookmark_properties_opened, 'Bookmark properties window is opened')

        paste('Focus')
        type(Key.TAB)

        paste(LocalWeb.FOCUS_TEST_SITE)
        type(Key.TAB)

        paste('Focus')
        if Settings.is_mac():
            type(Key.TAB)
        else:
            type(Key.TAB)
            type(Key.TAB)
        paste('Focus')

        type(Key.ENTER)

        open_bookmarks_toolbar()

        bookmark_edited = exists(LocalWeb.FOCUS_BOOKMARK_SMALL, Settings.FIREFOX_TIMEOUT)
        assert_true(self, bookmark_edited, 'The window is dismissed and all the changes are correctly saved')

        right_click(LocalWeb.FOCUS_BOOKMARK_SMALL)

        properties_option_exists = exists(properties_option_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, properties_option_exists, 'Properties option exists')

        click(properties_option_pattern)

        name_edited = exists(name_edited_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, name_edited, 'Name is edited')

        location_edited = exists(location_edited_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, location_edited, 'Location is edited')

        tags_edited = exists(tags_edited_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, tags_edited, 'Tags are edited')

        keyword_edited = exists(keyword_edited_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, keyword_edited, 'Keyword are edited')

        type(Key.ESC)

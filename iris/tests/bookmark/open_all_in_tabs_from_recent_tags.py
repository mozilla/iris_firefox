# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):
    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Open \'All in Tabs\' option from \'Recent Tags\' section'
        self.test_case_id = '163222'
        self.test_suite_id = '2525'
        self.locales = ['en-US']

    def setup(self):
        BaseTest.setup(self)
        self.profile = Profile.TEN_BOOKMARKS
        return

    def run(self):
        image_in_firefox_page_pattern = LocalWeb.FIREFOX_IMAGE
        image_in_focus_page_pattern = LocalWeb.FOCUS_IMAGE
        firefox_bookmark_with_tag_pattern = Pattern('firefox_bookmark_with_tag.png')
        open_all_in_tabs_option_pattern = Pattern('open_all_in_tabs_option.png')
        focus_bookmark_with_tag_pattern = Pattern('focus_bookmark_with_tag.png')
        other_bookmarks_folder_pattern = Pattern('other_bookmarks_folder.png')
        top_menu_bookmarks_option_pattern = Pattern('bookmarks_top_menu.png')
        name_column_header_pattern = Pattern('name_column_header.png')
        recent_tags_option_pattern = Pattern('recent_tags_option.png')
        firefox_bookmark_pattern = Pattern('firefox_bookmark.png')
        focus_bookmark_pattern = Pattern('focus_bookmark.png')
        tags_field_pattern = Pattern('tags_field.png')
        test_tag_pattern = Pattern('test_tag.png')

        open_library()

        library_menu_opened = exists(other_bookmarks_folder_pattern, DEFAULT_SHORT_FIREFOX_TIMEOUT)
        assert_true(self, library_menu_opened, '\'Library\' menu opened')

        click(other_bookmarks_folder_pattern)

        click(name_column_header_pattern)

        firefox_bookmark_available = exists(firefox_bookmark_pattern, DEFAULT_SHORT_FIREFOX_TIMEOUT)
        assert_true(self, firefox_bookmark_available,
                    '\'Firefox\' bookmark available in \'Other bookmarks\' folder in \'Library\' menu')

        focus_bookmark_available = exists(focus_bookmark_pattern, DEFAULT_SHORT_FIREFOX_TIMEOUT)
        assert_true(self, focus_bookmark_available,
                    '\'Focus\' bookmarks available in \'Other bookmarks\' folder in \'Library\' menu')

        click(firefox_bookmark_pattern)

        click(tags_field_pattern)

        paste('test')
        type(Key.ENTER)
        bookmark_tagged = exists(firefox_bookmark_with_tag_pattern, DEFAULT_SHORT_FIREFOX_TIMEOUT)
        assert_true(self, bookmark_tagged, '\'Firefox\' bookmark was tagged')

        click(focus_bookmark_pattern)

        click(tags_field_pattern)

        paste('test')
        type(Key.ENTER)
        bookmark_tagged = exists(focus_bookmark_with_tag_pattern, DEFAULT_SHORT_FIREFOX_TIMEOUT)
        assert_true(self, bookmark_tagged, '\'Focus\' bookmark was tagged')

        close_tab()
        open_firefox_menu()
        bookmarks_option_is_available_in_top_menu = exists(top_menu_bookmarks_option_pattern)
        assert_true(self, bookmarks_option_is_available_in_top_menu,
                    '\'Bookmarks\' option is available in Firefox top menu')

        click(top_menu_bookmarks_option_pattern)

        recent_tags_option_available = exists(recent_tags_option_pattern, DEFAULT_SHORT_FIREFOX_TIMEOUT)
        assert_true(self, recent_tags_option_available,
                    '\'Recent tags\' option available after clicking at \'Bookmarks option\' in Firefox top menu')

        mouse_move(recent_tags_option_pattern)
        test_tag_displayed = exists(test_tag_pattern, DEFAULT_SHORT_FIREFOX_TIMEOUT)
        assert_true(self, test_tag_displayed, 'The recent bookmark tags are displayed.')

        right_click(test_tag_pattern)

        open_all_in_tabs_option_available = exists(open_all_in_tabs_option_pattern, DEFAULT_SHORT_FIREFOX_TIMEOUT)
        assert_true(self, open_all_in_tabs_option_available,
                    '\'Open all in tabs\' option available after right click at the tag name')

        click(open_all_in_tabs_option_pattern)

        firefox_page_opened = exists(image_in_firefox_page_pattern, DEFAULT_SITE_LOAD_TIMEOUT)
        next_tab()
        focus_page_opened = exists(image_in_focus_page_pattern, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, firefox_page_opened and focus_page_opened,
                    'Al the bookmarks that contain that specific tag are opened in separate tabs.')

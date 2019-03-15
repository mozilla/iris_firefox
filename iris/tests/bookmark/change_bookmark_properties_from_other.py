# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Change the properties of a bookmark from \'Other Bookmarks\' sections - Bookmarks menu'
        self.test_case_id = '163219'
        self.test_suite_id = '2525'
        self.locales = ['en-US']

    def setup(self):
        BaseTest.setup(self)
        self.profile = Profile.TEN_BOOKMARKS

    def run(self):
        bookmark_location_field_pattern = Pattern('add_bookmark_location_field.png')
        bookmarks_top_menu_pattern = Pattern('bookmarks_top_menu.png')
        other_bookmarks_pattern = Pattern('other_bookmarks.png')
        firefox_bookmark_top_menu_pattern = Pattern('firefox_bookmark_top_menu.png')
        bookmark_properties_item_pattern = Pattern('bookmark_properties_button.png')
        name_bookmark_field_pattern = Pattern('name_bookmark_field.png')
        tags_field_pattern = Pattern('tags_field.png')
        keyword_field_pattern = Pattern('keyword_field.png')
        pocket_bookmark_name_pattern = Pattern('pocket_bookmark_name.png')

        open_firefox_menu()

        firefox_menu_opened = exists(bookmarks_top_menu_pattern)
        assert_true(self, firefox_menu_opened, 'Firefox menu is opened')

        click(bookmarks_top_menu_pattern)

        bookmarks_menu_opened = exists(other_bookmarks_pattern)
        assert_true(self, bookmarks_menu_opened, 'Bookmarks menu is opened')

        click(other_bookmarks_pattern)

        pocket_bookmarks_list = find_all(pocket_bookmark_name_pattern)
        pocket_bookmark_unique = len(pocket_bookmarks_list) == 1
        assert_true(self, pocket_bookmark_unique, 'Only one pocket bookmark is displayed')

        firefox_bookmark_displayed = exists(firefox_bookmark_top_menu_pattern)
        assert_true(self, firefox_bookmark_displayed, 'Firefox bookmark is properly displayed')

        bookmark_width, bookmark_height = firefox_bookmark_top_menu_pattern.get_size()
        bookmark_location = find(firefox_bookmark_top_menu_pattern)
        bookmark_region = Region(bookmark_location.x, bookmark_location.y, bookmark_width, bookmark_height)

        right_click(firefox_bookmark_top_menu_pattern)

        bookmark_context_menu_opened = exists(bookmark_properties_item_pattern)
        assert_true(self, bookmark_context_menu_opened, 'Bookmark context menu is properly displayed')

        click(bookmark_properties_item_pattern)

        name_field_reachable = exists(name_bookmark_field_pattern)
        assert_true(self, name_field_reachable, 'Name field is reachable')

        click(name_bookmark_field_pattern)

        edit_select_all()
        paste('Pocket')

        location_field_reachable = exists(bookmark_location_field_pattern)
        assert_true(self, location_field_reachable, 'Location field is reachable')

        click(bookmark_location_field_pattern)

        edit_select_all()
        paste(LocalWeb.POCKET_TEST_SITE)

        tags_field_reachable = exists(tags_field_pattern)
        assert_true(self, tags_field_reachable, 'Tags field is reachable')

        click(tags_field_pattern)

        edit_select_all()
        paste('Tag')

        keyword_field_reachable = exists(keyword_field_pattern)
        assert_true(self, keyword_field_reachable, 'Keywords field is reachable')

        click(keyword_field_pattern)

        edit_select_all()
        paste('test')

        type(Key.ENTER)

        open_firefox_menu()

        click(bookmarks_top_menu_pattern)

        click(other_bookmarks_pattern)

        pocket_bookmarks_list = find_all(pocket_bookmark_name_pattern)
        two_pocket_bookmarks_displayed = len(pocket_bookmarks_list) == 2
        assert_true(self, two_pocket_bookmarks_displayed, 'Two "Pocket" bookmarks are saved')

        firefox_bookmark_not_exists = not exists(firefox_bookmark_top_menu_pattern)
        assert_true(self, firefox_bookmark_not_exists, 'Firefox bookmark doesn\'t exist')

        pocket_bookmark_at_firefox_bookmark_place = exists(pocket_bookmark_name_pattern, in_region=bookmark_region)
        assert_true(self, pocket_bookmark_at_firefox_bookmark_place, 'Pocket bookmark replaced firefox bookmark')

        right_click(pocket_bookmark_name_pattern, in_region=bookmark_region)

        click(bookmark_properties_item_pattern)

        type(Key.ESC)

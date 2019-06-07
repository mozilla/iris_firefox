# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Change the properties of a bookmark from \'Other Bookmarks\' sections - Bookmarks menu',
        locale=['en-US'],
        test_case_id='163219',
        test_suite_id='2525',
        profile=Profiles.TEN_BOOKMARKS,
        exclude=OSPlatform.MAC
    )
    def run(self, firefox):
        bookmark_location_field_pattern = Pattern('location_field_label.png')
        bookmarks_top_menu_pattern = Pattern('bookmarks_top_menu.png')
        other_bookmarks_pattern = Pattern('other_bookmarks.png')
        firefox_bookmark_top_menu_pattern = Pattern('firefox_bookmark_top_menu.png').similar(0.9)
        bookmark_properties_item_pattern = Pattern('bookmark_properties_button.png')
        name_bookmark_field_pattern = Pattern('name_bookmark_field.png')
        tags_field_pattern = Pattern('tags_field_label.png')
        keyword_field_pattern = Pattern('keyword_field_label.png')
        pocket_bookmark_name_pattern = Pattern('pocket_bookmark_name.png')
        pocket_url_saved_pattern = Pattern('pocket_url.png')
        tag_bookmark_saved_pattern = Pattern('tag_bookmark.png')
        test_keyword_saved_pattern = Pattern('test_keyword.png')
        tag = 'Tag_bookmark'
        keyword = 'test'

        open_firefox_menu()

        firefox_menu_opened = exists(bookmarks_top_menu_pattern)
        assert firefox_menu_opened is True, 'Firefox menu is opened'

        click(bookmarks_top_menu_pattern)

        bookmarks_menu_opened = exists(other_bookmarks_pattern)
        assert bookmarks_menu_opened is True, 'Bookmarks menu is opened'

        click(other_bookmarks_pattern)

        firefox_bookmark_displayed = exists(firefox_bookmark_top_menu_pattern)
        assert firefox_bookmark_displayed is True, 'Firefox bookmark is properly displayed'

        bookmark_width, bookmark_height = firefox_bookmark_top_menu_pattern.get_size()
        bookmark_location = find(firefox_bookmark_top_menu_pattern)
        bookmark_region = Region(bookmark_location.x, bookmark_location.y, bookmark_width * 2, bookmark_height * 2)

        other_bookmarks_location_y = find(other_bookmarks_pattern).y
        bookmark_location_y = find(firefox_bookmark_top_menu_pattern).y

        hover(Location(Screen.SCREEN_WIDTH, other_bookmarks_location_y))

        hover(Location(Screen.SCREEN_WIDTH, bookmark_location_y))

        right_click(firefox_bookmark_top_menu_pattern)

        bookmark_context_menu_opened = exists(bookmark_properties_item_pattern)
        assert bookmark_context_menu_opened is True, 'Bookmark context menu is properly displayed'

        click(bookmark_properties_item_pattern)

        name_field_reachable = exists(name_bookmark_field_pattern)
        assert name_field_reachable  is True, 'Name field is reachable'

        click(name_bookmark_field_pattern)

        edit_select_all()
        paste('Pocket')

        tags_field_reachable = exists(bookmark_location_field_pattern)
        assert tags_field_reachable is True, 'Location field is reachable'

        click(bookmark_location_field_pattern)

        edit_select_all()
        paste(LocalWeb.POCKET_TEST_SITE)

        tags_field_reachable = exists(tags_field_pattern)
        assert tags_field_reachable is True, 'Tags field is reachable'

        click(tags_field_pattern)

        edit_select_all()
        paste(tag)

        keywords_field_reachable = exists(keyword_field_pattern)
        assert keywords_field_reachable is True, 'Keywords field is reachable'

        click(keyword_field_pattern)

        edit_select_all()
        paste(keyword)

        type(Key.ENTER)

        open_firefox_menu()

        firefox_menu_opened = exists(bookmarks_top_menu_pattern)
        assert firefox_menu_opened is True, 'Firefox menu is opened'

        click(bookmarks_top_menu_pattern)

        bookmarks_menu_opened = exists(other_bookmarks_pattern)
        assert bookmarks_menu_opened is True, 'Bookmarks menu is opened'

        click(other_bookmarks_pattern)

        firefox_bookmark_not_exists = not exists(firefox_bookmark_top_menu_pattern)
        assert firefox_bookmark_not_exists is True, 'Firefox bookmark doesn\'t exist'

        pocket_bookmark_at_firefox_bookmark_place = exists(pocket_bookmark_name_pattern, region=bookmark_region)
        assert pocket_bookmark_at_firefox_bookmark_place is True, 'Pocket bookmark replaced firefox bookmark'

        hover(Location(Screen.SCREEN_WIDTH, other_bookmarks_location_y))

        hover(Location(Screen.SCREEN_WIDTH, bookmark_location_y))

        right_click(pocket_bookmark_name_pattern, region=bookmark_region)

        bookmark_context_menu_opened = exists(bookmark_properties_item_pattern)
        assert bookmark_context_menu_opened is True, 'Bookmark context menu is properly displayed'

        click(bookmark_properties_item_pattern)

        location_field_reachable = exists(bookmark_location_field_pattern)
        assert location_field_reachable is True, 'Location field is reachable'

        location_field_location = find(bookmark_location_field_pattern)
        location_region = Region(location_field_location.x, location_field_location.y,
                                 Screen.SCREEN_WIDTH // 5, Screen.SCREEN_HEIGHT // 10)

        tags_edited = exists(pocket_url_saved_pattern, region=location_region)
        assert tags_edited is True, 'Location is changed'

        tags_field_reachable = exists(tags_field_pattern)
        assert tags_field_reachable is True, 'Tags field is reachable'

        tags_field_location = find(tags_field_pattern)
        tags_region = Region(tags_field_location.x, tags_field_location.y, Screen.SCREEN_WIDTH // 10,
                             Screen.SCREEN_HEIGHT // 10)

        tags_edited = exists(tag_bookmark_saved_pattern, region=tags_region)
        assert tags_edited is True, 'Tags are edited'

        keywords_field_reachable = exists(keyword_field_pattern)
        assert keywords_field_reachable is True, 'Keywords field is reachable'

        keywords_field_location = find(keyword_field_pattern)
        keywords_region = Region(keywords_field_location.x, keywords_field_location.y,
                                 Screen.SCREEN_WIDTH // 10, Screen.SCREEN_HEIGHT // 10)
        keywords_edited = exists(test_keyword_saved_pattern, region=keywords_region)
        assert keywords_edited is True, 'Keywords are edited'

        type(Key.ESC)

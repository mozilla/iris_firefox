# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Add a new bookmark in \'Other Bookmarks\' section form Bookmarks menu',
        locale=['en-US'],
        test_case_id='163212',
        test_suite_id='2525',
        exclude=OSPlatform.MAC
    )
    def run(self, firefox):
        # open_firefox_menu() is not working
        bookmarks_top_menu_pattern = Pattern('bookmarks_top_menu.png')
        empty_folder_stub_pattern = Pattern('empty_folder.png')
        added_bookmark_pattern = Pattern('manually_added_bookmark_top_menu.png')
        name_bookmark_field_pattern = Pattern('name_bookmark_field.png')
        new_bookmark_item_top_menu_pattern = Pattern('new_bookmark_item_top_menu.png')
        other_bookmarks_item_pattern = Pattern('other_bookmarks.png')

        open_firefox_menu()

        firefox_menu_opened = exists(bookmarks_top_menu_pattern)
        assert firefox_menu_opened is True, 'Firefox menu is opened'

        click(bookmarks_top_menu_pattern)

        bookmarks_menu_displayed = exists(other_bookmarks_item_pattern)
        assert bookmarks_menu_displayed is True, 'Bookmarks menu is displayed'

        click(other_bookmarks_item_pattern)

        other_bookmarks_empty = exists(empty_folder_stub_pattern)
        assert other_bookmarks_empty is True, 'No bookmarks are saved in \'Other bookmarks\''

        right_click(empty_folder_stub_pattern)

        context_menu_displayed = exists(new_bookmark_item_top_menu_pattern)
        assert context_menu_displayed is True, 'Context menu for bookmark top menu item is displayed'

        click(new_bookmark_item_top_menu_pattern)

        form_appeared = exists(name_bookmark_field_pattern)
        assert form_appeared is True, 'Bookmark creation form is opened'

        click(name_bookmark_field_pattern)

        paste('FIREFOX_TEST_SITE')
        type(Key.TAB)
        paste(LocalWeb.FIREFOX_TEST_SITE)
        type(Key.TAB)
        paste('tag')
        type(Key.TAB)
        type(Key.TAB)
        paste('kw')
        type(Key.ENTER)

        restore_firefox_focus()

        open_firefox_menu()

        firefox_menu_reopened = exists(bookmarks_top_menu_pattern)
        assert firefox_menu_reopened is True, 'Firefox menu is reopened'

        click(bookmarks_top_menu_pattern)

        bookmarks_menu_displayed_again = exists(other_bookmarks_item_pattern)
        assert bookmarks_menu_displayed_again is True, 'Bookmarks menu is displayed second time'

        click(other_bookmarks_item_pattern)

        bookmark_saved = exists(added_bookmark_pattern)
        assert bookmark_saved is True, 'Manually added bookmark is saved'

        try:
            click(NavBar.HAMBURGER_MENU)
        except FindError:
            raise FindError('No Hamburger menu button found')

        restore_firefox_focus()

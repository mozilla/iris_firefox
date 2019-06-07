# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Add a new Folder in \'Other Bookmarks\' section form Bookmarks menu',
        locale=['en-US'],
        test_case_id='163213',
        test_suite_id='2525',
        profile=Profiles.TEN_BOOKMARKS,
        exclude=OSPlatform.MAC
    )
    def run(self, firefox):
        add_button_pattern = Pattern('add_button.png')
        bookmarks_top_menu_pattern = Pattern('bookmarks_top_menu.png')
        firefox_bookmark_top_menu_pattern = Pattern('firefox_bookmark_top_menu.png')
        folder_bookmarks_top_menu_pattern = Pattern('folder_bookmarks_top_menu.png')
        other_bookmarks_top_menu_pattern = Pattern('other_bookmarks.png')
        name_bookmark_field_pattern = Pattern('name_bookmark_field.png')
        new_folder_pattern = Pattern('new_folder.png')

        open_firefox_menu()

        firefox_menu_opened = exists(bookmarks_top_menu_pattern)
        assert firefox_menu_opened is True, 'Firefox menu is displayed'

        click(bookmarks_top_menu_pattern)

        bookmarks_menu_opened = exists(other_bookmarks_top_menu_pattern)
        assert bookmarks_menu_opened is True, 'Bookmarks top menu is displayed'

        click(other_bookmarks_top_menu_pattern)

        bookmarks_displayed = exists(firefox_bookmark_top_menu_pattern)
        assert bookmarks_displayed is True, 'Previously saved bookmarks are saved'

        other_bookmarks_item_y = find(other_bookmarks_top_menu_pattern).y
        firefox_bookmark_item_y = find(firefox_bookmark_top_menu_pattern).y

        hover(Location(Screen.SCREEN_WIDTH, other_bookmarks_item_y))
        hover(Location(Screen.SCREEN_WIDTH, firefox_bookmark_item_y))

        right_click(firefox_bookmark_top_menu_pattern)

        context_menu_displayed = exists(new_folder_pattern)
        assert context_menu_displayed is True, 'Context menu for bookmarks is displayed'

        click(new_folder_pattern)

        form_window_displayed = exists(name_bookmark_field_pattern)
        assert form_window_displayed is True, 'Folder creation form properly displayed.'

        add_button_displayed = exists(add_button_pattern)
        assert add_button_displayed is True, '"Add" button displayed'

        click(name_bookmark_field_pattern)

        paste('folder')

        add_button_displayed = exists(add_button_pattern)
        assert add_button_displayed is True, '"Add" button displayed'

        click(add_button_pattern)

        restore_firefox_focus()

        open_firefox_menu()

        firefox_menu_opened = exists(bookmarks_top_menu_pattern)
        assert firefox_menu_opened is True, 'Firefox menu is displayed'

        click(bookmarks_top_menu_pattern)

        bookmarks_menu_opened = exists(other_bookmarks_top_menu_pattern)
        assert bookmarks_menu_opened is True, 'Bookmarks top menu is displayed'

        click(other_bookmarks_top_menu_pattern)

        folder_saved = exists(folder_bookmarks_top_menu_pattern)
        assert folder_saved is True, 'The new folder is available in the Other Bookmarks section.'

        click(NavBar.HAMBURGER_MENU)

        restore_firefox_focus()

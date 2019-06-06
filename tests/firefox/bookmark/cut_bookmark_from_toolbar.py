# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Cut items from "Bookmarks Toolbar"',
        locale=['en-US'],
        test_case_id='164371',
        test_suite_id='2525',
        profile=Profiles.TEN_BOOKMARKS,
        exclude=OSPlatform.MAC
    )
    def run(self, firefox):
        bookmark_cut_pattern = Pattern('bookmark_cut.png').similar(0.9)
        open_bookmark_toolbar_pattern = Pattern('open_bookmark_toolbar.png')
        most_visited_pattern = Pattern('drag_area.png')
        new_folder_pattern = Pattern('new_folder.png')
        bookmarks_folder_pattern = Pattern('bookmarks_folder.png')
        cut_item_pattern = Pattern('cut_bookmark.png')
        paste_item_pattern = Pattern('paste_bookmark.png')
        getting_started_bookmark_pattern = Pattern('getting_started_in_toolbar.png')
        getting_started_bookmark_in_folder_pattern = Pattern('getting_started_bookmark_folder.png')
        bookmarks_top_menu_pattern = Pattern('bookmarks_top_menu.png')
        bookmark_toolbar_top_menu_pattern = Pattern('bookmark_toolbar_top_menu.png')
        folder_bookmarks_top_menu_pattern = Pattern('folder_bookmarks_top_menu.png')
        getting_started_top_menu_pattern = Pattern('getting_started_top_menu.png')
        name_bookmark_field_pattern = Pattern('name_bookmark_field.png')

        navbar_offset, _ = NavBar.HOME_BUTTON.get_size()
        navbar_offset *= 1.5
        right_click(NavBar.HOME_BUTTON.target_offset(navbar_offset, 0))
        click(open_bookmark_toolbar_pattern)

        bookmark_in_toolbar = exists(getting_started_bookmark_pattern)
        assert bookmark_in_toolbar is True, 'Bookmark is displayed in bookmark toolbar'

        right_click(most_visited_pattern)

        click(new_folder_pattern)

        time.sleep(0.5)  # Required for prompt window activating after rendering

        click(name_bookmark_field_pattern)

        edit_select_all()
        paste('folder')
        type(Key.ENTER)

        right_click(getting_started_bookmark_pattern)

        click(cut_item_pattern)

        bookmark_is_cut = exists(bookmark_cut_pattern)
        assert bookmark_is_cut is True, 'Bookmark displayed in toolbar as cut'

        click(bookmarks_folder_pattern)

        folder_dropdown_offset_x, folder_dropdown_offset_y = bookmarks_folder_pattern.get_size()
        folder_dropdown_offset_x //= 2
        folder_dropdown_offset_y *= 1.5

        right_click(bookmarks_folder_pattern.target_offset(folder_dropdown_offset_x, folder_dropdown_offset_y))

        click(paste_item_pattern)

        restore_firefox_focus()

        bookmark_removed_from_toolbar = not exists(getting_started_bookmark_pattern)
        assert bookmark_removed_from_toolbar is True, 'The bookmark is moved from toolbar'

        click(bookmarks_folder_pattern)

        bookmark_in_folder = exists(getting_started_bookmark_in_folder_pattern)
        assert bookmark_in_folder is True, 'Bookmark placed in folder now'
        restore_firefox_focus()

        if OSHelper.is_windows():
            type(Key.ALT)

            click(bookmarks_top_menu_pattern)

            click(bookmark_toolbar_top_menu_pattern)

            click(folder_bookmarks_top_menu_pattern)

            bookmark_displayed_in_top_menu = exists(getting_started_top_menu_pattern)
            assert bookmark_displayed_in_top_menu is True, 'Bookmark is displayed in top menu'

            right_click(getting_started_top_menu_pattern)

            click(cut_item_pattern)

            click(NavBar.HAMBURGER_MENU)

            restore_firefox_focus()

            right_click(most_visited_pattern)

            click(paste_item_pattern)

            bookmark_displayed_in_toolbar = exists(getting_started_bookmark_pattern)
            assert bookmark_displayed_in_toolbar is True, 'Bookmark is displayed in toolbar again'

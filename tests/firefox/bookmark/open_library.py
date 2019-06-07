# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Open Library',
        locale=['en-US'],
        test_case_id='169255',
        test_suite_id='2525'
    )
    def run(self, firefox):
        show_all_bookmarks_button_pattern = Pattern('show_all_bookmarks_button.png')  # Should be added to library_menu
        firefox_menu_bookmarks_pattern = Pattern('firefox_menu_bookmarks.png')
        wiki_bookmark_logo_pattern = Pattern('wiki_bookmark_logo.png')
        if OSHelper.is_linux() or OSHelper.is_mac():
            ff_menu_show_all_bookmarks_pattern = Pattern('ff_menu_show_all_bookmarks.png')

        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)

        soap_wiki_opened = exists(LocalWeb.SOAP_WIKI_SOAP_LABEL, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert soap_wiki_opened is True, 'The Wiki page is opened'

        bookmark_page()

        star_dialog_opened = exists(Bookmarks.StarDialog.DONE)
        assert star_dialog_opened is True, 'StarDialog opened'

        click(Bookmarks.StarDialog.DONE)

        new_tab()

        open_library()

        library_opened_vis_shortcut = exists(Library.TITLE)
        assert library_opened_vis_shortcut is True, 'Library opened via CMD/CTRL+Shift+B'

        other_bookmarks_folder_displayed = exists(Library.OTHER_BOOKMARKS)
        assert other_bookmarks_folder_displayed is True, 'Other Bookmarks folder displayed'

        click(Library.OTHER_BOOKMARKS)

        other_bookmarks_is_default_shortcut = exists(wiki_bookmark_logo_pattern)
        assert other_bookmarks_is_default_shortcut is True, 'Other Bookmarks is set as default'

        close_window_control('auxiliary')

        library_menu_button_displayed = exists(NavBar.LIBRARY_MENU)
        assert library_menu_button_displayed is True, 'Library menu button displayed'

        click(NavBar.LIBRARY_MENU)

        bookmarks_option_displayed = exists(LibraryMenu.BOOKMARKS_OPTION)
        assert bookmarks_option_displayed is True, 'Bookmarks option displayed'

        click(LibraryMenu.BOOKMARKS_OPTION)

        show_all_bookmarks_button_displayed = exists(show_all_bookmarks_button_pattern)
        assert show_all_bookmarks_button_displayed is True, 'Bookmarks option displayed'

        click(show_all_bookmarks_button_pattern)

        library_opened_from_menu = exists(Library.TITLE)
        assert library_opened_from_menu is True, 'Library opened from View History, saved bookmarks and more'

        click(Library.OTHER_BOOKMARKS)

        other_bookmarks_is_default_shortcut = exists(wiki_bookmark_logo_pattern)
        assert other_bookmarks_is_default_shortcut is True, 'Other Bookmarks is set as default'

        close_window_control('auxiliary')

        restore_firefox_focus()

        open_firefox_menu()

        firefox_menu_bookmarks_exists = exists(firefox_menu_bookmarks_pattern)
        assert firefox_menu_bookmarks_exists is True, 'Firefox menu > Bookmarks exists'

        click(firefox_menu_bookmarks_pattern)

        if OSHelper.is_linux() or OSHelper.is_mac():
            ff_menu_show_all_bookmarks_exists = exists(ff_menu_show_all_bookmarks_pattern)
            assert ff_menu_show_all_bookmarks_exists is True, 'Firefox menu > Bookmarks > Show All Bookmarks exists'

            click(ff_menu_show_all_bookmarks_pattern)
        else:
            ff_menu_show_all_bookmarks_exists = exists(show_all_bookmarks_button_pattern)
            assert ff_menu_show_all_bookmarks_exists is True, 'Firefox menu > Bookmarks > Show All Bookmarks exists'

            click(show_all_bookmarks_button_pattern)

        library_opened_from_ff_menu = exists(Library.TITLE)
        assert library_opened_from_ff_menu is True, 'Library opened from View History, saved bookmarks and more'

        click(Library.OTHER_BOOKMARKS)

        other_bookmarks_is_default_shortcut = exists(wiki_bookmark_logo_pattern)
        assert other_bookmarks_is_default_shortcut is True, 'Other Bookmarks is set as default'

        close_window_control('auxiliary')

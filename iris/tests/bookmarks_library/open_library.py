# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = "Open Library"
        self.test_case_id = "169255"
        self.test_suite_id = "2525"
        self.locale = ["en-US"]

    def run(self):
        show_all_bookmarks_button_pattern = Pattern('show_all_bookmarks_button.png')  # Should be added to library_menu
        ff_menu_show_all_bookmarks_pattern = Pattern('ff_menu_show_all_bookmarks.png')
        firefox_menu_bookmarks_pattern = Pattern('firefox_menu_bookmarks.png')
        wiki_bookmark_logo_pattern = Pattern('wiki_bookmark_logo.png')

        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)

        soap_wiki_opened = exists(LocalWeb.SOAP_WIKI_SOAP_LABEL, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, soap_wiki_opened, 'The Wiki page is opened')

        bookmark_page()
        click(Bookmarks.StarDialog.DONE)

        new_tab()

        open_library()

        library_opened_vis_shortcut = exists(Library.TITLE)
        assert_true(self, library_opened_vis_shortcut, 'Library opened via CMD/CTRL+Shift+B')

        click(Library.OTHER_BOOKMARKS)

        other_bookmarks_is_default_shortcut = exists(wiki_bookmark_logo_pattern)
        assert_true(self, other_bookmarks_is_default_shortcut, 'Other Bookmarks is set as default')

        close_window_control('auxiliary')

        click(NavBar.LIBRARY_MENU)
        time.sleep(DEFAULT_UI_DELAY)
        click(LibraryMenu.BOOKMARKS_OPTION)
        time.sleep(DEFAULT_UI_DELAY)
        click(show_all_bookmarks_button_pattern)

        library_opened_from_menu = exists(Library.TITLE)
        assert_true(self, library_opened_from_menu, 'Library opened from View History, saved bookmarks and more')

        click(Library.OTHER_BOOKMARKS)

        other_bookmarks_is_default_shortcut = exists(wiki_bookmark_logo_pattern)
        assert_true(self, other_bookmarks_is_default_shortcut, 'Other Bookmarks is set as default')

        close_window_control('auxiliary')

        location_to_hover = Location(0, 100)

        hover(location_to_hover)
        key_down(Key.ALT)
        time.sleep(DEFAULT_FX_DELAY)
        key_up(Key.ALT)
        click(firefox_menu_bookmarks_pattern)
        time.sleep(DEFAULT_UI_DELAY)
        click(ff_menu_show_all_bookmarks_pattern)

        library_opened_from_ff_menu = exists(Library.TITLE)
        assert_true(self, library_opened_from_ff_menu, 'Library opened from View History, saved bookmarks and more')

        click(Library.OTHER_BOOKMARKS)

        other_bookmarks_is_default_shortcut = exists(wiki_bookmark_logo_pattern)
        assert_true(self, other_bookmarks_is_default_shortcut, 'Other Bookmarks is set as default')

        close_window_control('auxiliary')

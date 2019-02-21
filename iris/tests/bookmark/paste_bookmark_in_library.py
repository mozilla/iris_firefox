# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Copy a bookmark from Library '
        self.test_case_id = '169265'
        self.test_suite_id = '2525'
        self.locales = ['en-US']

    def run(self):
        soap_wiki_tab_pattern = Pattern('soap_wiki_tab.png')
        copy_option_pattern = Pattern('copy_option.png')
        paste_option_pattern = Pattern('paste_option.png')
        toolbar_bookmarks_toolbar_pattern = Pattern('toolbar_bookmarks_toolbar.png')

        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)

        soap_wiki_opened = exists(soap_wiki_tab_pattern, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, soap_wiki_opened, 'Soap wiki page opened')

        location_for_click = find(NavBar.HOME_BUTTON).right(100)

        right_click(location_for_click)
        toolbar_bookmarks_button_displayed = exists(toolbar_bookmarks_toolbar_pattern)
        assert_true(self, toolbar_bookmarks_button_displayed, 'Bookmarks toolbar button displayed')
        click(toolbar_bookmarks_toolbar_pattern)

        bookmark_page()
        click(Bookmarks.StarDialog.PANEL_FOLDER_DEFAULT_OPTION.similar(.6), 0)
        wiki_bookmark_toolbar_folder_displayed = exists(Bookmarks.StarDialog.PANEL_OPTION_BOOKMARK_TOOLBAR.similar(.6))
        assert_true(self, wiki_bookmark_toolbar_folder_displayed, 'Bookmark toolbar folder displayed')
        click(Bookmarks.StarDialog.PANEL_OPTION_BOOKMARK_TOOLBAR.similar(.6))
        click(Bookmarks.StarDialog.DONE)

        wiki_bookmark_added = exists(soap_wiki_tab_pattern, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, wiki_bookmark_added, 'The Wikipedia bookmark is successfully added')

        new_tab()
        select_tab(1)
        close_tab()

        right_click(soap_wiki_tab_pattern)

        copy_option_exists = exists(copy_option_pattern)
        assert_true(self, copy_option_exists, 'Copy option exists')

        click(copy_option_pattern)

        right_click(location_for_click)
        toolbar_bookmarks_button_displayed = exists(toolbar_bookmarks_toolbar_pattern)
        assert_true(self, toolbar_bookmarks_button_displayed, 'Bookmarks toolbar button displayed')
        click(toolbar_bookmarks_toolbar_pattern)

        open_library()

        library_opened = exists(Library.TITLE, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, library_opened, 'Library opened')

        location_to_paste = find(Library.OTHER_BOOKMARKS).right(200)

        right_click(location_to_paste)

        paste_option_exists = exists(paste_option_pattern)
        assert_true(self, paste_option_exists, 'Paste option exists')

        click(paste_option_pattern)

        click(Library.OTHER_BOOKMARKS)

        bookmark_pasted = exists(soap_wiki_tab_pattern)
        assert_true(self, bookmark_pasted, 'Bookmark exists')

        click(Library.TITLE)
        close_window_control('auxiliary')

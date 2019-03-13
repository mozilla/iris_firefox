# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Paste a bookmark in Library'
        self.test_case_id = '169266'
        self.test_suite_id = '2525'
        self.locales = ['en-US']

    def run(self):
        soap_wiki_tab_pattern = Pattern('soap_wiki_tab.png')
        copy_option_pattern = Pattern('copy_option.png')
        paste_option_pattern = Pattern('paste_option.png')
        other_bookmarks_option_pattern = Bookmarks.StarDialog.PANEL_FOLDER_DEFAULT_OPTION.similar(.6)
        bookmarks_toolbar_option = Bookmarks.StarDialog.PANEL_OPTION_BOOKMARK_TOOLBAR.similar(.6)

        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)

        soap_wiki_opened = exists(soap_wiki_tab_pattern, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, soap_wiki_opened, 'The test page is opened')

        bookmark_page()

        done_button_exists = exists(Bookmarks.StarDialog.DONE)
        assert_true(self, done_button_exists, 'StarDialog is opened')

        click(Bookmarks.StarDialog.DONE, 0)

        bookmark_page()

        other_bookmarks_option_exists = exists(other_bookmarks_option_pattern)
        assert_true(self, other_bookmarks_option_exists, 'Other Bookmarks option exists')

        click(other_bookmarks_option_pattern, 0)

        wiki_bookmark_toolbar_folder_displayed = exists(bookmarks_toolbar_option)
        assert_true(self, wiki_bookmark_toolbar_folder_displayed, 'Bookmark toolbar folder displayed')

        click(bookmarks_toolbar_option)

        click(Bookmarks.StarDialog.DONE)

        new_tab()
        select_tab(1)
        close_tab()

        wiki_bookmark_added = exists(soap_wiki_tab_pattern, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, wiki_bookmark_added, 'The Wikipedia bookmark is successfully added')

        right_click(soap_wiki_tab_pattern)

        copy_option_exists = exists(copy_option_pattern)
        assert_true(self, copy_option_exists, 'Copy option exists')

        click(copy_option_pattern)

        open_library()

        library_opened = exists(Library.OTHER_BOOKMARKS, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, library_opened, 'Library opened')

        maximize_window_control('auxiliary')

        other_bookmarks_width, other_bookmarks_height = Library.OTHER_BOOKMARKS.get_size()
        location_to_paste = find(Library.OTHER_BOOKMARKS).right(other_bookmarks_width * 2)

        right_click(location_to_paste)

        paste_option_exists = exists(paste_option_pattern)
        assert_true(self, paste_option_exists, 'Paste option exists')

        click(paste_option_pattern)

        click(Library.OTHER_BOOKMARKS)

        bookmark_pasted = exists(soap_wiki_tab_pattern)
        assert_true(self, bookmark_pasted, 'Bookmark is correctly copied in the selected session')

        close_window_control('auxiliary')

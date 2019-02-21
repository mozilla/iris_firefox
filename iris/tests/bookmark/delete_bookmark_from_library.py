# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Delete a bookmark from Library '
        self.test_case_id = '169267'
        self.test_suite_id = '2525'
        self.locales = ['en-US']

    def run(self):
        soap_wiki_tab_pattern = Pattern('soap_wiki_tab.png')
        delete_bookmark_pattern = Pattern('delete_bookmark.png')

        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)

        soap_wiki_opened = exists(soap_wiki_tab_pattern, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, soap_wiki_opened, 'Soap wiki page opened')

        bookmark_page()

        stardialog_displayed = exists(Bookmarks.StarDialog.DONE, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, stardialog_displayed, 'Bookmark page dialog displayed')

        click(Bookmarks.StarDialog.DONE)

        new_tab()
        select_tab(1)
        close_tab()

        open_library()

        library_opened = exists(Library.TITLE, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, library_opened, 'Library opened')

        click(Library.OTHER_BOOKMARKS)

        wiki_bookmark_added = exists(soap_wiki_tab_pattern, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, wiki_bookmark_added, 'The Wikipedia bookmark is successfully added')

        right_click(soap_wiki_tab_pattern)

        delete_option_exists = exists(delete_bookmark_pattern)
        assert_true(self, delete_option_exists, 'Delete option exists')

        click(delete_bookmark_pattern)

        bookmark_deleted = exists(soap_wiki_tab_pattern)
        assert_false(self, bookmark_deleted, 'The bookmark is correctly deleted.')

        click(Library.TITLE)
        close_window_control('auxiliary')

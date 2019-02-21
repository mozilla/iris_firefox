# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Move a bookmark to another section with drag&drop in Library'
        self.test_case_id = '169270'
        self.test_suite_id = '2525'
        self.locales = ['en-US']

    def run(self):
        soap_wiki_tab_pattern = Pattern('soap_wiki_tab.png')
        bookmarks_highlighted_pattern = Pattern('bookmarks_highlighted.png')
        bookmarks_moved_pattern = Pattern('bookmarks_moved.png')

        navigate(LocalWeb.FIREFOX_TEST_SITE)

        soap_wiki_opened = exists(LocalWeb.FIREFOX_LOGO, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, soap_wiki_opened, 'Firefox Test page opened')

        bookmark_page()

        stardialog_displayed = exists(Bookmarks.StarDialog.DONE, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, stardialog_displayed, 'Bookmark page dialog displayed')

        click(Bookmarks.StarDialog.DONE)

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

        bookmark_exists = exists(soap_wiki_tab_pattern)
        assert_true(self, bookmark_exists, 'Bookmarks added')

        click(soap_wiki_tab_pattern)
        if Settings.is_mac():
            type('a', KeyModifier.CMD)
        else:
            type('a', KeyModifier.CTRL)

        bookmarks_highlighted = exists(bookmarks_highlighted_pattern)
        assert_true(self, bookmarks_highlighted, 'Bookmarks are highlighted')

        drag_drop(bookmarks_highlighted_pattern, Library.BOOKMARKS_TOOLBAR)

        click(Library.OTHER_BOOKMARKS)
        click(Library.BOOKMARKS_TOOLBAR)

        bookmarks_moved = exists(bookmarks_moved_pattern)
        assert_true(self, bookmarks_moved, 'The bookmark is correctly moved in the selected section.')

        click(Library.TITLE)
        close_window_control('auxiliary')

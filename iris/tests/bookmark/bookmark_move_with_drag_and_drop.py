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

        home_width, home_height = NavBar.HOME_BUTTON.get_size()
        tabs_region = Region(0, 0, SCREEN_WIDTH, home_height * 4)

        navigate(LocalWeb.FIREFOX_TEST_SITE)

        firefox_test_site_opened = exists(LocalWeb.FIREFOX_LOGO, Settings.SITE_LOAD_TIMEOUT)
        assert_true(self, firefox_test_site_opened, 'Firefox Test page opened')

        bookmark_page()

        stardialog_displayed = exists(Bookmarks.StarDialog.DONE, Settings.FIREFOX_TIMEOUT)
        assert_true(self, stardialog_displayed, 'Bookmark page dialog displayed')

        click(Bookmarks.StarDialog.DONE)

        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)

        soap_wiki_opened = exists(soap_wiki_tab_pattern, Settings.SITE_LOAD_TIMEOUT, tabs_region)
        assert_true(self, soap_wiki_opened, 'The test page is opened')

        bookmark_page()

        stardialog_displayed = exists(Bookmarks.StarDialog.DONE, Settings.FIREFOX_TIMEOUT)
        assert_true(self, stardialog_displayed, 'Bookmark page dialog displayed')

        click(Bookmarks.StarDialog.DONE)

        new_tab()
        select_tab(1)
        close_tab()

        open_library()

        library_opened = exists(Library.TITLE, Settings.FIREFOX_TIMEOUT)
        assert_true(self, library_opened, 'Library opened')

        other_bookmarks_folder_exists = exists(Library.OTHER_BOOKMARKS)
        assert_true(self, other_bookmarks_folder_exists, 'Other Bookmarks folder exists')

        click(Library.OTHER_BOOKMARKS)

        bookmark_exists = exists(soap_wiki_tab_pattern)
        assert_true(self, bookmark_exists, 'The Wikipedia bookmark is successfully added')

        click(soap_wiki_tab_pattern)

        if Settings.is_mac():
            type('a', KeyModifier.CMD)
        else:
            type('a', KeyModifier.CTRL)

        bookmarks_highlighted = exists(bookmarks_highlighted_pattern)
        assert_true(self, bookmarks_highlighted, 'Bookmarks are highlighted')

        bookmarks_toolbar_folder_exists = exists(Library.BOOKMARKS_TOOLBAR)
        assert_true(self, bookmarks_toolbar_folder_exists, 'Bookmarks toolbar folder exists')

        drag_drop(bookmarks_highlighted_pattern, Library.BOOKMARKS_TOOLBAR)

        click(Library.OTHER_BOOKMARKS)

        click(Library.BOOKMARKS_TOOLBAR)

        bookmarks_moved = exists(bookmarks_moved_pattern)
        assert_true(self, bookmarks_moved, 'Bookmarks are correctly moved in the selected section.')

        click(Library.TITLE)

        close_window_control('auxiliary')

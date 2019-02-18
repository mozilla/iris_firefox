# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Open a bookmark using \'Open\' option from Library'
        self.test_case_id = '169257'
        self.test_suite_id = '2525'
        self.locales = ['en-US']

    def run(self):
        soap_wiki_tab_pattern = Pattern('soap_wiki_tab.png')
        wiki_bookmark_logo_pattern = Pattern('wiki_bookmark_logo.png')

        home_width, home_height = NavBar.HOME_BUTTON.get_size()
        tabs_region = Region(0, 0, SCREEN_WIDTH, home_height * 4)

        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)

        soap_wiki_opened = exists(soap_wiki_tab_pattern, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, soap_wiki_opened, 'Soap wiki page opened')

        bookmark_page()

        stardialog_displayed = exists(Bookmarks.StarDialog.DONE, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, stardialog_displayed, 'Bookmark added')

        click(Bookmarks.StarDialog.DONE)

        new_tab()
        select_tab(1)
        close_tab()

        open_library()

        library_opened = exists(Library.TITLE, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, library_opened, 'Library opened')

        click(Library.OTHER_BOOKMARKS)

        bookmark_exists = exists(wiki_bookmark_logo_pattern)
        assert_true(self, bookmark_exists, 'Bookmark exists')

        right_click(soap_wiki_tab_pattern)

        type(Key.DOWN)
        type(Key.DOWN)
        type(Key.ENTER)

        soap_wiki_opened_from_bookmarks = exists(soap_wiki_tab_pattern, DEFAULT_SITE_LOAD_TIMEOUT, tabs_region)
        assert_true(self, soap_wiki_opened_from_bookmarks, 'Soap wiki page opened with Open in a New Tab from Library')

        new_tab_exists = exists(Tabs.NEW_TAB_NOT_HIGHLIGHTED)
        assert_true(self, new_tab_exists, 'New tab displayed')

        open_library()

        click(Library.TITLE)
        close_window_control('auxiliary')


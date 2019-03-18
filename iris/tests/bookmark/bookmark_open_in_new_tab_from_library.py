# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Open a bookmark in a New Tab from Library '
        self.test_case_id = '169258'
        self.test_suite_id = '2525'
        self.locales = ['en-US']

    def run(self):
        soap_wiki_tab_pattern = Pattern('soap_wiki_tab.png')
        wiki_bookmark_logo_pattern = Pattern('wiki_bookmark_logo.png')
        open_in_new_tab_pattern = Pattern('open_in_new_tab.png')

        home_width, home_height = NavBar.HOME_BUTTON.get_size()
        tabs_region = Region(0, 0, SCREEN_WIDTH, home_height * 4)

        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)

        soap_wiki_opened = exists(soap_wiki_tab_pattern, DEFAULT_SITE_LOAD_TIMEOUT, tabs_region)
        assert_true(self, soap_wiki_opened, 'The test page is opened')

        bookmark_page()

        stardialog_displayed = exists(Bookmarks.StarDialog.DONE, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, stardialog_displayed, 'StarDialog opened')

        click(Bookmarks.StarDialog.DONE)

        new_tab()
        select_tab(1)
        close_tab()

        open_library()

        library_opened = exists(Library.TITLE, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, library_opened, 'Library opened')

        click(Library.OTHER_BOOKMARKS)

        bookmark_exists = exists(wiki_bookmark_logo_pattern)
        assert_true(self, bookmark_exists, 'Previously added bookmark exists in Library')

        right_click(soap_wiki_tab_pattern)

        open_in_new_tab_option_exists = exists(open_in_new_tab_pattern, DEFAULT_SHORT_FIREFOX_TIMEOUT)
        assert_true(self, open_in_new_tab_option_exists, 'Open in New Tab option exists')

        click(open_in_new_tab_pattern)

        soap_wiki_opened_from_bookmarks = exists(soap_wiki_tab_pattern, DEFAULT_SITE_LOAD_TIMEOUT, tabs_region)
        assert_true(self, soap_wiki_opened_from_bookmarks, 'The test page is downloaded')

        new_tab_exists = exists(Tabs.NEW_TAB_NOT_HIGHLIGHTED)
        assert_true(self, new_tab_exists, 'The selected bookmark page is opened in a new tab.')

        open_library()

        click(Library.TITLE)
        close_window_control('auxiliary')

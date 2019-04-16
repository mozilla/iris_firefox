# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Add a new bookmarks separator from Library '
        self.test_case_id = '169263'
        self.test_suite_id = '2525'
        self.locales = ['en-US']

    def run(self):
        soap_wiki_tab_pattern = Pattern('soap_wiki_tab.png')
        separator_added_pattern = Pattern('separator_added_to_library.png')

        navigate(LocalWeb.FIREFOX_TEST_SITE)

        soap_wiki_opened = exists(LocalWeb.FIREFOX_LOGO, Settings.SITE_LOAD_TIMEOUT)
        assert_true(self, soap_wiki_opened, 'Firefox Test page is opened')

        bookmark_page()

        stardialog_displayed = exists(Bookmarks.StarDialog.DONE, Settings.FIREFOX_TIMEOUT)
        assert_true(self, stardialog_displayed, 'StarDialog displayed')

        click(Bookmarks.StarDialog.DONE)

        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)

        soap_wiki_opened = exists(soap_wiki_tab_pattern, Settings.SITE_LOAD_TIMEOUT)
        assert_true(self, soap_wiki_opened, 'Soap wiki page opened')

        bookmark_page()

        stardialog_displayed = exists(Bookmarks.StarDialog.DONE, Settings.FIREFOX_TIMEOUT)
        assert_true(self, stardialog_displayed, 'StarDialog displayed')

        click(Bookmarks.StarDialog.DONE)

        new_tab()
        select_tab(1)
        close_tab()

        open_library()

        library_opened = exists(Library.TITLE, Settings.FIREFOX_TIMEOUT)
        assert_true(self, library_opened, 'The Library is opened')

        click(Library.OTHER_BOOKMARKS)

        bookmark_exists = exists(soap_wiki_tab_pattern)
        assert_true(self, bookmark_exists, 'Previously added bookmarks are displayed')

        right_click(soap_wiki_tab_pattern)

        new_bookmark_option_exists = exists(Library.Organize.NEW_SEPARATOR)
        assert_true(self, new_bookmark_option_exists, 'New Separator option exists')

        click(Library.Organize.NEW_SEPARATOR)

        separator_added = exists(separator_added_pattern)
        assert_true(self, separator_added, 'A new separator is displayed above the selected bookmark.')

        click(Library.TITLE)

        close_window_control('auxiliary')

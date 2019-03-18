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
        bookmark_pasted_pattern = Pattern('bookmark_pasted.png')

        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)

        soap_wiki_opened = exists(soap_wiki_tab_pattern, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, soap_wiki_opened, 'The test page is opened')

        bookmark_page()

        stardialog_displayed = exists(Bookmarks.StarDialog.DONE, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, stardialog_displayed, 'Stardialog displayed')

        click(Bookmarks.StarDialog.DONE)

        new_tab()
        select_tab(1)
        close_tab()

        open_library()

        library_opened = exists(Library.OTHER_BOOKMARKS, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, library_opened, 'Library opened')

        click(Library.OTHER_BOOKMARKS)

        bookmark_exists = exists(soap_wiki_tab_pattern)
        assert_true(self, bookmark_exists, 'Previously added bookmarks are displayed')

        right_click(soap_wiki_tab_pattern)

        copy_option_exists = exists(copy_option_pattern)
        assert_true(self, copy_option_exists, 'Copy option exists')

        click(copy_option_pattern)

        bookmarks_toolbar_folder_exists = exists(Library.BOOKMARKS_TOOLBAR)
        assert_true(self, bookmarks_toolbar_folder_exists, 'Bookmarks toolbar folder exists')

        click(Library.BOOKMARKS_TOOLBAR)

        other_bookmarks_width, other_bookmarks_height = Library.OTHER_BOOKMARKS.get_size()
        location_to_paste = find(Library.OTHER_BOOKMARKS).right(other_bookmarks_width * 2)

        right_click(location_to_paste)

        paste_option_exists = exists(paste_option_pattern)
        assert_true(self, paste_option_exists, 'Paste option exists')

        click(paste_option_pattern)

        bookmark_pasted = exists(bookmark_pasted_pattern)
        assert_true(self, bookmark_pasted, 'The file from the previous step is pasted in the selected section')

        click(Library.OTHER_BOOKMARKS)

        bookmark_not_deleted = exists(soap_wiki_tab_pattern)
        assert_true(self, bookmark_not_deleted, 'The file from the previous step is pasted in the selected section '
                                                'without being deleted from the previous one')

        click(Library.TITLE)
        close_window_control('auxiliary')

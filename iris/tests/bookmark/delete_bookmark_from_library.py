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

        stardialog_region = Region(SCREEN_WIDTH / 2, 0, SCREEN_WIDTH / 2, SCREEN_HEIGHT)

        home_width, home_height = NavBar.HOME_BUTTON.get_size()
        tabs_region = Region(0, 0, SCREEN_WIDTH, home_height * 4)

        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)

        soap_wiki_opened = exists(soap_wiki_tab_pattern, Settings.SITE_LOAD_TIMEOUT, tabs_region)
        assert_true(self, soap_wiki_opened, 'Soap wiki page opened')

        bookmark_page()

        stardialog_displayed = exists(Bookmarks.StarDialog.DONE, Settings.FIREFOX_TIMEOUT, stardialog_region)
        assert_true(self, stardialog_displayed, 'Bookmark page dialog displayed')

        click(Bookmarks.StarDialog.DONE, 0, stardialog_region)

        new_tab()
        select_tab(1)
        close_tab()

        open_library()

        library_opened = exists(Library.TITLE, Settings.FIREFOX_TIMEOUT)
        assert_true(self, library_opened, 'Library opened')

        other_bookmarks_exists = exists(Library.OTHER_BOOKMARKS)
        assert_true(self, other_bookmarks_exists, 'The Other Bookmarks folder exists')

        click(Library.OTHER_BOOKMARKS)

        wiki_bookmark_added = exists(soap_wiki_tab_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, wiki_bookmark_added, 'The Wikipedia bookmark is successfully added')

        right_click(soap_wiki_tab_pattern)

        delete_option_exists = exists(delete_bookmark_pattern)
        assert_true(self, delete_option_exists, 'Delete option exists')

        click(delete_bookmark_pattern)

        try:
            bookmark_deleted = wait_vanish(soap_wiki_tab_pattern)
            assert_true(self, bookmark_deleted, 'The bookmark is correctly deleted.')
        except FindError:
            raise FindError('The bookmark is not deleted.')

        click(Library.TITLE)

        close_window_control('auxiliary')

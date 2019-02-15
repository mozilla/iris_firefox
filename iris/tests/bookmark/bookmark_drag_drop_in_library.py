# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Bookmark a page by drag&drop in Library.'
        self.test_case_id = '169274'
        self.test_suite_id = '2525'
        self.locales = ['en-US']

    def run(self):
        soap_wiki_tab_pattern = Pattern('soap_wiki_tab.png')
        wiki_bookmark_logo_pattern = Pattern('wiki_bookmark_logo.png')

        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)

        soap_wiki_opened = exists(soap_wiki_tab_pattern, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, soap_wiki_opened, 'Soap wiki page opened')

        point_to_move_wiki_window = find(soap_wiki_tab_pattern).right(400)
        location_to_shift_wiki_window = find(soap_wiki_tab_pattern).right(SCREEN_WIDTH)

        drag_drop(point_to_move_wiki_window, location_to_shift_wiki_window)

        open_library()

        library_opened = exists(Library.TITLE, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, library_opened, 'Library opened')

        lib_loc = find(Library.OTHER_BOOKMARKS).right(300)

        drag_drop(soap_wiki_tab_pattern, lib_loc)

        bookmark_added = exists(wiki_bookmark_logo_pattern)
        assert_true(self, bookmark_added, 'Bookmark added')

        click(Library.TITLE)
        close_window_control('auxiliary')


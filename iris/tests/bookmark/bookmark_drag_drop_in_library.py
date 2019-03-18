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

        home_button_exists = exists(NavBar.HOME_BUTTON)
        assert_true(self, home_button_exists, 'Home button exists')

        home_height, home_width = NavBar.HOME_BUTTON.get_size()
        tabs_region = Region(0, 0, SCREEN_WIDTH, home_height * 4)

        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)

        soap_wiki_opened = exists(soap_wiki_tab_pattern, DEFAULT_SITE_LOAD_TIMEOUT, tabs_region)
        assert_true(self, soap_wiki_opened, 'Soap wiki page opened')

        point_to_move_wiki_window = find(soap_wiki_tab_pattern, tabs_region).right(SCREEN_WIDTH/5)
        location_to_shift_wiki_window = find(soap_wiki_tab_pattern, tabs_region).right(SCREEN_WIDTH)

        drag_drop(point_to_move_wiki_window, location_to_shift_wiki_window)

        open_library()

        library_opened = exists(Library.TITLE, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, library_opened, 'Library opened')

        other_bookmarks_folder_exists = exists(Library.OTHER_BOOKMARKS)
        assert_true(self, other_bookmarks_folder_exists, 'Other bookmarks folder exists')

        other_bookmarks_width, other_bookmarks_height = Library.OTHER_BOOKMARKS.get_size()
        other_bookmarks_location = find(Library.OTHER_BOOKMARKS).right(other_bookmarks_width * 3)

        drag_drop(soap_wiki_tab_pattern, other_bookmarks_location)

        bookmark_added = exists(wiki_bookmark_logo_pattern)
        assert_true(self, bookmark_added, 'Bookmark added')

        click(Library.TITLE)
        close_window_control('auxiliary')

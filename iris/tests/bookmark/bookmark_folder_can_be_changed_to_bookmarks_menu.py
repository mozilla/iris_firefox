# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Bookmark folders can be changed in Bookmarks Menu'
        self.test_case_id = '163402'
        self.test_suite_id = '2525'
        self.locales = ['en-US']

    def run(self):
        soap_wiki_tab_pattern = Pattern('soap_wiki_tab.png')

        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)

        soap_wiki_opened = exists(soap_wiki_tab_pattern, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, soap_wiki_opened, 'Soap wiki page opened')

        stardialog_region = Region(SCREEN_WIDTH / 2, 0, SCREEN_WIDTH / 2, SCREEN_HEIGHT)

        bookmark_page()

        stardialog_displayed = exists(Bookmarks.StarDialog.DONE, DEFAULT_FIREFOX_TIMEOUT, stardialog_region)
        assert_true(self, stardialog_displayed, 'Bookmark page dialog displayed')

        click(Bookmarks.StarDialog.DONE, in_region=stardialog_region)

        restore_firefox_focus()

        click(LocationBar.STAR_BUTTON_STARRED, in_region=stardialog_region)

        edit_stardialog_displayed = exists(Bookmarks.StarDialog.EDIT_THIS_BOOKMARK, DEFAULT_FIREFOX_TIMEOUT,
                                           in_region=stardialog_region)
        assert_true(self, edit_stardialog_displayed, 'The Edit This Bookmark popup is displayed under the star-shaped '
                                                     'icon.')

        click(Bookmarks.StarDialog.PANEL_FOLDER_DEFAULT_OPTION.similar(.6), 0, stardialog_region)
        wiki_bookmark_menu_folder_displayed = exists(Bookmarks.StarDialog.PANEL_OPTION_BOOKMARK_MENU.similar(.6),
                                                     in_region=stardialog_region)
        assert_true(self, wiki_bookmark_menu_folder_displayed, 'Bookmark toolbar folder displayed')
        click(Bookmarks.StarDialog.PANEL_OPTION_BOOKMARK_MENU.similar(.6), in_region=stardialog_region)
        click(Bookmarks.StarDialog.DONE)

        bookmarks_sidebar('open')

        bookmarks_sidebar_location = find(Sidebar.BookmarksSidebar.SIDEBAR_BOOKMARKS_TITLE)
        bookmarks_width, bookmarks_height = Sidebar.BookmarksSidebar.SIDEBAR_BOOKMARKS_TITLE.get_size()
        bookmarks_sidebar_region = Region(0,
                                          bookmarks_sidebar_location.y,
                                          bookmarks_width * 2,
                                          SCREEN_HEIGHT / 2)

        bookmarks_menu_folder_exists = exists(SidebarBookmarks.BOOKMARKS_MENU, DEFAULT_FIREFOX_TIMEOUT,
                                              bookmarks_sidebar_region)
        assert_true(self, bookmarks_menu_folder_exists, 'Bookmarks menu folder exists')

        click(SidebarBookmarks.BOOKMARKS_MENU, in_region=bookmarks_sidebar_region)

        wiki_bookmark_moved = exists(soap_wiki_tab_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, wiki_bookmark_moved, 'The pop up is dismissed and the bookmark is correctly saved in '
                                               'Bookmarks menu.')




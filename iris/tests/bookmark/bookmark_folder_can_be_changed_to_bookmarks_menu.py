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

    def setup(self):
        BaseTest.setup(self)
        self.profile = Profile.TEN_BOOKMARKS
        return

    def run(self):
        navigate(LocalWeb.FOCUS_TEST_SITE)

        test_site_opened = exists(LocalWeb.FOCUS_LOGO, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, test_site_opened, 'Previously bookmarked Focus website is opened')

        stardialog_region = Region(SCREEN_WIDTH / 2, 0, SCREEN_WIDTH / 2, SCREEN_HEIGHT)

        star_button_exists = exists(LocationBar.STAR_BUTTON_STARRED)
        assert_true(self, star_button_exists, 'Star button is displayed')

        click(LocationBar.STAR_BUTTON_STARRED, in_region=stardialog_region)

        edit_stardialog_displayed = exists(Bookmarks.StarDialog.EDIT_THIS_BOOKMARK, DEFAULT_FIREFOX_TIMEOUT,
                                           in_region=stardialog_region)
        assert_true(self, edit_stardialog_displayed, 'The Edit This Bookmark popup is displayed under the star-shaped '
                                                     'icon.')

        panel_folder_default_option_exists = exists(Bookmarks.StarDialog.PANEL_FOLDER_DEFAULT_OPTION.similar(.6),
                                                    in_region=stardialog_region)
        assert_true(self, panel_folder_default_option_exists, 'Panel folder default option exists')

        click(Bookmarks.StarDialog.PANEL_FOLDER_DEFAULT_OPTION.similar(.6), 0, stardialog_region)

        bookmark_menu_folder_displayed = exists(Bookmarks.StarDialog.PANEL_OPTION_BOOKMARK_MENU.similar(.6),
                                                in_region=stardialog_region)
        assert_true(self, bookmark_menu_folder_displayed, 'Bookmark menu folder displayed')

        click(Bookmarks.StarDialog.PANEL_OPTION_BOOKMARK_MENU.similar(.6), in_region=stardialog_region)

        stardialog_done_button_displayed = exists(Bookmarks.StarDialog.DONE, in_region=stardialog_region)
        assert_true(self, stardialog_done_button_displayed, 'Stardialog Done button is displayed')

        click(Bookmarks.StarDialog.DONE)

        home_button_displayed = exists(NavBar.HOME_BUTTON)
        assert_true(self, home_button_displayed, 'Home button is displayed')

        bookmarks_sidebar('open')

        bookmarks_sidebar_location = find(Sidebar.BookmarksSidebar.SIDEBAR_BOOKMARKS_TITLE)
        bookmarks_width, bookmarks_height = Sidebar.BookmarksSidebar.SIDEBAR_BOOKMARKS_TITLE.get_size()
        bookmarks_sidebar_region = Region(0, bookmarks_sidebar_location.y, bookmarks_width * 2, SCREEN_HEIGHT / 2)

        bookmarks_menu_folder_exists = exists(SidebarBookmarks.BOOKMARKS_MENU, DEFAULT_FIREFOX_TIMEOUT,
                                              bookmarks_sidebar_region)
        assert_true(self, bookmarks_menu_folder_exists, 'Bookmarks menu folder exists')

        click(SidebarBookmarks.BOOKMARKS_MENU, in_region=bookmarks_sidebar_region)

        bookmark_moved = exists(LocalWeb.FOCUS_BOOKMARK_SMALL, DEFAULT_FIREFOX_TIMEOUT, bookmarks_sidebar_region)
        assert_true(self, bookmark_moved, 'The pop up is dismissed and the bookmark is correctly saved in '
                                          'Bookmarks menu.')

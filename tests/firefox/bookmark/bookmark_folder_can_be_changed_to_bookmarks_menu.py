# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Bookmark folders can be changed in Bookmarks Menu',
        locale=['en-US'],
        test_case_id='163402',
        test_suite_id='2525',
        profile=Profiles.TEN_BOOKMARKS,
    )
    def run(self, firefox):
        navigate(LocalWeb.FOCUS_TEST_SITE)

        test_site_opened = exists(LocalWeb.FOCUS_LOGO, FirefoxSettings.FIREFOX_TIMEOUT*3)
        assert test_site_opened is True, 'Previously bookmarked Focus website is opened'

        stardialog_region = Rectangle(Screen.SCREEN_WIDTH / 2, 0, Screen.SCREEN_WIDTH / 2, Screen.SCREEN_HEIGHT)

        star_button_exists = exists(LocationBar.STAR_BUTTON_STARRED)
        assert star_button_exists is True, 'Star button is displayed'

        click(LocationBar.STAR_BUTTON_STARRED, region=stardialog_region)

        edit_stardialog_displayed = exists(Bookmarks.StarDialog.EDIT_THIS_BOOKMARK, FirefoxSettings.FIREFOX_TIMEOUT,
                                           region=stardialog_region)
        assert edit_stardialog_displayed is True, 'The Edit This Bookmark popup is displayed under the star-shaped ' \
                                                  'icon.'

        panel_folder_default_option_exists = exists(Bookmarks.StarDialog.PANEL_FOLDER_DEFAULT_OPTION.similar(.6),
                                                    region=stardialog_region)
        assert panel_folder_default_option_exists is True, 'Panel folder default option exists'

        click(Bookmarks.StarDialog.PANEL_FOLDER_DEFAULT_OPTION.similar(.6), 0, stardialog_region)

        bookmark_menu_folder_displayed = exists(Bookmarks.StarDialog.PANEL_OPTION_BOOKMARK_MENU.similar(.6),
                                                region=stardialog_region)
        assert bookmark_menu_folder_displayed, 'Bookmark menu folder displayed'

        click(Bookmarks.StarDialog.PANEL_OPTION_BOOKMARK_MENU.similar(.6), region=stardialog_region)

        stardialog_done_button_displayed = exists(Bookmarks.StarDialog.DONE, region=stardialog_region)
        assert stardialog_done_button_displayed is True, 'Stardialog Done button is displayed'

        click(Bookmarks.StarDialog.DONE)

        home_button_displayed = exists(NavBar.HOME_BUTTON)
        assert home_button_displayed is True, 'Home button is displayed'

        bookmarks_sidebar('open')

        bookmarks_sidebar_location = find(Sidebar.BookmarksSidebar.SIDEBAR_BOOKMARKS_TITLE)
        bookmarks_width, bookmarks_height = Sidebar.BookmarksSidebar.SIDEBAR_BOOKMARKS_TITLE.get_size()
        bookmarks_sidebar_region = Rectangle(0, bookmarks_sidebar_location.y, bookmarks_width * 2,
                                          Screen.SCREEN_HEIGHT / 2)

        bookmarks_menu_folder_exists = exists(SidebarBookmarks.BOOKMARKS_MENU, FirefoxSettings.FIREFOX_TIMEOUT,
                                              bookmarks_sidebar_region)
        assert bookmarks_menu_folder_exists is True, 'Bookmarks menu folder exists'

        click(SidebarBookmarks.BOOKMARKS_MENU, region=bookmarks_sidebar_region)

        bookmark_moved = exists(LocalWeb.FOCUS_BOOKMARK_SMALL, FirefoxSettings.FIREFOX_TIMEOUT, bookmarks_sidebar_region)
        assert bookmark_moved is True, 'The pop up is dismissed and the bookmark is correctly saved in ' \
                                       'Bookmarks menu.'

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Bookmark folders can be changed in Bookmarks Toolbar'
        self.test_case_id = '163401'
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
        wiki_bookmark_toolbar_folder_displayed = exists(Bookmarks.StarDialog.PANEL_OPTION_BOOKMARK_TOOLBAR.similar(.6),
                                                        in_region=stardialog_region)
        assert_true(self, wiki_bookmark_toolbar_folder_displayed, 'Bookmark toolbar folder displayed')
        click(Bookmarks.StarDialog.PANEL_OPTION_BOOKMARK_TOOLBAR.similar(.6), in_region=stardialog_region)
        click(Bookmarks.StarDialog.DONE)

        home_width, home_height = NavBar.HOME_BUTTON.get_size()
        bookmarks_toolbar_location = find(NavBar.HOME_BUTTON)
        bookmarks_toolbar_region = Region(0, bookmarks_toolbar_location.y, SCREEN_WIDTH, home_height * 3)

        soap_wiki_bookmark_folder_changed = exists(soap_wiki_tab_pattern, DEFAULT_SITE_LOAD_TIMEOUT,
                                                   bookmarks_toolbar_region)
        assert_true(self, soap_wiki_bookmark_folder_changed, 'The Bookmarks Toolbar is enabled and the saved bookmark '
                                                             'is correctly displayed.')


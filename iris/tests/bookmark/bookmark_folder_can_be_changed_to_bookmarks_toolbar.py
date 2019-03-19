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

        click(Bookmarks.StarDialog.PANEL_FOLDER_DEFAULT_OPTION.similar(.6), in_region=stardialog_region)

        bookmark_toolbar_folder_displayed = exists(Bookmarks.StarDialog.PANEL_OPTION_BOOKMARK_TOOLBAR.similar(.6),
                                                   in_region=stardialog_region)
        assert_true(self, bookmark_toolbar_folder_displayed, 'Bookmark toolbar folder displayed')

        click(Bookmarks.StarDialog.PANEL_OPTION_BOOKMARK_TOOLBAR.similar(.6), in_region=stardialog_region)

        stardialog_done_button_displayed = exists(Bookmarks.StarDialog.DONE, in_region=stardialog_region)
        assert_true(self, stardialog_done_button_displayed, 'Stardialog Done button is displayed')

        click(Bookmarks.StarDialog.DONE)

        home_button_displayed = exists(NavBar.HOME_BUTTON)
        assert_true(self, home_button_displayed, 'Home button is displayed')

        home_width, home_height = NavBar.HOME_BUTTON.get_size()
        bookmarks_toolbar_location = find(NavBar.HOME_BUTTON)
        bookmarks_toolbar_region = Region(0, bookmarks_toolbar_location.y, SCREEN_WIDTH, home_height * 4)

        test_bookmark_folder_changed = exists(LocalWeb.FOCUS_BOOKMARK.similar(0.6), DEFAULT_SITE_LOAD_TIMEOUT,
                                              bookmarks_toolbar_region)
        assert_true(self, test_bookmark_folder_changed, 'The Bookmarks Toolbar is enabled and the saved bookmark '
                                                        'is correctly displayed.')


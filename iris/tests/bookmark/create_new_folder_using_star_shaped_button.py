# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = '"Create" a new folder using star-shaped button '
        self.test_case_id = '163404'
        self.test_suite_id = '2525'
        self.locales = ['en-US']

    def setup(self):
        BaseTest.setup(self)
        self.profile = Profile.TEN_BOOKMARKS
        return

    def run(self):
        destination_folders_pattern = Pattern('destination_folders.png')
        new_folder_added_pattern = Pattern('new_folder_added.png')

        navigate(LocalWeb.FOCUS_TEST_SITE)

        test_site_opened = exists(LocalWeb.FOCUS_LOGO, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, test_site_opened, 'Previously bookmarked Focus website is opened')

        stardialog_region = Region(SCREEN_WIDTH / 2, 0, SCREEN_WIDTH / 2, SCREEN_HEIGHT)

        star_button_exists = exists(LocationBar.STAR_BUTTON_STARRED, in_region=stardialog_region)
        assert_true(self, star_button_exists, 'Star button is displayed')

        click(LocationBar.STAR_BUTTON_STARRED, in_region=stardialog_region)

        edit_stardialog_displayed = exists(Bookmarks.StarDialog.EDIT_THIS_BOOKMARK, DEFAULT_FIREFOX_TIMEOUT,
                                           in_region=stardialog_region)
        assert_true(self, edit_stardialog_displayed, 'The Edit This Bookmark popup is displayed under the star-shaped '
                                                     'icon.')

        other_bookmarks_default_option_exists = exists(Bookmarks.StarDialog.PANEL_FOLDER_DEFAULT_OPTION.similar(.6),
                                                       in_region=stardialog_region)
        assert_true(self, other_bookmarks_default_option_exists, 'The Other Bookmarks default folder option exists')

        click(Bookmarks.StarDialog.PANEL_FOLDER_DEFAULT_OPTION.similar(.6), 0, stardialog_region)

        choose_option_displayed = exists(Bookmarks.StarDialog.PANEL_OPTION_CHOOSE.similar(.6), DEFAULT_FIREFOX_TIMEOUT,
                                         in_region=stardialog_region)
        assert_true(self, choose_option_displayed, 'The \'Choose..\' option is displayed')

        click(Bookmarks.StarDialog.PANEL_OPTION_CHOOSE.similar(.6), in_region=stardialog_region)

        destination_folders_displayed = exists(destination_folders_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, destination_folders_displayed, 'Edit This Bookmark panel is displayed with all the '
                                                         'destination folders.')

        bookmarks_toolbar_folder_exists = exists(Bookmarks.StarDialog.PANEL_OPTION_BOOKMARK_TOOLBAR,
                                                 in_region=stardialog_region)
        assert_true(self, bookmarks_toolbar_folder_exists,'The Bookmarks toolbar folder exists')

        click(Bookmarks.StarDialog.PANEL_OPTION_BOOKMARK_TOOLBAR)

        new_folder_button_exists = exists(Bookmarks.StarDialog.NEW_FOLDER)
        assert_true(self, new_folder_button_exists, 'New folder button exists')

        click(Bookmarks.StarDialog.NEW_FOLDER)

        new_folder_created = exists(Bookmarks.StarDialog.NEW_FOLDER_CREATED)
        assert_true(self, new_folder_created, 'New folder created')

        done_button_exists = exists(Bookmarks.StarDialog.DONE)
        assert_true(self, done_button_exists, 'The Done button exists')

        click(Bookmarks.StarDialog.DONE)

        click(LocationBar.STAR_BUTTON_STARRED)

        folder_expander_exists = exists(Bookmarks.StarDialog.PANEL_FOLDERS_EXPANDER, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, folder_expander_exists, 'Folder expander exists')

        click(Bookmarks.StarDialog.PANEL_FOLDERS_EXPANDER)

        new_folder_added = exists(new_folder_added_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, new_folder_added, 'The folder is correctly saved and displayed in Bookmarks Menu.')

        restore_firefox_focus()

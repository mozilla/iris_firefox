# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = '"Choose..." another destination folder using star-shaped button '
        self.test_case_id = '163403'
        self.test_suite_id = '2525'
        self.locales = ['en-US']

    def setup(self):
        BaseTest.setup(self)
        self.profile = Profile.TEN_BOOKMARKS
        return

    def run(self):
        destination_folders_pattern = Pattern('destination_folders.png')

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

        click(Bookmarks.StarDialog.PANEL_FOLDER_DEFAULT_OPTION.similar(.6), 0, stardialog_region)

        choose_option_displayed = exists(Bookmarks.StarDialog.PANEL_OPTION_CHOOSE.similar(.6),
                                         in_region=stardialog_region)
        assert_true(self, choose_option_displayed, 'Bookmark toolbar folder displayed')

        click(Bookmarks.StarDialog.PANEL_OPTION_CHOOSE.similar(.6), in_region=stardialog_region)

        destination_folders_displayed = exists(destination_folders_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, destination_folders_displayed, 'Edit This Bookmark panel is displayed with all the '
                                                         'destination folders.')

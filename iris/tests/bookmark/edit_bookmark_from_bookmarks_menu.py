# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Edit a Bookmark from Bookmarks menu'
        self.test_case_id = '163195'
        self.test_suite_id = '2525'
        self.locales = ['en-US']

    def setup(self):
        BaseTest.setup(self)
        self.profile = Profile.TEN_BOOKMARKS
        return

    def run(self):
        firefox_menu_bookmarks_pattern = Pattern('firefox_menu_bookmarks.png')
        edit_this_bookmark_option_pattern = Pattern('edit_this_bookmark_option.png')

        navigate(LocalWeb.MOZILLA_TEST_SITE)

        test_site_opened = exists(LocalWeb.MOZILLA_LOGO, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, test_site_opened, 'Previously bookmarked Mozilla website is opened')

        open_firefox_menu()

        firefox_menu_bookmarks_exists = exists(firefox_menu_bookmarks_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, firefox_menu_bookmarks_exists, 'Firefox menu > Bookmarks exists')

        click(firefox_menu_bookmarks_pattern)

        edit_this_bookmark_option_exists = exists(edit_this_bookmark_option_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, edit_this_bookmark_option_exists, 'Edit This Bookmark option exists')

        click(edit_this_bookmark_option_pattern)

        edit_stardialog_displayed = exists(Bookmarks.StarDialog.EDIT_THIS_BOOKMARK, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, edit_stardialog_displayed, 'The Edit This Bookmark popup is displayed under the star-shaped '
                                                     'icon.')


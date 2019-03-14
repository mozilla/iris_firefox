# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = '"Edit this bookmark" panel appears after a page is already bookmarked'
        self.test_case_id = '163399'
        self.test_suite_id = '2525'
        self.locales = ['en-US']

    def setup(self):
        BaseTest.setup(self)
        self.profile = Profile.TEN_BOOKMARKS
        return

    def run(self):
        navigate(LocalWeb.MOZILLA_TEST_SITE)

        test_site_opened = exists(LocalWeb.MOZILLA_LOGO, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, test_site_opened, 'Previously bookmarked Mozilla website is opened')

        star_button_exists = exists(LocationBar.STAR_BUTTON_STARRED)
        assert_true(self, star_button_exists, 'Star button is displayed')

        click(LocationBar.STAR_BUTTON_STARRED)

        edit_stardialog_displayed = exists(Bookmarks.StarDialog.EDIT_THIS_BOOKMARK, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, edit_stardialog_displayed, 'The Edit This Bookmark popup is displayed under the star-shaped '
                                                     'icon.')

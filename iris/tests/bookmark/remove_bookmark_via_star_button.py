# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from iris.test_case import *


class Test(BaseTest):
    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Remove a bookmark using star-shaped button'
        self.test_case_id = '163407'
        self.test_suite_id = '2525'
        self.locales = ['en-US']

    def setup(self):
        BaseTest.setup(self)
        self.profile = Profile.TEN_BOOKMARKS

    def run(self):
        firefox_logo_pattern = LocalWeb.FIREFOX_LOGO
        blue_star_button_pattern = LocationBar.STAR_BUTTON_STARRED
        white_star_button_pattern = LocationBar.STAR_BUTTON_UNSTARRED
        edit_bookmark_pattern = Bookmarks.StarDialog.EDIT_THIS_BOOKMARK
        remove_button_pattern = Bookmarks.StarDialog.REMOVE_BOOKMARK

        navigate(LocalWeb.FIREFOX_TEST_SITE)
        firefox_logo_assert = exists(firefox_logo_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, firefox_logo_assert, 'Previously bookmarked page loaded.')

        blue_star_button_assert = exists(blue_star_button_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, blue_star_button_assert, 'Star button is blue.')

        click(blue_star_button_pattern)

        edit_bookmark_assert = exists(edit_bookmark_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, edit_bookmark_assert, 'Edit bookmark panel opened.')

        remove_button_assert = exists(remove_button_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, remove_button_assert, 'Remove button is present.')

        click(remove_button_pattern)

        white_star_button_assert = exists(white_star_button_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, white_star_button_assert, 'Star button turned white.')


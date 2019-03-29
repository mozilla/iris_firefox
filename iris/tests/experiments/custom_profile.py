# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'This is a test that checks for an existing bookmark in a custom profile'
        self.enabled = False

    def setup(self):
        """ Test case setup
        This overrides the setup method in the BaseTest class,
        so that it can use a profile that already has bookmarks.
        """
        BaseTest.setup(self)
        self.profile = Profile.TEN_BOOKMARKS
        return

    def run(self):
        bookmark_image_1 = LocalWeb.FIREFOX_BOOKMARK
        bookmark_image_2 = LocalWeb.POCKET_BOOKMARK_SMALL
        library_menu_pattern = NavBar.LIBRARY_MENU

        # Look for bookmarks via library menu button
        click(library_menu_pattern)
        time.sleep(Settings.UI_DELAY)
        type(Key.TAB)
        type(Key.ENTER)

        expected_1 = exists(bookmark_image_1, 5)
        assert_true(self, expected_1, 'Find Firefox bookmark 1st image')

        type(Key.ESC)

        # Look for bookmark in bookmark menu
        bookmarks_sidebar('open')
        paste('pocket')

        expected_2 = exists(bookmark_image_2, 5)
        assert_true(self, expected_2, 'Find Pocket bookmark 2nd image')

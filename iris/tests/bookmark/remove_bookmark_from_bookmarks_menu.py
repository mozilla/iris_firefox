# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):
    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Bookmarks can be removed from Bookmarks menu.'
        self.test_case_id = '4101'
        self.test_suite_id = '2525'
        self.locales = ['en-US']

    def setup(self):
        """Test case setup

        Override the setup method to use a pre-canned bookmarks profile.
        """
        BaseTest.setup(self)
        self.profile = Profile.TEN_BOOKMARKS
        return

    def run(self):

        bookmarks_menu_pattern = LibraryMenu.BOOKMARKS_OPTION
        menu_bookmark_pattern = Pattern('moz_bookmark_from_menu.png')
        delete_pattern = Pattern('delete_bookmark.png')

        right_upper_corner = Region(SCREEN_WIDTH / 2, 0, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

        navigate('about:blank')

        open_library_menu(bookmarks_menu_pattern)

        try:
            right_upper_corner.wait(menu_bookmark_pattern, 10)
            logger.debug('Moz bookmark is present in the Bookmarks Menu section.')
            right_click(menu_bookmark_pattern)
        except FindError:
            raise FindError('Moz bookmark is not present in the Bookmarks Menu, aborting.')

        bookmark_options(delete_pattern)

        try:
            delete_bookmark_menu_assert = right_upper_corner.wait_vanish(menu_bookmark_pattern, 10)
            assert_true(self, delete_bookmark_menu_assert,
                        'Moz bookmark has been successfully deleted from the Bookmarks Menu.')
        except FindError:
            raise FindError('Moz bookmark can not be deleted from the Bookmarks Menu.')

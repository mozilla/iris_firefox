# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Bookmarks can be removed from the Bookmarks Library.'
        self.test_case_id = '4100'
        self.test_suite_id = '75'
        self.locales = ['en-US']

    def setup(self):
        """Test case setup

        Override the setup method to use a pre-canned bookmarks profile.
        """
        BaseTest.setup(self)
        self.profile = Profile.TEN_BOOKMARKS
        return

    def run(self):

        library_bookmarks_pattern = Library.BOOKMARKS_TOOLBAR
        moz_library_pattern = Pattern('moz_library_bookmark.png')
        delete_pattern = Pattern('delete_bookmark.png')

        navigate('about:blank')

        open_library()

        bookmarks_menu_library_assert = exists(library_bookmarks_pattern, 10)
        assert_true(self, bookmarks_menu_library_assert, 'Bookmarks menu has been found.')

        click(library_bookmarks_pattern)

        type(Key.ENTER)
        type(Key.DOWN)

        try:
            wait(moz_library_pattern, 10)
            logger.debug('Moz bookmark can be accessed in Library section.')
            right_click(moz_library_pattern)
        except FindError:
            raise FindError('Moz bookmark is not present in Library section, aborting.')

        bookmark_options(delete_pattern)

        try:
            deleted_bookmark_assert = wait_vanish(moz_library_pattern, 10)
            assert_true(self, deleted_bookmark_assert, 'Moz bookmark has been removed from the Library.')
        except FindError:
            raise FindError('MOz bookmark can NOT be removed from the Library, aborting.')

        click_window_control('close')

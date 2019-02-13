# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Tags can be added to bookmarks using the star-shaped button.'
        self.test_case_id = '4146'
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
        library_bookmarks_pattern = Library.BOOKMARKS_TOOLBAR
        moz_library_pattern = Pattern('moz_library_bookmark.png')
        moz_tagged_bookmark = Pattern('moz_sidebar_bookmark.png')
        tags_field = Bookmarks.StarDialog.TAGS_FIELD

        navigate('about:blank')

        open_library()

        bookmarks_menu_library_assert = exists(library_bookmarks_pattern, 10)
        assert_true(self, bookmarks_menu_library_assert, 'Bookmarks menu has been found.')

        click(library_bookmarks_pattern)

        type(Key.ENTER)
        type(Key.DOWN)

        library_bookmark_assert = exists(moz_library_pattern, 10)
        assert_true(self, library_bookmark_assert, 'Moz bookmark is present in the Library section.')

        click(moz_library_pattern)

        try:
            wait(tags_field, 10)
            logger.debug('Tags field is present on the page.')
            click(tags_field)
        except FindError:
            raise FindError('Tags field is NOT present on the page, aborting.')

        paste('Iris')

        click_window_control('close')

        bookmarks_sidebar('open')

        paste('Iris')

        tagged_bookmark_assert = exists(moz_tagged_bookmark, 10)
        assert_true(self, tagged_bookmark_assert, 'Moz bookmark has been successfully tagged via library.')

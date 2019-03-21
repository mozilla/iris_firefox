# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Address bar does not autofill unvisited bookmark URLs.'
        self.test_case_id = '210301'
        self.test_suite_id = '1902'
        self.locales = ['en-US']

    def setup(self):
        """Test case setup

        This overrides the setup method in the BaseTest class, so that it can use a brand new profile.
        """
        BaseTest.setup(self)
        self.profile = Profile.BRAND_NEW
        return

    def run(self):
        library_bookmarks_mozilla_pattern = Pattern('library_bookmarks_mozilla.png')
        mozilla_autocomplete_pattern = Pattern('mozilla_autocomplete.png')

        navigate(LocalWeb.MOZILLA_TEST_SITE)

        expected = exists(LocalWeb.MOZILLA_LOGO, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, expected, 'Mozilla page loaded successfully.')

        expected = exists(LocationBar.STAR_BUTTON_UNSTARRED, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, expected, 'Bookmark star is present in the page.')

        click(LocationBar.STAR_BUTTON_UNSTARRED)

        expected = exists(Bookmarks.StarDialog.NEW_BOOKMARK, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, expected, 'The page was successfully bookmarked.')

        click(LocationBar.HISTORY_DROPMARKER)

        # From Library delete the history.
        open_library()

        expected = exists(Library.OTHER_BOOKMARKS)
        assert_true(self, expected, 'The Other Bookmarks folder exists.')

        click(Library.OTHER_BOOKMARKS)

        expected = exists(library_bookmarks_mozilla_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, expected, 'The Mozilla page is found in the library.')

        right_click(library_bookmarks_mozilla_pattern)
        type('d')

        try:
            bookmark_deleted = wait_vanish(library_bookmarks_mozilla_pattern)
            assert_true(self, bookmark_deleted, 'The bookmark is correctly deleted.')
        except FindError:
            raise FindError('The bookmark is not deleted.')

        click_window_control('close')

        select_location_bar()
        paste('moz')

        expected = exists(mozilla_autocomplete_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, expected, 'The address bar completes the URL.')

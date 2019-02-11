# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Specific tags can be removed from a bookmark'
        self.test_case_id = '4150'
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

        moz_bookmark_pattern = Pattern('moz_sidebar_bookmark.png')
        properties_pattern = Pattern('properties_option.png')
        save_pattern = Pattern('save_bookmark_name.png')
        done_button_from_star_menu = Bookmarks.StarDialog.DONE
        bookmark_tags = Pattern('bookmark_tags_selected.png')
        bookmark_button_pattern = LocationBar.STAR_BUTTON_STARRED

        right_upper_corner = Region(SCREEN_WIDTH / 2, 0, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

        navigate('about:blank')

        bookmarks_sidebar('open')

        paste('mozilla')

        try:
            wait(moz_bookmark_pattern, 10)
            logger.debug('Moz bookmark is present in the Bookmark sidebar.')
            right_click(moz_bookmark_pattern)
        except FindError:
            raise FindError('Moz bookmark is NOT present in the Bookmark sidebar, aborting.')

        option_assert = exists(properties_pattern, 10)
        assert_true(self, option_assert, 'Properties option is present on the page.')

        click(properties_pattern)

        properties_window_assert = exists(save_pattern, 10)
        assert_true(self, properties_window_assert, 'Properties window is present on the page.')

        for i in range(2):
            type(Key.TAB)

        paste('iris,tag,test')

        click(save_pattern)

        bookmarks_sidebar('close')

        time.sleep(DEFAULT_UI_DELAY)

        bookmarks_sidebar('open')

        paste('iris')

        tagged_bookmark_assert = exists(moz_bookmark_pattern, 10)
        assert_true(self, tagged_bookmark_assert, 'Moz bookmark was successfully tagged via bookmark sidebar.')

        navigate(LocalWeb.MOZILLA_TEST_SITE)

        mozilla_page_assert = exists(LocalWeb.MOZILLA_LOGO, 10)
        assert_true(self, mozilla_page_assert, 'Mozilla page loaded successfully.')

        try:
            right_upper_corner.wait(bookmark_button_pattern, 10)
            logger.debug('Bookmark star is present on the page.')
            right_upper_corner.click(bookmark_button_pattern)
        except FindError:
            raise FindError('Bookmark star is not present on the page, aborting.')

        time.sleep(Settings.UI_DELAY_LONG)

        max_attempts = 10

        while max_attempts > 0:
            type(Key.TAB)
            if exists(bookmark_tags, 1):
                edit_delete()
                max_attempts = 0
            max_attempts -= 1

        click(done_button_from_star_menu)

        bookmarks_sidebar('close')

        navigate('about:blank')

        bookmarks_sidebar('open')

        paste('iris')

        removed_tags_assert = exists(moz_bookmark_pattern, 10)
        assert_false(self, removed_tags_assert, 'Tags has been successfully removed from Moz bookmark.')

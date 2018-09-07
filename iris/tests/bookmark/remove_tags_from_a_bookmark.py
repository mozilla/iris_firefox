# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'Specific tags can be removed from a bookmark'
        self.test_case_id = '4150'
        self.test_suite_id = '75'

    def setup(self):
        """Test case setup

        This overrides the setup method in the BaseTest class, so that it can use a brand new profile.
        """
        BaseTest.setup(self)
        self.profile = Profile.TEN_BOOKMARKS
        return

    def run(self):

        moz_bookmark_pattern = Pattern('moz_sidebar_bookmark.png')
        properties_pattern = Pattern('properties_option.png')
        save_pattern = Pattern('save_bookmark_name.png')
        done_button_from_star_menu = Pattern('done_button_from_star_menu.png')
        bookmark_button_pattern = LocationBar.BOOKMARK_SELECTED_BUTTON

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

        bookmarks_sidebar('open')

        paste('iris')

        tagged_bookmark_assert = exists(moz_bookmark_pattern, 10)
        assert_true(self, tagged_bookmark_assert, 'Moz bookmark was successfully tagged via bookmark sidebar.')

        navigate(LocalWeb.MOZILLA_TEST_SITE)

        try:
            right_upper_corner.wait(bookmark_button_pattern, 10)
            logger.debug('Bookmark star is present on the page.')
            right_upper_corner.click(bookmark_button_pattern)
        except FindError:
            raise FindError('Bookmark star is not present on the page, aborting.')

        time.sleep(Settings.UI_DELAY)

        type(Key.TAB)

        edit_delete()

        click(done_button_from_star_menu)

        removed_tags_assert = wait_vanish(moz_bookmark_pattern, 10)
        assert_true(self, removed_tags_assert, 'Tags has been successfully removed from Moz bookmark.')


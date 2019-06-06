# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Specific tags can be removed from a bookmark',
        locale=['en-US'],
        test_case_id='4150',
        test_suite_id='2525',
        profile=Profiles.TEN_BOOKMARKS
    )
    def run(self, firefox):
        moz_bookmark_pattern = Pattern('moz_sidebar_bookmark.png')
        properties_pattern = Pattern('properties_option.png')
        save_pattern = Pattern('save_bookmark_name.png')
        done_button_from_star_menu = Bookmarks.StarDialog.DONE
        bookmark_tags = Pattern('bookmark_tags_selected.png')
        bookmark_button_pattern = LocationBar.STAR_BUTTON_STARRED

        right_upper_corner = Region(Screen.SCREEN_WIDTH / 2, 0, Screen.SCREEN_WIDTH / 2, Screen.SCREEN_HEIGHT / 2)

        navigate('about:blank')

        bookmarks_sidebar('open')

        paste('mozilla')

        try:
            wait(moz_bookmark_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
            logger.debug('Moz bookmark is present in the Bookmark sidebar.')
            right_click(moz_bookmark_pattern)
        except FindError:
            raise FindError('Moz bookmark is NOT present in the Bookmark sidebar, aborting.')

        option_assert = exists(properties_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert option_assert is True, 'Properties option is present on the page.'

        click(properties_pattern)

        properties_window_assert = exists(save_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert properties_window_assert is True, 'Properties window is present on the page.'

        for i in range(2):
            type(Key.TAB)

        paste('iris,tag,test')

        click(save_pattern)

        bookmarks_sidebar('close')

        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)

        bookmarks_sidebar('open')

        paste('iris')

        tagged_bookmark_assert = exists(moz_bookmark_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert tagged_bookmark_assert, 'Moz bookmark was successfully tagged via bookmark sidebar.'

        navigate(LocalWeb.MOZILLA_TEST_SITE)

        mozilla_page_assert = exists(LocalWeb.MOZILLA_LOGO, FirefoxSettings.FIREFOX_TIMEOUT)
        assert mozilla_page_assert is True, 'Mozilla page loaded successfully.'

        try:
            right_upper_corner.wait(bookmark_button_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
            logger.debug('Bookmark star is present on the page.')
            right_upper_corner.click(bookmark_button_pattern)
        except FindError:
            raise FindError('Bookmark star is not present on the page, aborting.')

        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)

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

        removed_tags_assert = exists(moz_bookmark_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert removed_tags_assert is False, 'Tags has been successfully removed from Moz bookmark.'

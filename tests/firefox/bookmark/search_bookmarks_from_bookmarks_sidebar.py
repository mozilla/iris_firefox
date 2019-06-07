# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Searching for bookmarks from the Bookmarks Sidebar works properly.',
        locale=['en-US'],
        test_case_id='168922',
        test_suite_id='2525',
        profile=Profiles.TEN_BOOKMARKS
    )
    def run(self, firefox):
        moz_bookmark_pattern = Pattern('moz_sidebar_bookmark.png')
        properties_pattern = Pattern('properties_option.png')
        save_pattern = Pattern('save_bookmark_name.png')

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

        paste('iris')

        click(save_pattern)

        bookmarks_sidebar('close')

        bookmarks_sidebar('open')

        paste('iris')

        tagged_bookmark_assert = exists(moz_bookmark_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert tagged_bookmark_assert is True, 'Moz bookmark was successfully tagged via bookmark sidebar.'

        click(moz_bookmark_pattern)

        mozilla_page_assert = exists(LocalWeb.MOZILLA_LOGO, FirefoxSettings.FIREFOX_TIMEOUT)
        assert mozilla_page_assert is True, 'Mozilla page loaded successfully.'

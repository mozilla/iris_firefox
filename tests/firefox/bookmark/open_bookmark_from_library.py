# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Bookmarks can be opened from the Bookmarks Library',
        locale=['en-US'],
        test_case_id='169256',
        test_suite_id='2525',
        profile=Profiles.TEN_BOOKMARKS
    )
    def run(self, firefox):
        library_bookmarks_pattern = Library.BOOKMARKS_TOOLBAR
        moz_library_pattern = Pattern('moz_library_bookmark.png')

        navigate('about:blank')

        open_library()

        bookmarks_menu_library_assert = exists(library_bookmarks_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert bookmarks_menu_library_assert is True, 'Bookmarks menu has been found.'

        click(library_bookmarks_pattern)

        type(Key.ENTER)
        type(Key.DOWN)

        library_bookmark_assert = exists(moz_library_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert library_bookmark_assert is True, 'Moz bookmark can be accessed from Library section.'

        click(moz_library_pattern)
        type(Key.ENTER)

        if OSHelper.is_windows():
            change_window_view()
            click_window_control('close')

        mozilla_page_assert = exists(LocalWeb.MOZILLA_LOGO, FirefoxSettings.FIREFOX_TIMEOUT)
        assert mozilla_page_assert  is True, 'Mozilla page loaded successfully.'

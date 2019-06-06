# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Bookmarks can be opened from Bookmarks menu.',
        locale=['en-US'],
        test_case_id='163194',
        test_suite_id='2525',
        profile=Profiles.TEN_BOOKMARKS
    )
    def run(self, firefox):
        bookmarks_menu_pattern = LibraryMenu.BOOKMARKS_OPTION
        menu_bookmark_pattern = Pattern('moz_bookmark_from_menu.png')

        right_upper_corner = Region(Screen.SCREEN_WIDTH / 2, 0, Screen.SCREEN_WIDTH / 2, Screen.SCREEN_HEIGHT / 2)

        navigate('about:blank')

        open_library_menu(bookmarks_menu_pattern)

        moz_bookmark_menu_right_corner_assert = right_upper_corner.exists(menu_bookmark_pattern,
                                                                          FirefoxSettings.FIREFOX_TIMEOUT)
        assert moz_bookmark_menu_right_corner_assert is True, 'Moz bookmark can be accessed from the Bookmarks Menu.'

        right_upper_corner.click(menu_bookmark_pattern)

        mozilla_page_assert = exists(LocalWeb.MOZILLA_LOGO, FirefoxSettings.FIREFOX_TIMEOUT)
        assert mozilla_page_assert is True, 'Mozilla page has been successfully accessed from the Bookmarks Menu.'

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Open a bookmark from the Recently Bookmarked section using Open option',
        locale=['en-US'],
        test_case_id='165485',
        test_suite_id='2525',
        profile=Profiles.TEN_BOOKMARKS
    )
    def run(self, firefox):
        open_option_pattern = Pattern('open_option.png')

        library_button_exists = exists(NavBar.LIBRARY_MENU)
        assert library_button_exists is True, 'View history, saved bookmarks and more section exists'

        click(NavBar.LIBRARY_MENU)

        bookmarks_menu_option_exists = exists(LibraryMenu.BOOKMARKS_OPTION)
        assert bookmarks_menu_option_exists is True, 'The Bookmarks menu is correctly displayed'

        click(LibraryMenu.BOOKMARKS_OPTION)

        recently_firefox_bookmark_exists = exists(LocalWeb.FIREFOX_BOOKMARK)
        assert recently_firefox_bookmark_exists is True, 'Firefox bookmark exists in recently bookmarked section'

        right_click(LocalWeb.FIREFOX_BOOKMARK)

        open_option_exists = exists(open_option_pattern)
        assert open_option_exists is True, 'Open option exists'

        click(open_option_pattern)

        firefox_full_logo_exists = exists(LocalWeb.FIREFOX_IMAGE, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert firefox_full_logo_exists is True, 'Bookmark is correctly opened in the current tab.'

        bookmark_opened_in_current_tab = exists(LocalWeb.IRIS_LOGO_INACTIVE_TAB)
        assert bookmark_opened_in_current_tab is False, 'The page that was previously displayed in the current ' \
                                                        'tab is no longer displayed'

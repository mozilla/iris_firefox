# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Cut a bookmark from the Recently Bookmarked section',
        locale=['en-US'],
        test_case_id='165489',
        test_suite_id='2525',
        profile=Profiles.TEN_BOOKMARKS,
        blocked_by={'id': '1533339', 'platform': OSPlatform.ALL}
    )
    def run(self, firefox):
        cut_option_pattern = Pattern('cut_option.png')
        paste_option_pattern = Pattern('paste_option.png')
        firefox_bookmark_cut_pattern = Pattern('firefox_bookmark_cut.png')

        library_button_exists = exists(NavBar.LIBRARY_MENU)
        assert library_button_exists is True, 'View history, saved bookmarks and more section exists'

        click(NavBar.LIBRARY_MENU)

        bookmarks_menu_option_exists = exists(LibraryMenu.BOOKMARKS_OPTION)
        assert bookmarks_menu_option_exists is True, 'The Bookmarks menu is correctly displayed'

        click(LibraryMenu.BOOKMARKS_OPTION)

        recently_firefox_bookmark_exists = exists(LocalWeb.FIREFOX_BOOKMARK)
        assert recently_firefox_bookmark_exists is True, 'Firefox bookmark exists in recently bookmarked section'

        right_click(LocalWeb.FIREFOX_BOOKMARK)

        cut_option_exists = exists(cut_option_pattern)
        assert cut_option_exists is True, '\'Cut\' option exists'

        click(cut_option_pattern)

        firefox_bookmark_cut_exists = exists(firefox_bookmark_cut_pattern)
        assert firefox_bookmark_cut_exists is True, 'The selected bookmark is grayed out'

        open_library()

        library_exists = exists(Library.TITLE)
        assert library_exists is True, 'Library bookmark menu is opened'

        bookmarks_toolbar_exists = exists(Library.BOOKMARKS_TOOLBAR)
        assert bookmarks_toolbar_exists is True, 'Bookmarks toolbar section exists'

        right_click(Library.BOOKMARKS_TOOLBAR)

        paste_option_exists = exists(paste_option_pattern)
        assert paste_option_exists is True, 'Paste option exists'

        click(paste_option_pattern)

        firefox_bookmark_cut_exists = exists(LocalWeb.FIREFOX_BOOKMARK)
        assert firefox_bookmark_cut_exists is True, 'The bookmark is correctly added in the selected section and ' \
                                                    'deleted from the previous one.'

        close_window_control('auxiliary')

        click(NavBar.LIBRARY_MENU)

        bookmarks_menu_option_exists = exists(LibraryMenu.BOOKMARKS_OPTION)
        assert bookmarks_menu_option_exists is True, 'The Bookmarks menu is correctly displayed'

        click(LibraryMenu.BOOKMARKS_OPTION)

        recently_firefox_bookmark_not_exists = exists(LocalWeb.FIREFOX_BOOKMARK)
        assert recently_firefox_bookmark_not_exists is True, 'Firefox bookmark cut from recently bookmarked section'


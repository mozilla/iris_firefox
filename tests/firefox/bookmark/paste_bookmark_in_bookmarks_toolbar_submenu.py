# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Paste a bookmark in the Bookmarks Toolbar submenu',
        locale=['en-US'],
        test_case_id='163489',
        test_suite_id='2525',
        profile=Profiles.TEN_BOOKMARKS,
        exclude=OSPlatform.MAC
    )
    def run(self, firefox):
        firefox_menu_bookmarks_pattern = Pattern('firefox_menu_bookmarks.png')
        firefox_menu_bookmarks_toolbar_pattern = Pattern('firefox_menu_bookmarks_toolbar.png')
        getting_started_pattern = Pattern('getting_started_top_menu.png')
        copy_option_pattern = Pattern('copy_option.png')
        paste_option_pattern = Pattern('paste_option.png')
        firefox_menu_most_visited_pattern = Pattern('firefox_menu_most_visited.png')
        mozilla_firefox_bookmarks_folder_pattern = Pattern('mozilla_firefox_bookmarks_folder.png')
        mozilla_about_us_bookmark_pattern = Pattern('mozilla_about_us_bookmark.png')
        mozilla_about_us_bookmark_toolbar_pattern = Pattern('mozilla_about_us_bookmark_toolbar.png')

        open_firefox_menu()

        firefox_menu_bookmarks_exists = exists(firefox_menu_bookmarks_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert firefox_menu_bookmarks_exists is True, 'Firefox menu > Bookmarks exists'

        click(firefox_menu_bookmarks_pattern)

        mozilla_firefox_bookmarks_folder_exists = exists(mozilla_firefox_bookmarks_folder_pattern,
                                                         FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert mozilla_firefox_bookmarks_folder_exists is True, 'Firefox menu > Bookmarks > Mozilla Firefox ' \
                                                                'bookmarks folder exists'
        click(mozilla_firefox_bookmarks_folder_pattern)

        mozilla_about_us_bookmark_exists = exists(mozilla_about_us_bookmark_pattern,
                                                  FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert mozilla_about_us_bookmark_exists is True, 'Mozilla About Us bookmark is displayed'

        right_click(mozilla_about_us_bookmark_pattern)

        copy_option_exists = exists(copy_option_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert copy_option_exists is True, 'The Copy option exists'

        click(copy_option_pattern)

        bookmarks_toolbar_folder_exists = exists(firefox_menu_bookmarks_toolbar_pattern,
                                                 FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert bookmarks_toolbar_folder_exists is True, 'Firefox menu > Bookmarks > Bookmarks Toolbar folder exists'

        click(firefox_menu_bookmarks_toolbar_pattern)

        most_visited_folder_exists = exists(firefox_menu_most_visited_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert most_visited_folder_exists is True, 'Firefox menu > Bookmarks > Bookmarks Toolbar > Most Visited ' \
                                                   'folder exists'

        getting_started_exists = exists(getting_started_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert getting_started_exists is True, 'Firefox menu > Bookmarks > Bookmarks Toolbar > Getting Started ' \
                                               'bookmark exists'

        right_click(getting_started_pattern)

        paste_option_exists = exists(paste_option_pattern)
        assert paste_option_exists is True, 'Paste option exists'

        click(paste_option_pattern)

        hover(firefox_menu_bookmarks_toolbar_pattern)

        mozilla_about_us_bookmark_exists = exists(mozilla_about_us_bookmark_pattern,
                                                  FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert mozilla_about_us_bookmark_exists is True, 'Mozilla About Us bookmark is displayed in Firefox menu > ' \
                                                         'Bookmarks > Bookmarks Toolbar'

        restore_firefox_focus()

        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT/3)

        open_bookmarks_toolbar()

        bookmark_exists_in_toolbar = exists(mozilla_about_us_bookmark_toolbar_pattern,
                                            FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert bookmark_exists_in_toolbar is True, 'The copied file/folder is correctly pasted in the ' \
                                                   '**Bookmarks Toolbar** section.'

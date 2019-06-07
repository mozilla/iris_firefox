# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Add a new bookmark in \'Mozilla Firefox\' section',
        locale=['en-US'],
        test_case_id='163373',
        test_suite_id='2525',
        exclude=OSPlatform.MAC
    )
    def run(self, firefox):
        firefox_menu_bookmarks_pattern = Pattern('firefox_menu_bookmarks.png')
        mozilla_firefox_bookmarks_folder_pattern = Pattern('mozilla_firefox_bookmarks_folder.png')
        mozilla_about_us_bookmark_pattern = Pattern('mozilla_about_us_bookmark.png')
        new_bookmark_window_pattern = Pattern('new_bookmark_window.png')
        new_soap_bookmark_pattern = Pattern('new_soap_bookmark.png')
        open_all_in_tabs_pattern = Pattern('open_all_in_tabs.png')
        customize_firefox_bookmark_pattern = Pattern('mozilla_customize_firefox_bookmark.png')
        get_involved_bookmark_pattern = Pattern('mozilla_get_involved_bookmark.png')
        help_and_tutorials_bookmark_pattern = Pattern('mozilla_help_and_tutorials_bookmark.png')

        open_firefox_menu()

        firefox_menu_bookmarks_exists = exists(firefox_menu_bookmarks_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert firefox_menu_bookmarks_exists is True, 'Firefox menu > Bookmarks exists'

        click(firefox_menu_bookmarks_pattern)

        mozilla_firefox_bookmarks_folder_exists = exists(mozilla_firefox_bookmarks_folder_pattern,
                                                         FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert mozilla_firefox_bookmarks_folder_exists is True, 'Firefox menu > Bookmarks > Mozilla Firefox ' \
                                                                'bookmarks folder exists'
        click(mozilla_firefox_bookmarks_folder_pattern)

        mozilla_customize_firefox_bookmark_exists = exists(customize_firefox_bookmark_pattern,
                                                           FirefoxSettings.FIREFOX_TIMEOUT)
        assert mozilla_customize_firefox_bookmark_exists is True, 'Customize Firefox bookmark is displayed'

        mozilla_get_involved_bookmark_exists = exists(get_involved_bookmark_pattern)
        assert mozilla_get_involved_bookmark_exists, 'Get Involved bookmark is displayed'

        mozilla_help_and_tutorials_bookmark_exists = exists(help_and_tutorials_bookmark_pattern)
        assert mozilla_help_and_tutorials_bookmark_exists is True, 'Help and Tutorials bookmark is displayed'

        mozilla_about_us_bookmark_exists = exists(mozilla_about_us_bookmark_pattern)
        assert mozilla_about_us_bookmark_exists is True, 'About Us bookmark is displayed'

        open_all_in_tabs_exists = exists(open_all_in_tabs_pattern)
        assert open_all_in_tabs_exists is True, 'Open all in tabs option exists'

        right_click(mozilla_about_us_bookmark_pattern)

        context_menu_new_bookmark_pattern_displayed = exists(Library.Organize.NEW_BOOKMARK,
                                                             FirefoxSettings.FIREFOX_TIMEOUT)
        assert context_menu_new_bookmark_pattern_displayed is True, 'Context menu New Bookmark option is displayed'

        click(Library.Organize.NEW_BOOKMARK)

        new_bookmark_window_opened = exists(new_bookmark_window_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert new_bookmark_window_opened is True, 'New Bookmark window is displayed'

        paste('SOAP')
        type(Key.TAB)

        paste(LocalWeb.SOAP_WIKI_TEST_SITE)
        type(Key.TAB)

        paste('SOAP')
        type(Key.TAB)
        type(Key.TAB)

        paste('SOAP')
        type(Key.ENTER)

        open_firefox_menu()

        firefox_menu_bookmarks__second_exists = exists(firefox_menu_bookmarks_pattern,
                                                       FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert firefox_menu_bookmarks__second_exists is True, 'Firefox menu > Bookmarks exists'

        click(firefox_menu_bookmarks_pattern)

        mozilla_firefox_bookmarks_folder_second_exists = exists(mozilla_firefox_bookmarks_folder_pattern,
                                                                FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert mozilla_firefox_bookmarks_folder_second_exists is True, 'Firefox menu > Bookmarks > Mozilla Firefox ' \
                                                                       'bookmarks folder exists'
        click(mozilla_firefox_bookmarks_folder_pattern)

        bookmark_exists = exists(new_soap_bookmark_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert bookmark_exists is True, 'A new bookmark is added in Mozilla Firefox section.'

        restore_firefox_focus()

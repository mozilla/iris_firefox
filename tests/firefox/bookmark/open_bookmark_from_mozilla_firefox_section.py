# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Open a bookmark from \'Mozilla Firefox\' section',
        locale=['en-US'],
        test_case_id='163230',
        test_suite_id='2525'
    )
    def run(self, firefox):
        firefox_menu_bookmarks_pattern = Pattern('firefox_menu_bookmarks.png')
        mozilla_firefox_predefined_bookmarks_pattern = Pattern('mozilla_firefox_predefined_bookmarks.png')
        mozilla_firefox_bookmarks_folder_pattern = Pattern('mozilla_firefox_bookmarks_folder.png')
        mozilla_about_us_bookmark_pattern = Pattern('mozilla_about_us_bookmark.png')
        mozilla_about_us_page_pattern = Pattern('mozilla_about_us_page.png')

        open_firefox_menu()

        firefox_menu_bookmarks_exists = exists(firefox_menu_bookmarks_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert firefox_menu_bookmarks_exists is True, 'Firefox menu > Bookmarks exists'

        click(firefox_menu_bookmarks_pattern)

        mozilla_firefox_bookmarks_folder_exists = exists(mozilla_firefox_bookmarks_folder_pattern,
                                                         FirefoxSettings.FIREFOX_TIMEOUT)
        assert mozilla_firefox_bookmarks_folder_exists is True, 'Firefox menu > Bookmarks > Mozilla Firefox ' \
                                                                'bookmarks folder exists'
        click(mozilla_firefox_bookmarks_folder_pattern)

        mozilla_firefox_predefined_bookmarks_exists = exists(mozilla_firefox_predefined_bookmarks_pattern,
                                                             FirefoxSettings.FIREFOX_TIMEOUT)
        assert mozilla_firefox_predefined_bookmarks_exists is True, 'Predefined Mozilla Firefox related bookmarks ' \
                                                                    'displayed'

        click(mozilla_about_us_bookmark_pattern)

        mozilla_about_us_page_displayed = exists(mozilla_about_us_page_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert mozilla_about_us_page_displayed is True, 'Mozilla about us page is displayed'

        restore_firefox_focus()

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Open a bookmark in a New Private Window from \'Mozilla Firefox\' section',
        locale=['en-US'],
        test_case_id='163233',
        test_suite_id='2525',
        profile=Profiles.TEN_BOOKMARKS,
        exclude=OSPlatform.MAC
    )
    def run(self, firefox):
        firefox_menu_bookmarks_pattern = Pattern('firefox_menu_bookmarks.png')
        mozilla_firefox_predefined_bookmarks_pattern = Pattern('mozilla_firefox_predefined_bookmarks.png')
        mozilla_firefox_bookmarks_folder_pattern = Pattern('mozilla_firefox_bookmarks_folder.png')
        mozilla_about_us_bookmark_pattern = Pattern('mozilla_about_us_bookmark.png')
        mozilla_about_us_page_pattern = Pattern('mozilla_about_us_page.png')
        context_menu_open_in_a_new_private_window_pattern = Pattern('context_menu_open_in_a_new_private_window.png')

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
        assert mozilla_firefox_predefined_bookmarks_exists is True, 'Predefined Mozilla Firefox related ' \
                                                                    'bookmarks displayed'

        right_click(mozilla_about_us_bookmark_pattern)

        open_in_a_new_private_window_option_displayed = exists(context_menu_open_in_a_new_private_window_pattern,
                                                               FirefoxSettings.FIREFOX_TIMEOUT)
        assert open_in_a_new_private_window_option_displayed is True, 'Context menu Open in a New ' \
                                                                      'Private Window option is displayed'

        click(context_menu_open_in_a_new_private_window_pattern)

        mozilla_about_us_page_displayed = exists(mozilla_about_us_page_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert mozilla_about_us_page_displayed is True, 'The website related to the selected bookmark is loaded'

        private_window_image_displayed = exists(PrivateWindow.private_window_pattern)
        assert private_window_image_displayed is True, 'The website related to the selected bookmark' \
                                                       ' is opened in a new private window.'

        close_window()

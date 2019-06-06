# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Edit a Bookmark from Bookmarks menu',
        locale=['en-US'],
        test_case_id='163195',
        test_suite_id='2525',
        profile=Profiles.TEN_BOOKMARKS
    )
    def run(self, firefox):
        firefox_menu_bookmarks_pattern = Pattern('firefox_menu_bookmarks.png')
        edit_this_bookmark_option_pattern = Pattern('edit_this_bookmark_option.png')

        navigate(LocalWeb.MOZILLA_TEST_SITE)

        test_site_opened = exists(LocalWeb.MOZILLA_LOGO, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert test_site_opened is True, 'Previously bookmarked Mozilla website is opened'

        open_firefox_menu()

        firefox_menu_bookmarks_exists = exists(firefox_menu_bookmarks_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert firefox_menu_bookmarks_exists is True, 'Firefox menu > Bookmarks exists'

        click(firefox_menu_bookmarks_pattern)

        edit_this_bookmark_option_exists = exists(edit_this_bookmark_option_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert edit_this_bookmark_option_exists, 'Edit This Bookmark option exists'

        click(edit_this_bookmark_option_pattern)

        edit_stardialog_displayed = exists(Bookmarks.StarDialog.EDIT_THIS_BOOKMARK, FirefoxSettings.FIREFOX_TIMEOUT)
        assert edit_stardialog_displayed is True, 'The Edit This Bookmark popup is displayed under the star-shaped ' \
                                                  'icon.'


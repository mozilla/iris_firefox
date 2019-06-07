# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Open a bookmark in a New Tab from Bookmarks Sidebar',
        locale=['en-US'],
        test_case_id='168927',
        test_suite_id='2525',
        profile=Profiles.TEN_BOOKMARKS
    )
    def run(self, firefox):
        open_in_new_tab_option_pattern = Pattern('open_in_new_tab.png')
        firefox_sidebar_logo_pattern = Pattern('firefox_bookmark.png')
        iris_tab_pattern = Pattern('iris_tab.png')

        if OSHelper.is_mac():
            other_bookmarks_pattern = Pattern('other_bookmarks.png')
        else:
            other_bookmarks_pattern = Library.OTHER_BOOKMARKS

        bookmarks_sidebar('open')

        bookmarks_sidebar_menu_exists = exists(SidebarBookmarks.BOOKMARKS_HEADER, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert bookmarks_sidebar_menu_exists is True, '\'Bookmarks Sidebar\' is correctly displayed.'

        other_bookmarks_exists = exists(other_bookmarks_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert other_bookmarks_exists is True, '\'Other bookmarks\' folder exists on the sidebar.'

        click(other_bookmarks_pattern)

        firefox_sidebar_logo_exists = exists(firefox_sidebar_logo_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert firefox_sidebar_logo_exists is True, '\'Firefox\' bookmark exists in the \'Other bookmarks\' folder'

        right_click(firefox_sidebar_logo_pattern)

        open_option_exists = exists(open_in_new_tab_option_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert open_option_exists is True, '\'Open in new tab\' option is displayed after right-click ' \
                                           'at the Firefox bookmark icon'

        click(open_in_new_tab_option_pattern)

        select_tab("2")

        firefox_full_logo_exists = exists(LocalWeb.FIREFOX_IMAGE, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert firefox_full_logo_exists is True, 'The web page is opened in the new tab'

        select_tab("1")

        iris_tab_available = exists(iris_tab_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert iris_tab_available is True, 'Initial tab exists after opening bookmarked page in new tab'

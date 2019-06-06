# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Open a bookmark in a New Tab from Library',
        locale=['en-US'],
        test_case_id='169258',
        test_suite_id='2525'
    )
    def run(self, firefox):
        soap_wiki_tab_pattern = Pattern('soap_wiki_tab.png')
        wiki_bookmark_logo_pattern = Pattern('wiki_bookmark_logo.png')
        open_in_new_tab_pattern = Pattern('open_in_new_tab.png')

        home_width, home_height = NavBar.HOME_BUTTON.get_size()
        tabs_region = Rectangle(0, 0, Screen.SCREEN_WIDTH, home_height * 4)

        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)

        soap_wiki_opened = exists(soap_wiki_tab_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT, tabs_region)
        assert soap_wiki_opened is True, 'The test page is opened'

        bookmark_page()

        stardialog_displayed = exists(Bookmarks.StarDialog.DONE, FirefoxSettings.FIREFOX_TIMEOUT)
        assert stardialog_displayed is True, 'StarDialog opened'

        click(Bookmarks.StarDialog.DONE)

        new_tab()
        previous_tab()
        close_tab()

        open_library()

        library_opened = exists(Library.TITLE, FirefoxSettings.FIREFOX_TIMEOUT)
        assert library_opened is True, 'Library opened'

        click(Library.OTHER_BOOKMARKS)

        bookmark_exists = exists(wiki_bookmark_logo_pattern)
        assert bookmark_exists is True, 'Previously added bookmark exists in Library'

        right_click(soap_wiki_tab_pattern)

        open_in_new_tab_option_exists = exists(open_in_new_tab_pattern, FirefoxSettings.FIREFOX_TIMEOUT/2)
        assert open_in_new_tab_option_exists is True, 'Open in New Tab option exists'

        click(open_in_new_tab_pattern)

        soap_wiki_opened_from_bookmarks = exists(soap_wiki_tab_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT, tabs_region)
        assert soap_wiki_opened_from_bookmarks is True, 'The test page is downloaded'

        new_tab_exists = exists(Tabs.NEW_TAB_NOT_HIGHLIGHTED)
        assert new_tab_exists is True, 'The selected bookmark page is opened in a new tab.'

        open_library()

        click(Library.TITLE)
        close_window_control('auxiliary')

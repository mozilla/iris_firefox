# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Open a bookmark with drag&drop from Library',
        locale=['en-US'],
        test_case_id='169271',
        test_suite_id='2525'
    )
    def run(self, firefox):
        soap_wiki_tab_pattern = Pattern('soap_wiki_tab.png')
        wiki_bookmark_logo_pattern = Pattern('wiki_bookmark_logo.png')

        home_width, home_height = NavBar.HOME_BUTTON.get_size()
        tabs_region = Region(0, 0, Screen.SCREEN_WIDTH, home_height * 4)

        centre_location = Location(Screen.SCREEN_WIDTH/2, Screen.SCREEN_HEIGHT/4)

        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)

        soap_wiki_opened = exists(soap_wiki_tab_pattern, FirefoxSettings.FIREFOX_TIMEOUT*3, tabs_region)
        assert soap_wiki_opened is True, 'The test page is opened'

        bookmark_page()

        stardialog_displayed = exists(Bookmarks.StarDialog.DONE, FirefoxSettings.FIREFOX_TIMEOUT)
        assert stardialog_displayed is True, 'StarDialog displayed'

        click(Bookmarks.StarDialog.DONE)

        new_tab()

        previous_tab()

        close_tab()

        open_library()

        drag_drop(Library.TITLE, centre_location, duration=FirefoxSettings.FIREFOX_TIMEOUT*0.3)

        library_opened = exists(Library.TITLE, FirefoxSettings.FIREFOX_TIMEOUT)
        assert library_opened is True, 'Library opened'

        click(Library.OTHER_BOOKMARKS)

        bookmark_exists = exists(wiki_bookmark_logo_pattern)
        assert bookmark_exists is True, 'Previously added bookmark exists in Library'

        drag_drop(soap_wiki_tab_pattern, LocationBar.SEARCH_BAR, duration=FirefoxSettings.FIREFOX_TIMEOUT*0.3)

        soap_wiki_opened_from_bookmarks = exists(soap_wiki_tab_pattern, FirefoxSettings.FIREFOX_TIMEOUT*3, tabs_region)
        assert soap_wiki_opened_from_bookmarks is True, 'The test page is opened with drag and drop from Library'

        open_library()

        click(Library.TITLE)

        close_window_control('auxiliary')

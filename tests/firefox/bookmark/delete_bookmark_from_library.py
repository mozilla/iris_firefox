# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Delete a bookmark from Library',
        locale=['en-US'],
        test_case_id='169267',
        test_suite_id='2525'
    )
    def run(self, firefox):
        soap_wiki_tab_pattern = Pattern('soap_wiki_tab.png')
        delete_bookmark_pattern = Pattern('delete_bookmark.png')

        stardialog_region = Region(Screen.SCREEN_WIDTH / 2, 0, Screen.SCREEN_WIDTH / 2, Screen.SCREEN_HEIGHT)

        home_width, home_height = NavBar.HOME_BUTTON.get_size()
        tabs_region = Region(0, 0, Screen.SCREEN_WIDTH, home_height * 4)

        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)

        soap_wiki_opened = exists(soap_wiki_tab_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT, tabs_region)
        assert soap_wiki_opened is True, 'Soap wiki page opened'

        bookmark_page()

        stardialog_displayed = exists(Bookmarks.StarDialog.DONE, FirefoxSettings.FIREFOX_TIMEOUT, stardialog_region)
        assert stardialog_displayed is True, 'Bookmark page dialog displayed'

        click(Bookmarks.StarDialog.DONE, 0, stardialog_region)

        new_tab()
        select_tab("1")
        close_tab()

        open_library()

        library_opened = exists(Library.TITLE, FirefoxSettings.FIREFOX_TIMEOUT)
        assert library_opened is True, 'Library opened'

        other_bookmarks_exists = exists(Library.OTHER_BOOKMARKS)
        assert other_bookmarks_exists is True, 'The Other Bookmarks folder exists'

        click(Library.OTHER_BOOKMARKS)

        wiki_bookmark_added = exists(soap_wiki_tab_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert wiki_bookmark_added is True, 'The Wikipedia bookmark is successfully added'

        right_click(soap_wiki_tab_pattern)

        delete_option_exists = exists(delete_bookmark_pattern)
        assert delete_option_exists is True, 'Delete option exists'

        click(delete_bookmark_pattern)

        try:
            bookmark_deleted = wait_vanish(soap_wiki_tab_pattern)
            assert bookmark_deleted is True, 'The bookmark is correctly deleted.'
        except FindError:
            raise FindError('The bookmark is not deleted.')

        click(Library.TITLE)

        close_window_control('auxiliary')

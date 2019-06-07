# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Move a bookmark to another section with drag&drop in Library',
        locale=['en-US'],
        test_case_id='169270',
        test_suite_id='2525'
    )
    def run(self, firefox):
        soap_wiki_tab_pattern = Pattern('soap_wiki_tab.png')
        bookmarks_highlighted_pattern = Pattern('bookmarks_highlighted.png')
        bookmarks_moved_pattern = Pattern('bookmarks_moved.png')

        home_width, home_height = NavBar.HOME_BUTTON.get_size()
        tabs_region = Rectangle(0, 0, Screen.SCREEN_WIDTH, home_height * 4)

        navigate(LocalWeb.FIREFOX_TEST_SITE)

        firefox_test_site_opened = exists(LocalWeb.FIREFOX_LOGO, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert firefox_test_site_opened is True, 'Firefox Test page opened'

        bookmark_page()

        stardialog_displayed = exists(Bookmarks.StarDialog.DONE, FirefoxSettings.FIREFOX_TIMEOUT)
        assert stardialog_displayed is True, 'Bookmark page dialog displayed'

        click(Bookmarks.StarDialog.DONE)

        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)

        soap_wiki_opened = exists(soap_wiki_tab_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT, tabs_region)
        assert soap_wiki_opened is True, 'The test page is opened'

        bookmark_page()

        stardialog_displayed = exists(Bookmarks.StarDialog.DONE, FirefoxSettings.FIREFOX_TIMEOUT)
        assert stardialog_displayed is True, 'Bookmark page dialog displayed'

        click(Bookmarks.StarDialog.DONE)

        new_tab()
        select_tab("1")
        close_tab()

        open_library()

        library_opened = exists(Library.TITLE, FirefoxSettings.FIREFOX_TIMEOUT)
        assert library_opened, 'Library opened'

        other_bookmarks_folder_exists = exists(Library.OTHER_BOOKMARKS)
        assert other_bookmarks_folder_exists is True, 'Other Bookmarks folder exists'

        click(Library.OTHER_BOOKMARKS)

        bookmark_exists = exists(soap_wiki_tab_pattern)
        assert bookmark_exists is True, 'The Wikipedia bookmark is successfully added'

        click(soap_wiki_tab_pattern)

        if OSHelper.is_mac():
            type('a', KeyModifier.CMD)
        else:
            type('a', KeyModifier.CTRL)

        bookmarks_highlighted = exists(bookmarks_highlighted_pattern)
        assert bookmarks_highlighted is True, 'Bookmarks are highlighted'

        bookmarks_toolbar_folder_exists = exists(Library.BOOKMARKS_TOOLBAR)
        assert bookmarks_toolbar_folder_exists is True, 'Bookmarks toolbar folder exists'

        drag_drop(bookmarks_highlighted_pattern, Library.BOOKMARKS_TOOLBAR)

        click(Library.OTHER_BOOKMARKS)

        click(Library.BOOKMARKS_TOOLBAR)

        bookmarks_moved = exists(bookmarks_moved_pattern)
        assert bookmarks_moved is True, 'Bookmarks are correctly moved in the selected section.'

        click(Library.TITLE)

        close_window_control('auxiliary')

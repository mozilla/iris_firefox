# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Paste a bookmark in Library',
        locale=['en-US'],
        test_case_id='169266',
        test_suite_id='2525'
    )
    def run(self, firefox):
        soap_wiki_tab_pattern = Pattern('soap_wiki_tab.png')
        copy_option_pattern = Pattern('copy_option.png')
        paste_option_pattern = Pattern('paste_option.png')
        other_bookmarks_option_pattern = Bookmarks.StarDialog.PANEL_FOLDER_DEFAULT_OPTION.similar(.6)
        bookmarks_toolbar_option = Bookmarks.StarDialog.PANEL_OPTION_BOOKMARK_TOOLBAR.similar(.6)

        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)

        soap_wiki_opened = exists(soap_wiki_tab_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert soap_wiki_opened is True, 'The test page is opened'

        bookmark_page()

        done_button_exists = exists(Bookmarks.StarDialog.DONE)
        assert done_button_exists is True, 'StarDialog is opened'

        click(Bookmarks.StarDialog.DONE, 0)

        bookmark_page()

        other_bookmarks_option_exists = exists(other_bookmarks_option_pattern)
        assert other_bookmarks_option_exists is True, 'Other Bookmarks option exists'

        click(other_bookmarks_option_pattern, 0)

        wiki_bookmark_toolbar_folder_displayed = exists(bookmarks_toolbar_option)
        assert wiki_bookmark_toolbar_folder_displayed is True, 'Bookmark toolbar folder displayed'

        click(bookmarks_toolbar_option)

        click(Bookmarks.StarDialog.DONE)

        new_tab()
        select_tab("1")
        close_tab()

        wiki_bookmark_added = exists(soap_wiki_tab_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert wiki_bookmark_added is True, 'The Wikipedia bookmark is successfully added'

        right_click(soap_wiki_tab_pattern)

        copy_option_exists = exists(copy_option_pattern)
        assert copy_option_exists is True, 'Copy option exists'

        click(copy_option_pattern)

        open_library()

        library_opened = exists(Library.OTHER_BOOKMARKS, FirefoxSettings.FIREFOX_TIMEOUT)
        assert library_opened is True, 'Library opened'

        maximize_window_control('auxiliary')

        other_bookmarks_width, other_bookmarks_height = Library.OTHER_BOOKMARKS.get_size()
        location_to_paste = find(Library.OTHER_BOOKMARKS).right(other_bookmarks_width * 2)

        right_click(location_to_paste)

        paste_option_exists = exists(paste_option_pattern)
        assert paste_option_exists is True, 'Paste option exists'

        click(paste_option_pattern)

        click(Library.OTHER_BOOKMARKS)

        bookmark_pasted = exists(soap_wiki_tab_pattern)
        assert bookmark_pasted is True, 'Bookmark is correctly copied in the selected session'

        close_window_control('auxiliary')

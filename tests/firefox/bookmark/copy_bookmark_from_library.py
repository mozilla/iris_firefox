# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Copy a bookmark from Library',
        locale=['en-US'],
        test_case_id='169265',
        test_suite_id='2525',
    )
    def run(self, firefox):
        soap_wiki_tab_pattern = Pattern('soap_wiki_tab.png')
        copy_option_pattern = Pattern('copy_option.png')
        paste_option_pattern = Pattern('paste_option.png')
        bookmark_pasted_pattern = Pattern('bookmark_pasted.png')

        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)

        soap_wiki_opened = exists(soap_wiki_tab_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert soap_wiki_opened is True, 'The test page is opened'

        bookmark_page()

        stardialog_displayed = exists(Bookmarks.StarDialog.DONE, FirefoxSettings.FIREFOX_TIMEOUT)
        assert stardialog_displayed is True, 'Stardialog displayed'

        click(Bookmarks.StarDialog.DONE)

        new_tab()
        previous_tab()
        close_tab()

        open_library()

        library_opened = exists(Library.OTHER_BOOKMARKS, FirefoxSettings.FIREFOX_TIMEOUT)
        assert library_opened is True, 'Library opened'

        click(Library.OTHER_BOOKMARKS)

        bookmark_exists = exists(soap_wiki_tab_pattern)
        assert bookmark_exists is True, 'Previously added bookmarks are displayed'

        right_click(soap_wiki_tab_pattern)

        copy_option_exists = exists(copy_option_pattern)
        assert copy_option_exists is True, 'Copy option exists'

        click(copy_option_pattern)

        bookmarks_toolbar_folder_exists = exists(Library.BOOKMARKS_TOOLBAR)
        assert bookmarks_toolbar_folder_exists is True, 'Bookmarks toolbar folder exists'

        click(Library.BOOKMARKS_TOOLBAR)

        other_bookmarks_width, other_bookmarks_height = Library.OTHER_BOOKMARKS.get_size()
        location_to_paste = find(Library.OTHER_BOOKMARKS).right(other_bookmarks_width * 2)

        right_click(location_to_paste)

        paste_option_exists = exists(paste_option_pattern)
        assert paste_option_exists is True, 'Paste option exists'

        click(paste_option_pattern)

        bookmark_pasted = exists(bookmark_pasted_pattern)
        assert bookmark_pasted is True, 'The file from the previous step is pasted in the selected section'

        click(Library.OTHER_BOOKMARKS)

        bookmark_not_deleted = exists(soap_wiki_tab_pattern)
        assert bookmark_not_deleted is True, 'The file from the previous step is pasted in the selected section ' \
                                             'without being deleted from the previous one'

        click(Library.TITLE)
        close_window_control('auxiliary')

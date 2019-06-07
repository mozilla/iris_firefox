# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Add a new bookmarks separator from Library',
        locale=['en-US'],
        test_case_id='169263',
        test_suite_id='2525'
    )
    def run(self, firefox):
        soap_wiki_tab_pattern = Pattern('soap_wiki_tab.png')
        separator_added_pattern = Pattern('separator_added_to_library.png')

        navigate(LocalWeb.FIREFOX_TEST_SITE)

        soap_wiki_opened = exists(LocalWeb.FIREFOX_LOGO, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert soap_wiki_opened is True, 'Firefox Test page is opened'

        bookmark_page()

        stardialog_displayed = exists(Bookmarks.StarDialog.DONE, FirefoxSettings.FIREFOX_TIMEOUT)
        assert stardialog_displayed is True, 'StarDialog displayed'

        click(Bookmarks.StarDialog.DONE)

        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)

        soap_wiki_opened = exists(soap_wiki_tab_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert soap_wiki_opened is True, 'Soap wiki page opened'

        bookmark_page()

        stardialog_displayed = exists(Bookmarks.StarDialog.DONE, FirefoxSettings.FIREFOX_TIMEOUT)
        assert stardialog_displayed is True, 'StarDialog displayed'

        click(Bookmarks.StarDialog.DONE)

        new_tab()
        select_tab('1')
        close_tab()

        open_library()

        library_opened = exists(Library.TITLE, FirefoxSettings.FIREFOX_TIMEOUT)
        assert library_opened is True, 'The Library is opened'

        click(Library.OTHER_BOOKMARKS)

        bookmark_exists = exists(soap_wiki_tab_pattern)
        assert bookmark_exists is True, 'Previously added bookmarks are displayed'

        right_click(soap_wiki_tab_pattern)

        new_bookmark_option_exists = exists(Library.Organize.NEW_SEPARATOR)
        assert new_bookmark_option_exists is True, 'New Separator option exists'

        click(Library.Organize.NEW_SEPARATOR)

        separator_added = exists(separator_added_pattern)
        assert separator_added is True, 'A new separator is displayed above the selected bookmark.'

        click(Library.TITLE)

        close_window_control('auxiliary')

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description='Remove part of the searched item',
        locale=['en-US'],
        test_case_id='127246',
        test_suite_id='2085'
    )
    def run(self, firefox):
        soap_label_pattern = LocalWeb.SOAP_WIKI_SOAP_LABEL
        soap_large_title_selected_pattern = Pattern('soap_large_title_selected.png')
        soap_large_title_unselected_pattern = Pattern('soap_large_title_unselected.png')
        soap_s_large_title_selected_pattern = Pattern('soap_s_large_title_selected.png')
        soap_so_large_title_selected_pattern = Pattern('soap_so_large_title_selected.png')
        soap_soa_large_title_selected_pattern = Pattern('soap_soa_large_title_selected.png')

        # Open Firefox and navigate to a popular website
        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)

        soap_label_exists = exists(soap_label_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert soap_label_exists, 'The page is successfully loaded.'

        # Open the Find Toolbar
        open_find()
        edit_select_all()
        edit_delete()

        find_toolbar_opened = exists(FindToolbar.FINDBAR_TEXTBOX, FirefoxSettings.FIREFOX_TIMEOUT)
        assert find_toolbar_opened, 'Find Toolbar is opened.'

        # Search for a term that appears on the page
        type('soap', interval=1)

        selected_label_exists = exists(soap_large_title_selected_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert selected_label_exists, 'The first one has a green background highlighted.'

        unselected_label_exists = exists(soap_label_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert unselected_label_exists, 'The others are not highlighted.'

        # Delete letters from the searched term, one by one
        type(Key.BACKSPACE)

        soa_selected_exists = exists(soap_soa_large_title_selected_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert soa_selected_exists, '"soa" part highlighted.'

        type(Key.BACKSPACE)

        so_selected_exists = exists(soap_so_large_title_selected_pattern)
        assert so_selected_exists, '"so" part highlighted.'

        type(Key.BACKSPACE)

        s_selected_exists = exists(soap_s_large_title_selected_pattern)
        assert s_selected_exists, '"s" part highlighted.'

        type(Key.BACKSPACE)

        soap_clean_exists = exists(soap_large_title_unselected_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert soap_clean_exists, 'Word is not highlighted.'

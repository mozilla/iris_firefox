# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description='Search on a window with a different size',
        locale=['en-US'],
        test_case_id='127247',
        test_suite_id='2085'
    )
    def run(self, firefox):
        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)

        soap_label_exists = exists(LocalWeb.SOAP_WIKI_SOAP_LABEL, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert soap_label_exists, 'The page is successfully loaded.'

        full_screen()

        open_find()
        edit_select_all()
        edit_delete()

        find_toolbar_opened = exists(FindToolbar.FINDBAR_TEXTBOX, FirefoxSettings.FIREFOX_TIMEOUT)
        assert find_toolbar_opened, 'Find Toolbar is opened.'

        paste('soap')
        click(FindToolbar.FIND_CASE_SENSITIVE)

        find_next()

        selected_label_exists = exists(LocalWeb.SOAP_WIKI_SOAP_ENVELOPE_LABEL_SELECTED,
                                       FirefoxSettings.FIREFOX_TIMEOUT)
        assert selected_label_exists, 'The first one has a green background highlighted.'

        unselected_label_exists = exists(LocalWeb.SOAP_WIKI_SOAP_XML_LABEL, FirefoxSettings.FIREFOX_TIMEOUT)
        assert unselected_label_exists, 'The others are not highlighted.'

        full_screen()

        selected_label_exists = exists(LocalWeb.SOAP_WIKI_SOAP_ENVELOPE_LABEL_SELECTED,
                                       FirefoxSettings.FIREFOX_TIMEOUT)
        assert selected_label_exists, 'The first one has a green background highlighted.'

        unselected_label_exists = exists(LocalWeb.SOAP_WIKI_SOAP_XML_LABEL, FirefoxSettings.FIREFOX_TIMEOUT)
        assert unselected_label_exists, 'The others are not highlighted.'

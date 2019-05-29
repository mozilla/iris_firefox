# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description='"Match Case" button works properly',
        locale=['en-US'],
        test_case_id='127452',
        test_suite_id='2085'
    )
    def run(self, firefox):
        soap_label_pattern = LocalWeb.SOAP_WIKI_SOAP_LABEL
        soap_xml_label_pattern = LocalWeb.SOAP_WIKI_SOAP_XML_LABEL
        soap_envelope_label_selected_pattern = LocalWeb.SOAP_WIKI_SOAP_ENVELOPE_LABEL_SELECTED
        soap_label_selected_pattern = Pattern('soap_label_selected.png')

        # Open Firefox and navigate to a popular website
        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)

        soap_label_exists = exists(soap_label_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert soap_label_exists, 'The page is successfully loaded.'

        # Open the Find Toolbar
        open_find()
        edit_select_all()
        edit_delete()

        find_toolbar_opened = exists(FindToolbar.FINDBAR_TEXTBOX, FirefoxSettings.FIREFOX_TIMEOUT)
        assert find_toolbar_opened, 'Find Toolbar is opened.'

        # Enter a search term using a word written with an upper case, activate "Match Case" and press ENTER
        type('soap', interval=1)
        click(FindToolbar.FIND_CASE_SENSITIVE)
        find_next()

        selected_label_exists = exists(soap_envelope_label_selected_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert selected_label_exists, 'The first one has a green background highlighted.'

        unselected_label_exists = exists(soap_xml_label_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert unselected_label_exists, 'The others are not highlighted.'

        # Navigate through the result
        find_next()

        first_label_is_green = exists(soap_label_selected_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert first_label_is_green, 'The next matching words/characters have a green background highlighted'

        other_label_is_unhighlighted = exists(soap_xml_label_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert other_label_is_unhighlighted, 'The other is not highlighted'

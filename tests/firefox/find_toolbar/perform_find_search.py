# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description='Perform a search',
        locale=['en-US'],
        test_case_id='127239',
        test_suite_id='2085'
    )
    def run(self, firefox):
        soap_label_pattern = LocalWeb.SOAP_WIKI_SOAP_LABEL
        from_wikipedia_label_pattern = Pattern('from_wikipedia_label.png')

        # Open Firefox and navigate to a popular website
        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)

        soap_label_exists = exists(soap_label_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert soap_label_exists, 'The page is successfully loaded.'

        # Open the Find toolbar
        open_find()
        edit_select_all()
        edit_delete()

        find_toolbar_opened = exists(FindToolbar.FINDBAR_TEXTBOX, FirefoxSettings.FIREFOX_TIMEOUT)
        assert find_toolbar_opened, 'Find Toolbar is opened.'

        # Enter a search term and press ENTER
        paste('From Wikipedia')
        type(Key.ENTER)

        selected_label_exists = exists(from_wikipedia_label_pattern.similar(0.6), FirefoxSettings.FIREFOX_TIMEOUT)
        assert selected_label_exists, 'All the matching words/characters are found.'

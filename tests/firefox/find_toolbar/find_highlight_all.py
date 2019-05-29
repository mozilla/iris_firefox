# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description='"Highlight All" button works properly',
        locale=['en-US'],
        test_case_id='127451',
        test_suite_id='2085'
    )
    def run(self, firefox):
        soap_label_pattern = LocalWeb.SOAP_WIKI_SOAP_LABEL
        see_label_pattern = LocalWeb.SOAP_WIKI_SEE_LABEL
        see_label_unhighlited_pattern = LocalWeb.SOAP_WIKI_SEE_LABEL_UNHIGHLITED
        see_label_pink_pattern = Pattern('see_label_pink.png')
        see_label_capital_selected_pattern = Pattern('see_label_capital_selected.png')
        see_also_label_pattern = Pattern('see_also_label.png')

        # Open Firefox and navigate to a popular website
        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)
        soap_label_exists = exists(soap_label_pattern, FirefoxSettings.FIREFOX_TIMEOUT*9)
        assert soap_label_exists, 'The page is successfully loaded.'

        # Open the Find Toolbar
        open_find()
        edit_select_all()
        edit_delete()

        find_toolbar_opened = exists(FindToolbar.FINDBAR_TEXTBOX, FirefoxSettings.FIREFOX_TIMEOUT)
        assert find_toolbar_opened, 'Find Toolbar is opened.'

        # Enter a search term and press ENTER
        type('see', interval=1)
        type(Key.ENTER)

        selected_label_exists = exists(see_label_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert selected_label_exists, 'The first one has a green background highlighted.'

        unhighlighted_label_exists = exists(see_label_unhighlited_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert unhighlighted_label_exists, 'The others are not highlighted.'

        # Click on "Highlight All"
        click(FindToolbar.HIGHLIGHT)

        first_label_is_green = exists(see_label_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert first_label_is_green, 'The first one has a green background highlighted'

        other_label_pink = exists(see_label_pink_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert other_label_pink, 'The other one has a pink background highlighted'

        # Navigate through the results
        find_next()
        find_next()

        next_matching_green_exists = exists(see_label_capital_selected_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert next_matching_green_exists, 'The next matching words/characters have a green background highlighted'

        next_matching_pink_exists = exists(see_also_label_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert next_matching_pink_exists, 'The other ones have a pink background highlighted'

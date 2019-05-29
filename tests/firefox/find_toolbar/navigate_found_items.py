# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description='Navigate through found items',
        locale=['en-US'],
        test_case_id='127249',
        test_suite_id='2085'
    )
    def run(self, firefox):
        one_of_five_label_pattern = Pattern('1_of_5_matches_label.png')
        two_of_five_label_pattern = Pattern('2_of_5_matches_label.png')

        # Open Firefox and navigate to a website
        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)

        soap_label_exists = exists(LocalWeb.SOAP_WIKI_SOAP_LABEL, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert soap_label_exists, 'The page is successfully loaded.'

        # Open the Find Toolbar
        open_find()

        edit_select_all()

        edit_delete()

        find_toolbar_opened = exists(FindToolbar.FINDBAR_TEXTBOX, FirefoxSettings.FIREFOX_TIMEOUT)
        assert find_toolbar_opened, 'Find Toolbar is opened.'

        # Search for a term that appears more than once in the page
        type('see', interval=1)

        type(Key.ENTER)

        selected_label_exists = exists(LocalWeb.SOAP_WIKI_SEE_LABEL, FirefoxSettings.FIREFOX_TIMEOUT)
        assert selected_label_exists, 'The first one has a green background highlighted.'

        not_highlighted_label_exists = exists(LocalWeb.SOAP_WIKI_SEE_LABEL_UNHIGHLITED, FirefoxSettings.FIREFOX_TIMEOUT)
        assert not_highlighted_label_exists, 'The others are not highlighted.'

        # Navigate forward and back through found items using the toolbar arrows

        click(FindToolbar.FIND_PREVIOUS.similar(0.9))

        cleaning_see_label_exists = exists(LocalWeb.SOAP_WIKI_CLEANING_SEE_SELECTED_LABEL,
                                           FirefoxSettings.FIREFOX_TIMEOUT)
        assert cleaning_see_label_exists, 'Navigation using toolbar up arrow works fine.'

        find_next_arrow = exists(FindToolbar.FIND_NEXT)
        assert find_next_arrow, 'Find next arrow available'

        find_next_location = find(FindToolbar.FIND_NEXT)

        click(find_next_location)

        selected_label_exists = exists(LocalWeb.SOAP_WIKI_SEE_LABEL, FirefoxSettings.FIREFOX_TIMEOUT)
        assert selected_label_exists, 'Navigation using toolbar down arrow works fine.'

        # Inspect if the number of the current highlighted item from the Find Toolbar changes when navigating

        click(FindToolbar.FIND_PREVIOUS)

        one_of_five_label_exists = exists(one_of_five_label_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert one_of_five_label_exists, 'The number of the highlighted item changes when ' \
                                         'navigating. ("1 of 5" expected)'

        click(find_next_location)

        two_of_five_label_exists = exists(two_of_five_label_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert two_of_five_label_exists, 'The number of the highlighted item changes when ' \
                                         'navigating. ("2 of 5" expected)'

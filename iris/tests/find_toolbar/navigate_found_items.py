# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Navigate through found items'
        self.test_case_id = '127249'
        self.test_suite_id = '2085'
        self.locales = ['en-US']

    def run(self):
        one_of_five_label_pattern = Pattern('1_of_5_matches_label.png')
        two_of_five_label_pattern = Pattern('2_of_5_matches_label.png')

        # Open Firefox and navigate to a website
        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)

        soap_label_exists = exists(LocalWeb.SOAP_WIKI_SOAP_LABEL, Settings.SITE_LOAD_TIMEOUT)
        assert_true(self, soap_label_exists, 'The page is successfully loaded.')

        # Open the Find Toolbar
        open_find()

        edit_select_all()

        edit_delete()

        find_toolbar_opened = exists(FindToolbar.FINDBAR_TEXTBOX, Settings.FIREFOX_TIMEOUT)
        assert_true(self, find_toolbar_opened, 'Find Toolbar is opened.')

        # Search for a term that appears more than once in the page
        type('see', interval=1)

        type(Key.ENTER)

        selected_label_exists = exists(LocalWeb.SOAP_WIKI_SEE_LABEL, Settings.FIREFOX_TIMEOUT)
        assert_true(self, selected_label_exists, 'The first one has a green background highlighted.')

        not_highlighted_label_exists = exists(LocalWeb.SOAP_WIKI_SEE_LABEL_UNHIGHLITED, Settings.FIREFOX_TIMEOUT)
        assert_true(self, not_highlighted_label_exists, 'The others are not highlighted.')

        # Navigate forward and back through found items using the toolbar arrows

        click(FindToolbar.FIND_PREVIOUS)

        cleaning_see_label_exists = exists(LocalWeb.SOAP_WIKI_CLEANING_SEE_SELECTED_LABEL, Settings.FIREFOX_TIMEOUT)
        assert_true(self, cleaning_see_label_exists, 'Navigation using toolbar up arrow works fine.')

        click(FindToolbar.FIND_NEXT)

        selected_label_exists = exists(LocalWeb.SOAP_WIKI_SEE_LABEL, Settings.FIREFOX_TIMEOUT)
        assert_true(self, selected_label_exists, 'Navigation using toolbar down arrow works fine.')

        # Inspect if the number of the current highlighted item from the Find Toolbar changes when navigating

        click(FindToolbar.FIND_PREVIOUS)

        one_of_five_label_exists = exists(one_of_five_label_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, one_of_five_label_exists,
                    'The number of the highlighted item changes when navigating. ("1 of 5" expected)')

        click(FindToolbar.FIND_NEXT)

        two_of_five_label_exists = exists(two_of_five_label_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, two_of_five_label_exists,
                    'The number of the highlighted item changes when navigating. ("2 of 5" expected)')

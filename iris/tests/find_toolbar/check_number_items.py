# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Check the number of found items is correctly displayed'
        self.test_case_id = '127241'
        self.test_suite_id = '2085'
        self.locales = ['en-US']

    def run(self):
        soap_label_pattern = LocalWeb.SOAP_WIKI_SOAP_LABEL
        policy_about_label_pattern = Pattern('policy_about.png')
        of_4_matches_label_pattern = Pattern('of_4_matches_label.png')
        is_about_label_pattern = Pattern('is_about_label.png')
        help_about_label_pattern = Pattern('help_about_label.png')
        about_errors_label_pattern = Pattern('about_errors_label.png')

        # Open Firefox and navigate to a popular website
        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)
        soap_label_exists = exists(soap_label_pattern, 20)
        assert_true(self, soap_label_exists, 'The page is successfully loaded.')

        # Open the Find Toolbar
        open_find()
        edit_select_all()
        edit_delete()

        find_toolbar_opened = exists(FindToolbar.FINDBAR_TEXTBOX, 10)
        assert_true(self, find_toolbar_opened, 'Find Toolbar is opened.')

        # Search for a term that appears more than once in the page
        type('about', interval=1)

        is_about_label_found = exists(is_about_label_pattern, 5)
        assert_true(self, is_about_label_found, '"is about" label found.')

        find_next()

        about_errors_label_found = exists(about_errors_label_pattern, 5)
        assert_true(self, about_errors_label_found, '"about errors" label found.')

        find_next()

        help_about_label_found = exists(help_about_label_pattern, 5)
        assert_true(self, help_about_label_found, '"help about" label found.')

        find_next()

        policy_about_label_found = exists(policy_about_label_pattern, 5)
        assert_true(self, policy_about_label_found, '"policy about" label found.')

        find_next()

        is_about_label_found_again = exists(is_about_label_pattern, 5)
        assert_true(self, is_about_label_found_again, '"is about" label is found again.')

        # Inspect if the number of matches items is displayed and it is correct
        number_of_items_found = exists(of_4_matches_label_pattern, 5)
        assert_true(self, number_of_items_found,
                    'The number of matches found on the page is displayed and it corresponds '
                    'to the actual number of items')

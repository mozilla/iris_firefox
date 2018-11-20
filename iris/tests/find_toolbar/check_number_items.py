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

        soap_label_pattern = Pattern('soap_label.png')
        find_in_page_icon_pattern = Pattern('find_in_page_icon.png')

        policy_about_label_pattern = Pattern('policy_about.png')
        of_4_matches_label_pattern = Pattern('of_4_matches_label.png')
        is_about_label_pattern = Pattern('is_about_label.png')
        help_about_label_pattern = Pattern('help_about_label.png')
        about_erros_label_pattern = Pattern('about_errors_label.png')

        test_page_local = self.get_asset_path('wiki_soap.html')
        navigate(test_page_local)

        soap_label_exists = exists(soap_label_pattern, 20)

        assert_true(self, soap_label_exists, 'The page is successfully loaded.')

        open_find()
        edit_select_all()
        edit_delete()

        find_toolbar_opened = exists(find_in_page_icon_pattern, 10)

        assert_true(self, find_toolbar_opened, 'Find Toolbar is opened.')

        type('about', interval=1)

        is_about_label_found = exists(is_about_label_pattern, 5)

        find_next()
        about_errors_label_found = exists(about_erros_label_pattern, 5)

        find_next()
        help_about_label_found = exists(help_about_label_pattern, 5)

        find_next()
        policy_about_label_found = exists(policy_about_label_pattern, 5)

        find_next()
        is_about_label_found_again = exists(is_about_label_pattern, 5)

        assert_true(self, is_about_label_found &
                    about_errors_label_found &
                    help_about_label_found &
                    policy_about_label_found &
                    is_about_label_found_again,
                    'All the matching words/characters are found.')

        number_of_items_found = exists(of_4_matches_label_pattern, 5)

        assert_true(self, number_of_items_found,
                    'The number of matches found on the page is displayed and it corresponds to the actual number of items')

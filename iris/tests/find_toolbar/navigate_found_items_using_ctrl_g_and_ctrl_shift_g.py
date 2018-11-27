# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Navigate through found items using CTRL+G / CTRL+SHIFT+G'
        self.test_case_id = '127257'
        self.test_suite_id = '2085'
        self.locales = ['en-US']

    def run(self):

        soap_label_pattern = Pattern('soap_label.png')
        operating_all_pattern = Pattern('operating_all.png')
        operating_all_highlighted_pattern = Pattern('operating_all_highlighted.png')
        operating_disparate_pattern = Pattern('operating_disparate.png')
        operating_disparate_highlighted_pattern = Pattern('operating_disparate_highlighted.png')
        one_of_two_matches_pattern = Pattern('1_of_2_matches.png')
        two_of_two_matches_pattern = Pattern('2_of_2_matches.png')

        test_page_local = self.get_asset_path('wiki_soap.html')
        navigate(test_page_local)

        soap_label_exists = exists(soap_label_pattern, 40)
        assert_true(self, soap_label_exists, 'The page is successfully loaded.')

        open_find()
        edit_select_all()
        edit_delete()

        find_toolbar_opened = exists(FindToolbar.FINDBAR_TEXTBOX, 10)
        assert_true(self, find_toolbar_opened, 'Find Toolbar is opened.')

        type('operating')

        operating_disparate_highlighted_displayed = exists(operating_disparate_highlighted_pattern, 5)
        operating_all_displayed = exists(operating_all_pattern, 5)
        assert_true(self, operating_disparate_highlighted_displayed and operating_all_displayed,
                    'All the matching words/characters are found. '
                    'The first one has a green background highlighted, and the others are not highlighted.')

        find_next()

        operating_disparate_displayed = exists(operating_disparate_pattern, 5)
        operating_all_highlighted_displayed = exists(operating_all_highlighted_pattern, 5)

        find_previous()

        operating_disparate_highlighted_displayed = exists(operating_disparate_highlighted_pattern, 5)
        operating_all_displayed = exists(operating_all_pattern, 5)
        assert_true(self, operating_disparate_displayed and operating_all_highlighted_displayed
                    and operating_disparate_highlighted_displayed and operating_all_displayed,
                    'Navigation works fine. '
                    'The current item is highlighted with green. No functional or visible issue appears.')

        find_next()

        two_of_two_matches_displayed = exists(two_of_two_matches_pattern, 5)

        find_previous()

        one_of_two_matches_displayed = exists(one_of_two_matches_pattern, 5)
        assert_true(self, one_of_two_matches_displayed and two_of_two_matches_displayed,
                    'The number of the highlighted item changes when navigating.')

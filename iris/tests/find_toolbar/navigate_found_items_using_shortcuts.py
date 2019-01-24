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
        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)
        soap_label_exists = exists(LocalWeb.SOAP_WIKI_SOAP_LABEL, 40)
        assert_true(self, soap_label_exists, 'The page is successfully loaded.')

        open_find()
        edit_select_all()
        edit_delete()

        find_toolbar_opened = exists(FindToolbar.FINDBAR_TEXTBOX, 10)
        assert_true(self, find_toolbar_opened, 'Find Toolbar is opened.')

        type('operating')

        operating_disparate_highlighted_displayed = exists(LocalWeb.SOAP_WIKI_OPERATING_DISPARATE_HIGHLIGHTED, 5)
        operating_all_displayed = exists(LocalWeb.SOAP_WIKI_OPERATING_ALL, 5)
        assert_true(self, operating_disparate_highlighted_displayed and operating_all_displayed,
                    'All the matching words/characters are found. '
                    'The first one has a green background highlighted, and the others are not highlighted.')

        find_next()

        operating_disparate_displayed = exists(LocalWeb.SOAP_WIKI_OPERATING_DISPARATE, 5)
        operating_all_highlighted_displayed = exists(LocalWeb.SOAP_WIKI_OPERATING_ALL_HIGHLIGHTED, 5)

        find_previous()

        operating_disparate_highlighted_displayed = exists(LocalWeb.SOAP_WIKI_OPERATING_DISPARATE_HIGHLIGHTED, 5)
        operating_all_displayed = exists(LocalWeb.SOAP_WIKI_OPERATING_ALL, 5)
        assert_true(self, operating_disparate_displayed and operating_all_highlighted_displayed
                    and operating_disparate_highlighted_displayed and operating_all_displayed,
                    'Navigation works fine. '
                    'The current item is highlighted with green. No functional or visible issue appears.')

        find_next()

        two_of_two_matches_displayed = exists(LocalWeb.SOAP_WIKI_2_OF_2_MATCHES, 5)

        find_previous()

        one_of_two_matches_displayed = exists(LocalWeb.SOAP_WIKI_1_OF_2_MATCHES, 5)
        assert_true(self, one_of_two_matches_displayed and two_of_two_matches_displayed,
                    'The number of the highlighted item changes when navigating.')

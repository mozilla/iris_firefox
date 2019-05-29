# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description='Navigate through found items using F3 / SHIFT+F3',
        locale=['en-US'],
        test_case_id='127256',
        test_suite_id='2085'
    )
    def run(self, firefox):
        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)

        soap_label_exists = exists(LocalWeb.SOAP_WIKI_SOAP_LABEL, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert soap_label_exists, 'The page is successfully loaded.'

        open_find()
        edit_select_all()
        edit_delete()

        find_toolbar_opened = exists(FindToolbar.FINDBAR_TEXTBOX, FirefoxSettings.FIREFOX_TIMEOUT)
        assert find_toolbar_opened, 'Find Toolbar is opened.'

        type('operating')

        operating_disparate_highlighted_displayed = exists(LocalWeb.SOAP_WIKI_OPERATING_DISPARATE_HIGHLIGHTED,
                                                           FirefoxSettings.FIREFOX_TIMEOUT)
        operating_all_displayed = exists(LocalWeb.SOAP_WIKI_OPERATING_ALL, FirefoxSettings.FIREFOX_TIMEOUT)
        assert operating_disparate_highlighted_displayed and operating_all_displayed, \
            'All the matching words/characters are found. The first one has a green background highlighted, ' \
            'and the others are not highlighted.'

        type(Key.F3)

        operating_disparate_displayed = exists(LocalWeb.SOAP_WIKI_OPERATING_DISPARATE, FirefoxSettings.FIREFOX_TIMEOUT)
        operating_all_highlighted_displayed = exists(LocalWeb.SOAP_WIKI_OPERATING_ALL_HIGHLIGHTED,
                                                     FirefoxSettings.FIREFOX_TIMEOUT)

        type(Key.F3, KeyModifier.SHIFT)

        operating_disparate_highlighted_displayed = exists(LocalWeb.SOAP_WIKI_OPERATING_DISPARATE_HIGHLIGHTED,
                                                           FirefoxSettings.FIREFOX_TIMEOUT)
        operating_all_displayed = exists(LocalWeb.SOAP_WIKI_OPERATING_ALL, FirefoxSettings.FIREFOX_TIMEOUT)
        assert operating_disparate_displayed and operating_all_highlighted_displayed and \
            operating_disparate_highlighted_displayed and operating_all_displayed, \
            'Navigation works fine. The current item is highlighted with green. No functional or visible issue appears.'

        type(Key.F3)

        two_of_two_matches_displayed = exists(LocalWeb.SOAP_WIKI_2_OF_2_MATCHES, FirefoxSettings.FIREFOX_TIMEOUT)
        type(Key.F3, KeyModifier.SHIFT)
        one_of_two_matches_displayed = exists(LocalWeb.SOAP_WIKI_1_OF_2_MATCHES, FirefoxSettings.FIREFOX_TIMEOUT)
        assert one_of_two_matches_displayed and two_of_two_matches_displayed, 'The number of the highlighted item ' \
                                                                              'changes when navigating.'

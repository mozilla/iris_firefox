# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description='Navigate through Search Links only results ',
        locale=['en-US'],
        test_case_id='127253',
        test_suite_id='2085',
        blocked_by={'id': 'issue_1628', 'platform': OSPlatform.ALL}
    )
    def run(self, firefox):
        find_in_page_links_only_icon_pattern = Pattern('find_in_page_links_only_icon.png')
        soap_link_pattern = Pattern('soap_link.png')
        soap_other_link_pattern = Pattern('soap_link_disambiguation.png')
        soap_other_link_highlighted_pattern = Pattern('soap_link_disambiguation_highlighted.png')

        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)

        soap_label_exists = exists(LocalWeb.SOAP_WIKI_SOAP_LABEL, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert soap_label_exists, 'The page is successfully loaded.'

        type("'")

        # Remove all text from the toolbar
        edit_select_all()
        edit_delete()

        find_toolbar_opened = exists(find_in_page_links_only_icon_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert find_toolbar_opened, 'Quick find (links only) toolbar is opened.'

        type('soap', interval=1)

        found_link_highlighted_green = exists(LocalWeb.SOAP_WIKI_SOAP_LINK_HIGHLIGHTED, FirefoxSettings.FIREFOX_TIMEOUT)
        assert found_link_highlighted_green, 'Matching link is found.'

        # Other link doesn't have pink background

        # https://support.mozilla.org/en-US/questions/1260455 says that "Highlight All" option is turned off by default.
        # Test case 127253 needs to be rewritten.

        assert False, 'Other links are pink. [Known issue other links do not have pink background]'

        type(Key.F3)

        soap_link_not_highlighted = exists(soap_link_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        soap_other_link_highlighted = exists(soap_other_link_highlighted_pattern, FirefoxSettings.FIREFOX_TIMEOUT)

        type(Key.F3, KeyModifier.SHIFT)

        soap_link_highlighted = exists(LocalWeb.SOAP_WIKI_SOAP_LINK_HIGHLIGHTED, FirefoxSettings.FIREFOX_TIMEOUT)
        soap_other_link_not_highlighted = exists(soap_other_link_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert soap_link_not_highlighted and soap_other_link_highlighted and soap_link_highlighted and \
            soap_other_link_not_highlighted, 'The green box is moved with the current item'

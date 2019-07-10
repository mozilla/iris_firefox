# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description='Search Links only',
        locale=['en-US'],
        test_case_id='127252',
        test_suite_id='2085',
        blocked_by={'id': 'issue_1628', 'platform': OSPlatform.ALL}
    )
    def run(self, firefox):
        find_in_page_links_only_icon_pattern = Pattern('find_in_page_links_only_icon.png')
        find_in_page_links_only_soap_pattern = Pattern('find_links_only_part.png')
        LocalWeb.SOAP_WIKI_SOAP_LINK_HIGHLIGHTED.similarity = 0.6

        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)

        soap_label_exists = exists(LocalWeb.SOAP_WIKI_SOAP_LABEL, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert soap_label_exists, 'The page is successfully loaded.'

        type("'")

        # Remove all text from the toolbar
        edit_select_all()
        edit_delete()

        find_toolbar_opened = exists(find_in_page_links_only_icon_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert find_toolbar_opened, 'Find Toolbar (links only) is opened.'

        type('soap', interval=1)

        found_link_highlighted_green = exists(LocalWeb.SOAP_WIKI_SOAP_LINK_HIGHLIGHTED,
                                              FirefoxSettings.FIREFOX_TIMEOUT)
        assert found_link_highlighted_green, 'Matching link is found.'

        # Other link doesn't have pink background

        # https://support.mozilla.org/en-US/questions/1260455 says that "Highlight All" option is turned off by default.
        # Test case 127252 needs to be rewritten.

        # other_link_highlighted_pink = exists(soap_another_link_pattern, 10)
        assert False, 'Other links are pink. [Known issue other links do not have pink background]'

        try:
            search_links_only_toolbar_disappeared = wait_vanish(find_in_page_links_only_soap_pattern,
                                                                FirefoxSettings.SITE_LOAD_TIMEOUT)
            assert search_links_only_toolbar_disappeared, 'The Findbar is disappeared'
        except FindError:
            raise FindError('The Findbar is NOT disappeared')

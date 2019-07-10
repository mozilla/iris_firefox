# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description='Navigate through Quick Find items',
        locale=['en-US'],
        test_case_id='127260',
        test_suite_id='2085',
        blocked_by={'id': 'issue_1628', 'platform': OSPlatform.ALL}
    )
    def run(self, firefox):
        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)

        soap_label_exists = exists(LocalWeb.SOAP_WIKI_SOAP_LABEL, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert soap_label_exists, 'The page is successfully loaded.'

        type('/')
        edit_select_all()
        edit_delete()

        find_toolbar_opened = exists(FindToolbar.QUICK_FIND_LABEL, FirefoxSettings.FIREFOX_TIMEOUT)
        assert find_toolbar_opened, 'Find Toolbar is opened.'

        type('see', interval=1)

        selected_label_exists = exists(LocalWeb.SOAP_WIKI_CLEANING_SEE_SELECTED_LABEL, FirefoxSettings.FIREFOX_TIMEOUT)
        assert selected_label_exists, 'The first one has a green background highlighted.'

        type(Key.F3)

        changed_selection_exists = exists(LocalWeb.SOAP_WIKI_SEE_LABEL)
        assert changed_selection_exists, 'The green box is moved on next.'

        # https://support.mozilla.org/en-US/questions/1260455 says that "Highlight All" option is turned off by default.
        # Test case 127260 needs to be rewritten.

        assert False, 'The others are not highlighted as pink [known issue]'

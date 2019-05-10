# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='This test case checks the \'Paste & Go\' option if CRLF exists at the end of clipboard url.',
        locale=['en-US'],
        test_case_id='117523',
        test_suite_id='1902'
    )
    def run(self, firefox):

        navigate(LocalWeb.FIREFOX_TEST_SITE)

        expected = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert expected, 'Page successfully loaded, firefox logo found.'

        select_location_bar()
        edit_copy()

        new_tab()
        right_click(NavBar.HAMBURGER_MENU.target_offset(-400, 10))

        # Select 'Paste & Go' option.
        select_location_bar_option(RightClickLocationBar.PASTE_GO)

        expected = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert expected, 'Page successfully loaded after \'Paste & Go\' option is selected.'

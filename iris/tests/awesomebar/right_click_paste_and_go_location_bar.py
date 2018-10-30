# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'This test case checks the \'Paste & Go\' option if CRLF exists at the end of clipboard url.'
        self.test_case_id = '117523'
        self.test_suite_id = '1902'
        self.locales = ['en-US', 'zh-CN', 'es-ES', 'fr', 'de', 'ru', 'ko', 'pt-PT', 'vi', 'pl', 'tr', 'ro', 'ja']

    def run(self):
        url = LocalWeb.FIREFOX_TEST_SITE

        navigate(url)
        expected = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert_true(self, expected, 'Page successfully loaded, firefox logo found.')

        select_location_bar()

        # Copy selection to clipboard.
        edit_copy()

        new_tab()

        # Open menu from the location bar by pressing the right click.
        right_click(NavBar.HAMBURGER_MENU.target_offset(-400, 10))

        # Select 'Paste & Go' option.
        select_location_bar_option(RightClickLocationBar.PASTE_GO)

        expected = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert_true(self, expected, 'Page successfully loaded after \'Paste & Go\' option is selected.')

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from iris.api.core.mouse import middle_click
from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Middle clicking search results does not open a new tab.'
        self.test_case_id = '111373'
        self.test_suite_id = '83'
        self.locale = ['en-US']

    def run(self):
        test_bold_pattern = Pattern('test_bold.png')

        # Enable the search bar.
        change_preference('browser.search.widget.inNavBar', True)

        select_search_bar()
        paste('test')
        time.sleep(DEFAULT_UI_DELAY_LONG)

        expected = exists(test_bold_pattern, 10)
        assert_true(self, expected, 'Search suggestions are displayed in the search bar.')

        middle_click(test_bold_pattern)
        time.sleep(DEFAULT_UI_DELAY_LONG)

        expected = exists(test_bold_pattern, 10)
        assert_true(self, expected, 'The search box stays in focus after middle click.')

        next_tab()
        select_location_bar()
        url_text = copy_to_clipboard()

        assert_contains(self, url_text, 'test', 'A new tab is opened and contains the searched item.')

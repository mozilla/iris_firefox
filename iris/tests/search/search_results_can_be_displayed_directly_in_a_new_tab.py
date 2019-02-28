# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Search results can be displayed directly in a new tab.'
        self.test_case_id = '4266'
        self.test_suite_id = '83'
        self.locale = ['en-US']

    def run(self):
        iris_logo_tab_pattern = Pattern('iris_logo_tab.png')
        test_pattern = Pattern('test.png')

        change_preference('browser.search.widget.inNavBar', True)

        select_search_bar()
        paste('test')
        key_down(Key.ALT)
        type(Key.ENTER)
        time.sleep(DEFAULT_UI_DELAY_LONG)
        key_up(Key.ALT)

        expected = exists(iris_logo_tab_pattern, 10)
        assert_true(self, expected, 'Iris tab is not in focus.')

        expected = exists(test_pattern, 10)
        assert_true(self, expected, 'The search results are shown in a new tab.')

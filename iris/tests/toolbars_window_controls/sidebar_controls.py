# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'This is a test of the sidebar controls'
        self.test_case_id = '119466'
        self.test_suite_id = '1998'
        self.locales = ['en-US']

    def run(self):
        x_button_sidebar_pattern = Pattern('x_button_sidebar.png')
        x_button_sidebar_hovered_pattern = Pattern('x_button_sidebar_hovered.png')
        sidebar_title_pattern = Pattern('sidebar_title.png')

        bookmarks_sidebar('open')
        expected_1 = exists(sidebar_title_pattern, 10)
        assert_true(self, expected_1, 'Sidebar title was displayed properly')

        in_region = Region(0, find(sidebar_title_pattern).y, SCREEN_WIDTH / 4, SCREEN_HEIGHT / 4)
        expected_2 = in_region.exists(x_button_sidebar_pattern, 10)
        assert_true(self, expected_2, 'Close button was displayed properly')

        in_region.hover(x_button_sidebar_pattern)
        expected_3 = in_region.exists(x_button_sidebar_hovered_pattern, 10)
        assert_true(self, expected_3, 'Hover state displayed properly')

        in_region.click(x_button_sidebar_hovered_pattern)
        try:
            expected_4 = wait_vanish(sidebar_title_pattern, 10)
            assert_true(self, expected_4, 'Sidebar was closed successfully')
        except FindError:
            raise FindError('Sidebar is still open')

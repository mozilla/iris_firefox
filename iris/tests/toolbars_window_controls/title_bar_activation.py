# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'This is a test case that checks if the Title Bar can be activated/deactivated properly from ' \
                    'Customize menu'
        self.test_case_id = '118183'
        self.test_suite_id = '1998'
        self.locales = ['en-US']

    def run(self):

        navigate('about:home')

        activate_title_bar_pattern = Pattern('title_bar.png')
        active_title_bar_pattern = Pattern('active_title_bar.png')
        deactivate_title_bar_pattern = Pattern('deactivate_title_bar.png')

        click_hamburger_menu_option('Customize...')

        if Settings.get_os() == Platform.LINUX:

            expected_2 = exists(active_title_bar_pattern, 10)
            assert_true(self, expected_2, 'Title Bar can be deactivated')

            click(deactivate_title_bar_pattern)

            try:
                expected_3 = wait_vanish(deactivate_title_bar_pattern, 10)
                assert_true(self, expected_3, 'Title Bar has been successfully deactivated')
            except FindError:
                raise FindError('Title Bar can not be closed')
        else:

            expected_1 = exists(activate_title_bar_pattern, 10)
            assert_true(self, expected_1, 'Title Bar can be activated')

            click(activate_title_bar_pattern)

            expected_2 = exists(active_title_bar_pattern, 10)
            assert_true(self, expected_2, 'Title Bar can be deactivated')

            click(deactivate_title_bar_pattern)

            try:
                expected_3 = wait_vanish(active_title_bar_pattern, 10)
                assert_true(self, expected_3, 'Title Bar has been successfully deactivated')
            except FindError:
                raise FindError('Title Bar can not be closed')

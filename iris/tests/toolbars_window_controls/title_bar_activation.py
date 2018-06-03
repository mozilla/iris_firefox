# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This is a test case that checks if the Title Bar can be activated/deactivated properly from ' \
                    'Customize menu'

    def run(self):

        url = 'about:home'
        navigate(url)

        activate_title_bar = 'title_bar.png'
        active_title_bar = 'active_title_bar.png'
        deactivate_title_bar = 'deactivate_title_bar.png'

        click_hamburger_menu_option('Customize...')

        if Settings.getOS() == Platform.LINUX:

            expected_2 = exists(active_title_bar, 10)
            assert_true(self, expected_2, 'Title Bar can be deactivated')

            click(deactivate_title_bar)

            try:
                expected_3 = waitVanish(deactivate_title_bar, 10)
                assert_true(self, expected_3, 'Title Bar has been successfully deactivated')
            except Exception as error:
                logger.error('Title Bar can not be closed')
                raise error

        else:

            expected_1 = exists(activate_title_bar, 10)
            assert_true(self, expected_1, 'Title Bar can be activated')

            click(activate_title_bar)

            expected_2 = exists(active_title_bar, 10)
            assert_true(self, expected_2, 'Title Bar can be deactivated')

            click(deactivate_title_bar)

            try:
                expected_3 = waitVanish(active_title_bar, 10)
                assert_true(self, expected_3, 'Title Bar has been successfully deactivated')
            except Exception as error:
                logger.error('Title Bar can not be closed')
                raise error

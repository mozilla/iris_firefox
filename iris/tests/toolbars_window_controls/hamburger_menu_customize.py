# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This is a test case that checks the Hamburger menu > Customize opens the customize page'
        self.locales = ['en-US']
  
    def run(self):
        navigate('about:home')

        click_hamburger_menu_option('Customize...')

        expected_1 = exists(Pattern('zoom_controls_customize_page.png'), 10)
        assert_true(self, expected_1, '\'Customize\' page present.')
        close_customize_page()

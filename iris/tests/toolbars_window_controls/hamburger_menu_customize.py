# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This is a test case that checks the Hamburger menu > Customize opens the customize page'
  
    def run(self):
        url = 'about:home'
        navigate(url)

        # Open Customize from the Hamburger Menu

        click_hamburger_menu_option('Customize...')
        time.sleep(1)

        # Searching for text 'Drag'
        expected_1 = exists('Drag', 10, in_region=Region(0, 0, screen_width/3, screen_height/4))
        assert_true(self, expected_1, '\'Customize\' page present.')
        close_customize_page()

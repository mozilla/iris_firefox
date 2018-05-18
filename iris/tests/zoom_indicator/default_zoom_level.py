# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This is a test case that checks the default zoom level'

    def run(self):
        url = 'about:home'
        search_bar = 'search_bar.png'
        hamburger_menu = 'hamburger_menu.png'
        hamburger_menu_zoom_indicator = 'hamburger_menu_zoom_indicator.png'
        edit_buttons_below_zoom_buttons = 'edit_buttons_below_zoom_buttons.png'

        navigate(url)

        expected = exists(hamburger_menu, 10)
        assert_true(self, expected, 'Page successfully loaded, hamburger menu found.')

        coord = find(hamburger_menu)
        x_reg = coord.getX() - 350
        y_reg = coord.getY() - 30

        region = Region(x_reg, y_reg, coord.getX() - x_reg, screen_height / 4)

        expected = region.exists(search_bar, 10)
        assert_true(self, expected, 'Zoom level not displayed by default in the url bar.')

        click(hamburger_menu)

        time.sleep(1)

        new_region = Region(x_reg, y_reg, coord.getX() - x_reg + 50, screen_height / 2)

        expected = new_region.exists(hamburger_menu_zoom_indicator, 10)
        assert_true(self, expected, 'Zoom level is 100% by default.')

        expected = new_region.exists(edit_buttons_below_zoom_buttons, 10)
        assert_true(self, expected, 'Control buttons for zooming appear above the Cut/Copy/Paste buttons.')

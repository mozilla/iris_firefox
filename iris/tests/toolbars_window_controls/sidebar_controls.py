# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This is a test of the sidebar controls'

    def run(self):
        x_button_sidebar = 'x_button_sidebar.png'
        x_button_sidebar_hovered = 'x_button_sidebar_hovered.png'
        sidebar_title = 'sidebar_title.png'

        bookmarks_sidebar()
        expected_1 = exists(sidebar_title, 10)
        assert_true(self, expected_1, 'Sidebar title was displayed properly')

        in_region = Region(0, find(sidebar_title).getY(), SCREEN_WIDTH / 4, SCREEN_HEIGHT / 4)
        expected_2 = in_region.exists(x_button_sidebar, 10)
        assert_true(self, expected_2, 'Close button was displayed properly')

        in_region.hover(x_button_sidebar)
        expected_3 = in_region.exists(x_button_sidebar_hovered, 10)
        assert_true(self, expected_3, 'Hover state displayed properly')

        in_region.click(x_button_sidebar_hovered)
        try:
            expected_4 = waitVanish(sidebar_title, 10)
            assert_true(self, expected_4, 'Sidebar was closed successfully')
        except:
            raise FindError('Sidebar is still open')

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = "This is a test of the sidebar controls"

    def run(self):
        x_button_sidebar = 'x_button_sidebar.png'
        x_button_sidebar_hovered = 'x_button_sidebar_hovered.png'
        sidebar_title = 'sidebar_title.png'

        bookmarks_sidebar()
        expected_1 = exists(x_button_sidebar, 10)
        assert_true(self, expected_1, 'Sidebar was opened successfully')

        hover(x_button_sidebar)
        expected_2 = exists(x_button_sidebar_hovered, 10)
        assert_true(self, expected_2, 'Hover state displayed properly')

        click(x_button_sidebar_hovered)
        try:
            expected_3 = waitVanish(sidebar_title, 10)
            assert_true(self, expected_3, 'Sidebar was closed successfully')
        except:
            logger.error('Sidebar is still open')

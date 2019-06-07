# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description='This is a test of the sidebar controls.',
        locale=['en-US'],
        test_case_id='119466',
        test_suite_id='1998'
    )
    def run(self, firefox):
        x_button_sidebar_pattern = Pattern('x_button_sidebar.png')
        x_button_sidebar_hovered_pattern = Pattern('x_button_sidebar_hovered.png')
        sidebar_title_pattern = Pattern('sidebar_title.png')

        bookmarks_sidebar('open')
        assert exists(sidebar_title_pattern, 10), 'Sidebar title was displayed properly.'

        region = Region(0, find(sidebar_title_pattern).y, Screen.SCREEN_WIDTH / 4, Screen.SCREEN_HEIGHT / 4)
        assert region.exists(x_button_sidebar_pattern, 10), 'Close button was displayed properly.'

        region.hover(x_button_sidebar_pattern)
        assert region.exists(x_button_sidebar_hovered_pattern, 10), 'Hover state displayed properly.'

        region.click(x_button_sidebar_hovered_pattern)
        try:
            assert wait_vanish(sidebar_title_pattern, 10), 'Sidebar was closed successfully.'
        except FindError:
            raise FindError('Sidebar is still open.')

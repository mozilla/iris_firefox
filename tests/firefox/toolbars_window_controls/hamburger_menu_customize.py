# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description='This is a test case that checks the Hamburger menu > Customize opens the customize page.',
        locale=['en-US']
    )
    def run(self, firefox):
        navigate('about:home')

        click_hamburger_menu_option('Customize...')

        assert exists(NavBar.ZOOM_CONTROLS_CUSTOMIZE_PAGE, 10), '\'Customize\' page present.'
        close_customize_page()

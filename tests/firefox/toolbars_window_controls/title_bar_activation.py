# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description='Checks if the Title Bar can be activated/deactivated properly from Customize menu',
        locale=['en-US'],
        test_case_id='118183',
        test_suite_id='1998'
    )
    def run(self, firefox):
        navigate('about:home')

        activate_title_bar_pattern = Pattern('title_bar.png')
        active_title_bar_pattern = Pattern('active_title_bar.png')
        deactivate_title_bar_pattern = Pattern('deactivate_title_bar.png')

        click_hamburger_menu_option('Customize...')

        if OSHelper.is_linux():
            assert exists(active_title_bar_pattern, 10), 'Title Bar can be deactivated.'
            click(deactivate_title_bar_pattern)

            try:
                assert wait_vanish(deactivate_title_bar_pattern, 10), 'Title Bar has been successfully deactivated.'
            except FindError:
                raise FindError('Title Bar can not be closed')
        else:

            assert exists(activate_title_bar_pattern, 10), 'Title Bar can be activated.'

            click(activate_title_bar_pattern)
            assert exists(active_title_bar_pattern, 10), 'Title Bar can be deactivated.'

            click(deactivate_title_bar_pattern)

            try:
                assert wait_vanish(active_title_bar_pattern, 10), 'Title Bar has been successfully deactivated.'
            except FindError:
                raise FindError('Title Bar can not be closed')

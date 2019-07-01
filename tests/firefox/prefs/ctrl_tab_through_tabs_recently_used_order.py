# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='The CTRL + TAB shortcut can be set to cycle through tabs in recently used order',
        test_case_id='143549',
        test_suite_id='2241',
        locale=['en-US']
    )
    def run(self, firefox):
        navigate('about:preferences')

        assert exists(AboutPreferences.PRIVACY_AND_SECURITY_BUTTON_NOT_SELECTED, FirefoxSettings.SITE_LOAD_TIMEOUT),\
            'about:preferences page loaded.'

        # From "Tabs" check the box for "Ctrl+Tab cycles through tabs in recently used order".
        assert find_in_region_from_pattern(ctrl_tab_cycles_order_checked_pattern, AboutPreferences.CHECKED_BOX), \
            'The box for "Ctrl+Tab cycles is checked.'

        # Open a few sites and navigate through them in a specific order (remember the order you visited them).
        new_tab()
        navigate(LocalWeb.POCKET_TEST_SITE)

        assert exists(LocalWeb.POCKET_LOGO, FirefoxSettings.SITE_LOAD_TIMEOUT), 'Pocket site loaded.'

        new_tab()
        navigate(LocalWeb.FIREFOX_TEST_SITE)

        assert exists(LocalWeb.FIREFOX_LOGO, FirefoxSettings.SITE_LOAD_TIMEOUT), 'Firefox site loaded.'

        new_tab()
        navigate(LocalWeb.FOCUS_TEST_SITE)

        assert exists(LocalWeb.FOCUS_LOGO, FirefoxSettings.SITE_LOAD_TIMEOUT), 'Focus site loaded.'

        select_tab(2)
        select_tab(4)
        select_tab(3)

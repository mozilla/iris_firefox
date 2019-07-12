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
        ctrl_tab_cycles_order_checked_pattern = Pattern('ctrl_tab_cycles_order_checked.png')
        ctrl_tab_cycles_order_unchecked_pattern = Pattern('ctrl_tab_cycles_order_unchecked.png')
        ctrl_tab_focus_logo_pattern = Pattern('ctrl_tab_focus_logo.png')
        ctrl_tab_firefox_pattern = Pattern('ctrl_tab_firefox.png')
        ctrl_tab_focus_pattern = Pattern('ctrl_tab_focus.png')
        ctrl_tab_pocket_pattern = Pattern('ctrl_tab_pocket.png')
        ctrl_tab_focus_active_pattern = Pattern('ctrl_tab_focus_active.png')

        navigate('about:preferences#general')

        about_preferences = exists(AboutPreferences.PRIVACY_AND_SECURITY_BUTTON_NOT_SELECTED,
                                   FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert about_preferences, 'about:preferences page loaded.'

        # From "Tabs" check the box for "Ctrl+Tab cycles through tabs in recently used order".
        ctrl_tab_cycles = exists(ctrl_tab_cycles_order_unchecked_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert ctrl_tab_cycles, '"Ctrl+Tab cycles is checked" option is available.'

        click(ctrl_tab_cycles_order_unchecked_pattern)

        ctrl_tab_cycles_order_checked = find_in_region_from_pattern(ctrl_tab_cycles_order_checked_pattern,
                                                                    AboutPreferences.CHECKED_BOX)
        assert ctrl_tab_cycles_order_checked, 'The box for "Ctrl+Tab cycles is checked."'

        # Open a few sites and navigate through them in a specific order (remember the order you visited them).
        new_tab()
        navigate(LocalWeb.POCKET_TEST_SITE)

        pocket_site = exists(LocalWeb.POCKET_LOGO, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert pocket_site, 'Pocket site loaded.'

        new_tab()
        navigate(LocalWeb.FIREFOX_TEST_SITE)

        firefox_site = exists(LocalWeb.FIREFOX_LOGO, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert firefox_site, 'Firefox site loaded.'

        new_tab()
        navigate(LocalWeb.FOCUS_TEST_SITE)

        focus_site = exists(LocalWeb.FOCUS_LOGO, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert focus_site, 'Focus site loaded.'

        select_tab(2)
        select_tab(4)
        select_tab(3)

        try:

            key_down(Key.CTRL)

            type(Key.TAB)

            ctrl_tab_focus_logo = exists(ctrl_tab_focus_logo_pattern)
            assert ctrl_tab_focus_logo, 'Ctrl+Tab switcher appears.'

            ctrl_tab_firefox = exists(ctrl_tab_firefox_pattern)
            ctrl_tab_firefox_x = find(ctrl_tab_firefox_pattern).x
            assert ctrl_tab_firefox, 'Firefox tab appears in Ctrl+Tab switcher.'

            ctrl_tab_focus = exists(ctrl_tab_focus_pattern)
            ctrl_tab_focus_x = find(ctrl_tab_focus_pattern).x
            assert ctrl_tab_focus, 'Focus tab appears in Ctrl+Tab switcher.'

            ctrl_tab_pocket = exists(ctrl_tab_pocket_pattern)
            ctrl_tab_pocket_x = find(ctrl_tab_pocket_pattern).x
            assert ctrl_tab_pocket, 'Pocket tab appears in Ctrl+Tab switcher.'

            assert ctrl_tab_firefox_x < ctrl_tab_focus_x < ctrl_tab_pocket_x, 'The order of the tabs are ' \
                                                                              'the same as in step 3. '

            type(Key.TAB)

            try:
                ctrl_tab_focus_not_active = wait_vanish(ctrl_tab_focus_active_pattern.similar(0.99))
            except FindError:
                raise APIHelperError('The focus is not shifted between the tabs.')

            assert ctrl_tab_focus_not_active, 'If you continue to press Tab, the focus is shifted between the tabs.'

        except FindError:
            key_up(Key.CTRL)
            key_up(Key.TAB)

            raise FindError('Could not find patter while using Ctrl+Tab switcher.')

        key_up(Key.CTRL)

        ctrl_tab_focus_logo = exists(ctrl_tab_focus_logo_pattern)
        assert ctrl_tab_focus_logo is False, 'The switcher disappears.'

        pocket_site = exists(LocalWeb.POCKET_LOGO, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert pocket_site, 'Pocket site loaded. The focus is on the last tab that was selected in the switcher. '

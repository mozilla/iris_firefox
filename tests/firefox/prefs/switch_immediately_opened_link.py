# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Firefox can be set switch immediately to an opened link inside a new tab',
        test_case_id='161471',
        test_suite_id='2241',
        locale=['en-US'],
        preferences={'browser.tabs.loadinBackground': False},
    )
    def run(self, firefox):
        navigate_load_listener_page_title_pattern = Pattern('navigate_page_title.png').similar(0.6)
        when_you_open_link_checked_pattern = Pattern('when_you_open_link_checked.png')
        when_you_open_link_unchecked_pattern = Pattern('when_you_open_link_unchecked.png')
        page_one_active_tab_pattern = Pattern('page_one_active_tab.png')
        page_two_active_tab_pattern = Pattern('page_two_active_tab.png')
        page_one_inactive_tab_pattern = Pattern('page_one_inactive_tab.png')
        page_two_button_pattern = Pattern('link_load_listener.png').similar(0.6)
        page_one = self.get_asset_path('page_1.htm')

        navigate('about:preferences')

        page_loaded = exists(AboutPreferences.PRIVACY_AND_SECURITY_BUTTON_NOT_SELECTED)
        assert page_loaded, 'about:preferences page loaded.'

        # From "Tabs" check the box for "When you open a link in a new tab, switch to it immediately".

        when_you_open_link_checked = find_in_region_from_pattern(when_you_open_link_checked_pattern,
                                                                 AboutPreferences.CHECKED_BOX)

        if not when_you_open_link_checked:
            when_you_open_link_unchecked = find_in_region_from_pattern(when_you_open_link_unchecked_pattern,
                                                                       AboutPreferences.UNCHECKED_BOX)
            assert when_you_open_link_unchecked, '"When you open..." is unchecked.'

            click(when_you_open_link_unchecked_pattern)

        when_you_open_link_checked = find_in_region_from_pattern(when_you_open_link_checked_pattern,
                                                                 AboutPreferences.CHECKED_BOX)
        assert when_you_open_link_checked, '"When you open a link in a new tab, switch to it immediately"' \
                                           ' is checked.'

        new_tab()

        navigate(page_one)

        page_one_active_tab = exists(page_one_active_tab_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert page_one_active_tab, 'The page is successfully loaded.'

        page_two_button = exists(page_two_button_pattern)
        assert page_two_button, 'Try it button available'

        # The link opens in a new tab that is immediately focused.

        middle_click(page_two_button_pattern)

        page_two_loaded = exists(navigate_load_listener_page_title_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert page_two_loaded, 'The browser navigated to page two.'

        page_one_inactive_tab = exists(page_one_inactive_tab_pattern, FirefoxSettings.TINY_FIREFOX_TIMEOUT)
        assert page_one_inactive_tab, 'Tab one is inactive.'

        page_two_active_tab = exists(page_two_active_tab_pattern)
        assert page_two_active_tab, 'Tab two is active. \n The link opens in a new tab that is immediately focused.'

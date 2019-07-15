# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Links can be set to open in tabs instead of new windows',
        test_case_id='143550',
        test_suite_id='2241',
        locale=['en-US'],
    )
    def run(self, firefox):
        navigate_load_listener_page_title_pattern = Pattern('navigate_page_title.png').similar(0.6)
        open_links_unchecked_pattern = Pattern('open_links_unchecked.png')
        open_links_checked_pattern = Pattern('open_links_checked.png')
        page_one_active_tab_pattern = Pattern('page_one_active_tab.png')
        page_two_active_tab_pattern = Pattern('page_two_active_tab.png')
        page_one_inactive_tab_pattern = Pattern('page_one_inactive_tab.png')
        page_two_button_pattern = Pattern('link_load_listener.png').similar(0.6)

        navigate('about:preferences')

        page_loaded = exists(AboutPreferences.PRIVACY_AND_SECURITY_BUTTON_NOT_SELECTED)
        assert page_loaded, 'about:preferences page loaded.'

        # From "Tabs" check the box for "Open links in tabs instead of new windows".
        open_links_unchecked = find_in_region_from_pattern(open_links_unchecked_pattern, AboutPreferences.UNCHECKED_BOX)

        if not open_links_unchecked:
            click(open_links_checked_pattern)

        open_links_unchecked = find_in_region_from_pattern(open_links_unchecked_pattern, AboutPreferences.UNCHECKED_BOX)
        assert open_links_unchecked, '"Open links in tabs instead of new windows" is unchecked.'

        click(open_links_unchecked_pattern)

        page_one = self.get_asset_path('page_1.htm')

        new_tab()

        navigate(page_one)

        page_one_active_tab = exists(page_one_active_tab_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert page_one_active_tab, 'The page is successfully loaded.'

        page_two_button = exists(page_two_button_pattern)
        assert page_two_button, 'Try it button available'

        # The link opens in a new tab that is immediately focused.

        click(page_two_button_pattern)

        page_two_loaded = exists(navigate_load_listener_page_title_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert page_two_loaded, 'The browser navigated to page two.'

        page_one_inactive_tab = exists(page_one_inactive_tab_pattern, FirefoxSettings.TINY_FIREFOX_TIMEOUT)
        assert page_one_inactive_tab, 'Tab one is inactive.'

        page_two_active_tab = exists(page_two_active_tab_pattern)
        assert page_two_active_tab, 'Tab two is active. \n The link opens in a new tab that is immediately focused.'

        select_tab(1)

        open_links_checked = find_in_region_from_pattern(open_links_checked_pattern, AboutPreferences.CHECKED_BOX)
        assert open_links_checked, '"Open links in tabs instead of new windows" is checked.'

        click(open_links_checked_pattern)

        open_links_unchecked = find_in_region_from_pattern(open_links_unchecked_pattern, AboutPreferences.UNCHECKED_BOX)
        assert open_links_unchecked, '"Open links in tabs instead of new windows" is unchecked.'

        select_tab(2)

        page_one_inactive_tab = exists(page_one_inactive_tab_pattern)
        assert page_one_inactive_tab, 'Tab one is inactive.'

        # Click a link (e.g "load listener")
        page_two_button = exists(page_two_button_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert page_two_button, 'Link "load listener" found'

        click(page_two_button_pattern, 1)

        page_two_active_tab = exists(page_two_active_tab_pattern)
        assert page_two_active_tab, 'Page two loaded.'

        time.sleep(FirefoxSettings.SHORT_FIREFOX_TIMEOUT)

        page_one_inactive_tab = exists(page_one_inactive_tab_pattern)
        assert page_one_inactive_tab is False, 'The Page 2 link opens in a new window.'

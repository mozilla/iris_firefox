# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from targets.firefox.firefox_ui.tabs import Tabs
from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='[Kaspersky] No crash or bluescreen after closing a pinned tab',
        locale=['en-US'],
        test_case_id='219585',
        test_suite_id='3063'
    )
    def run(self, firefox):
        close_tab_pattern = Pattern('close_tab_item.png')
        pin_tab_pattern = Pattern('pin_tab_item.png')
        mozilla_tab_pattern = Pattern('mozilla_tab.png')
        mozilla_pinned_tab_pattern = Pattern('mozilla_pinned_tab.png')
        firefox_tab_pattern = Pattern('firefox_tab.png')
        firefox_pinned_tab_pattern = Pattern('firefox_pinned_tab.png')
        focus_tab_pattern = Pattern('focus_tab.png').similar(0.6)
        focus_pinned_tab_pattern = Pattern('focus_pinned_tab.png')

        new_tab()
        navigate(LocalWeb.FIREFOX_TEST_SITE)

        firefox_tab_opened = exists(firefox_tab_pattern)
        assert firefox_tab_opened, 'Second webpage is opened'

        right_click(firefox_tab_pattern)

        unpinned_dropdown_opened = exists(pin_tab_pattern)
        assert unpinned_dropdown_opened, 'Dropdown for common tab opened'

        click(pin_tab_pattern)

        second_tab_pinned = exists(firefox_pinned_tab_pattern)
        assert second_tab_pinned, 'Second tab is pinned'

        new_tab()
        navigate(LocalWeb.FOCUS_TEST_SITE)

        focus_tab_opened = exists(focus_tab_pattern)
        assert focus_tab_opened, 'Third tab is opened'

        right_click(focus_tab_pattern)
        click(pin_tab_pattern)

        focus_tab_pinned = exists(focus_pinned_tab_pattern)
        assert focus_tab_pinned, 'Third tab is pinned'

        new_tab()
        navigate(LocalWeb.MOZILLA_TEST_SITE)

        mozilla_webpage_loaded = exists(mozilla_tab_pattern, Settings.DEFAULT_SITE_LOAD_TIMEOUT)
        assert mozilla_webpage_loaded, 'First webpage is loaded.'

        right_click(mozilla_tab_pattern)

        unpinned_dropdown_opened_second_time = exists(pin_tab_pattern)
        assert unpinned_dropdown_opened_second_time, 'Right-click menu for unpinned displayed'

        click(pin_tab_pattern)

        first_tab_pinned = exists(mozilla_pinned_tab_pattern)
        assert first_tab_pinned, 'First tab is pinned'

        right_click(mozilla_pinned_tab_pattern)

        pinned_dropdown_opened = exists(close_tab_pattern)
        assert pinned_dropdown_opened, 'Right-click menu for pinned displayed'

        click(close_tab_pattern)

        new_tab()

        new_tab_opened = exists(Tabs.NEW_TAB_HIGHLIGHTED)
        assert new_tab_opened, 'New tab is opened, Firefox didn\'t crash.'

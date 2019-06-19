# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Firefox can be set to display the windows and tabs from last time on launch',
        test_case_id='143545',
        test_suite_id='2241',
        locale=['en-US'],
    )
    def run(self, firefox):
        restore_previous_session_checked_pattern = Pattern('restore_previous_session_checked.png')
        restore_previous_session_unchecked_pattern = Pattern('restore_previous_session_unchecked.png')

        navigate(LocalWeb.FIREFOX_TEST_SITE)

        firefox_site_loaded = exists(LocalWeb.FIREFOX_LOGO, Settings.site_load_timeout)
        assert firefox_site_loaded, 'Firefox local web page is loaded'

        new_tab()
        navigate(LocalWeb.FOCUS_TEST_SITE)

        focus_site_loaded = exists(LocalWeb.FOCUS_IMAGE, Settings.site_load_timeout)
        assert focus_site_loaded, 'Focus local web page is loaded'

        new_tab()
        navigate('about:preferences')

        general_tab_loaded = exists(restore_previous_session_unchecked_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert general_tab_loaded, 'The options for "General" section are displayed.'

        click(restore_previous_session_unchecked_pattern)

        restore_session_checked = exists(restore_previous_session_checked_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert restore_session_checked, 'The option "Restore previous session" from "Startup" is successfully selected.'

        firefox.restart()

        select_tab(1)

        firefox_site_loaded = exists(LocalWeb.FIREFOX_LOGO, Settings.site_load_timeout)

        select_tab(2)

        focus_site_loaded = exists(LocalWeb.FOCUS_IMAGE, Settings.site_load_timeout)

        select_tab(3)

        general_tab_loaded = exists(restore_previous_session_checked_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert general_tab_loaded and firefox_site_loaded and focus_site_loaded, \
            'The browser opens successfully and all the pages from the last session are loaded.'

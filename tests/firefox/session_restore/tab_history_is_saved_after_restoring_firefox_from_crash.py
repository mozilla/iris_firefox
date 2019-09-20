# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Tab History is saved after restoring Firefox from a crash',
        test_case_id='114828',
        test_suite_id='68',
        locales=Locales.ENGLISH,
        blocked_by={'id': 'issue_3222', 'platform': OSPlatform.ALL}
    )
    def run(self, firefox):
        restore_previous_session_checkbox_pattern = Pattern('restore_previous_session_checkbox.png')
        restart_firefox_button_pattern = Pattern('restart_firefox_button.png')

        if OSHelper.is_windows():
            crash_reporter_icon_pattern = Pattern('crash_reporter_icon.png')

        navigate('about:preferences#general')

        restore_previous_session_checkbox_displayed = exists(restore_previous_session_checkbox_pattern)
        assert restore_previous_session_checkbox_displayed, 'Restore previous session button displayed'

        click(restore_previous_session_checkbox_pattern)

        navigate(LocalWeb.MOZILLA_TEST_SITE)

        test_site_opened = exists(LocalWeb.MOZILLA_LOGO, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert test_site_opened, 'Mozilla test website is opened'

        navigate(LocalWeb.POCKET_TEST_SITE)

        test_site_opened = exists(LocalWeb.POCKET_LOGO, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert test_site_opened, 'Pocket test website is opened'

        navigate(LocalWeb.FOCUS_TEST_SITE)

        test_site_opened = exists(LocalWeb.FOCUS_LOGO, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert test_site_opened, 'Focus test website is opened'

        navigate(LocalWeb.FIREFOX_TEST_SITE)

        test_site_opened = exists(LocalWeb.FIREFOX_LOGO, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert test_site_opened, 'Firefox test website is opened'

        firefox.restart()

        navigate('about:crashparent')

        if OSHelper.is_windows():
            crash_reporter_icon_exists = exists(crash_reporter_icon_pattern, FirefoxSettings.HEAVY_SITE_LOAD_TIMEOUT)
            assert crash_reporter_icon_exists, 'Crash Reporter icon exists'

            click(crash_reporter_icon_pattern)

        firefox_crashed = exists(restart_firefox_button_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert firefox_crashed, 'Firefox crashed.'

        click(restart_firefox_button_pattern)

        firefox_is_restarted = exists(NavBar.HOME_BUTTON, FirefoxSettings.HEAVY_SITE_LOAD_TIMEOUT)
        assert firefox_is_restarted, 'Firefox is successfully restarted'

        previous_tab()

        test_site_opened = exists(LocalWeb.FIREFOX_LOGO, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert test_site_opened, 'Firefox test website is restored'

        navigate_back()

        test_site_opened = exists(LocalWeb.FOCUS_LOGO, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert test_site_opened, 'Focus test website history was successfully remembered.'

        navigate_back()

        test_site_opened = exists(LocalWeb.POCKET_LOGO, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert test_site_opened, 'Pocket test website history was successfully remembered.'

        navigate_back()

        test_site_opened = exists(LocalWeb.MOZILLA_LOGO, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert test_site_opened, 'Mozilla test website history was successfully remembered. The tab history was ' \
                                 'successfully remembered.'

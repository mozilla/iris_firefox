# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='No sections selected in Clear Recent History window.',
        locale=['en-US'],
        test_case_id='172046',
        test_suite_id='2000'
    )
    def run(self, firefox):
        checked_box = Utils.CHECKEDBOX
        clear_now_button_disabled = History.CLearRecentHistory.DISABLED_CLEAR_NOW

        # Open some pages to create some history.
        new_tab()
        navigate(LocalWeb.MOZILLA_TEST_SITE)

        mozilla_logo_exists = exists(LocalWeb.MOZILLA_LOGO, FirefoxSettings.FIREFOX_TIMEOUT)
        assert mozilla_logo_exists, 'Mozilla page loaded successfully.'

        new_tab()
        navigate(LocalWeb.FIREFOX_TEST_SITE)

        firefox_logo_exists = exists(LocalWeb.FIREFOX_LOGO, FirefoxSettings.FIREFOX_TIMEOUT)
        assert firefox_logo_exists, 'Firefox page loaded successfully.'

        # Open the History sidebar.
        history_sidebar()

        # Open the 'Clear Recent History' window and uncheck all the items.
        for step in open_clear_recent_history_window():
            assert step.resolution, step.message

        # Uncheck all options to be cleared.
        for step in range(1, 6):
            checked_box_exists = exists(checked_box, FirefoxSettings.TINY_FIREFOX_TIMEOUT)
            if checked_box_exists:
                assert checked_box_exists, 'Checked box number {} exist'.format(step)

                time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT/2)
                click(checked_box)
            else:
                break

        # Check that the 'Clear Now' button is disabled.
        clear_now_button_disabled_exists = exists(clear_now_button_disabled.similar(0.8),
                                                  FirefoxSettings.FIREFOX_TIMEOUT)
        assert clear_now_button_disabled_exists, 'Clear Now button is disabled.'

        # Close the 'Clear Recent History' window.
        type(Key.ESC)

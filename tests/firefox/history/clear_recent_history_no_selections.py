# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='No sections selected in Clear Recent History window.',
        locale='[en-US]',
        test_case_id='172046',
        test_suite_id='2000'
    )
    def run(self, firefox):
        checked_box = Utils.CHECKEDBOX
        clear_now_button_disabled = History.CLearRecentHistory.DISABLED_CLEAR_NOW

        # Open some pages to create some history.
        new_tab()
        navigate(LocalWeb.MOZILLA_TEST_SITE)
        expected_1 = exists(LocalWeb.MOZILLA_LOGO, 10)
        assert  expected_1, 'Mozilla page loaded successfully.'

        new_tab()
        navigate(LocalWeb.FIREFOX_TEST_SITE)
        expected_2 = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert  expected_2, 'Firefox page loaded successfully.'

        # Open the History sidebar.
        history_sidebar()

        # Open the 'Clear Recent History' window and uncheck all the items.
        for step in open_clear_recent_history_window():
            assert  step.resolution, step.message

        region = Region(Screen().width / 4, Screen().height / 4, Screen().width / 2, Screen().height / 2)

        # Uncheck all options to be cleared.
        while region.exists(checked_box.similar(0.9), 10):
            time.sleep(Settings.DEFAULT_UI_DELAY)
            click(checked_box)
            region.exists(checked_box.similar(0.9), 10)

        # Check that the 'Clear Now' button is disabled.
        expected_4 = exists(clear_now_button_disabled.similar(0.8), 10)
        assert expected_4, 'Clear Now button is disabled.'

        # Close the 'Clear Recent History' window.
        type(Key.ESC)

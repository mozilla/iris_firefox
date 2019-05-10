# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Check that the \'Clear Recent History\' window is displayed properly.',
        locale=['en-US'],
        test_case_id='172043',
        test_suite_id='2000',
        profile=Profiles.BRAND_NEW
    )
    def run(self, firefox):
        clear_recent_history_window_pattern = History.CLearRecentHistory.CLEAR_RECENT_HISTORY_TITLE

        # Check that the Clear Recent History window is displayed properly.
        clear_recent_history()
        expected = exists(clear_recent_history_window_pattern, 10)
        assert expected, 'Clear Recent History window was displayed properly.'
        type(Key.ESC)

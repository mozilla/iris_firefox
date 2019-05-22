# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Dismiss the \'Clear Recent History\' window.',
        locale=['en-US'],
        test_case_id='172048',
        test_suite_id='2000',
        profile=Profiles.BRAND_NEW
    )
    def run(self, firefox):
        clear_recent_history_window_pattern = History.CLearRecentHistory.CLEAR_RECENT_HISTORY_TITLE
        dismiss_clear_recent_history_window_button_pattern = History.CLearRecentHistory.CANCEL

        # Open the 'Clear Recent History' window and uncheck all the items.
        for step in open_clear_recent_history_window():
            assert step.resolution, step.message

        # Dismiss the Clear recent window
        try:
            wait(dismiss_clear_recent_history_window_button_pattern, 10)
            logger.debug('Clear Recent History button found.')
            click(dismiss_clear_recent_history_window_button_pattern)
        except FindError:
            raise FindError('Clear Recent History button NOT found, aborting.')

        # Check that the Clear Recent History window was dismissed properly.
        try:
            expected = wait_vanish(clear_recent_history_window_pattern.similar(0.9), 10)
            assert expected is True, 'Clear Recent History window was dismissed properly.'
        except FindError:
            raise FindError('Clear Recent History window was NOT dismissed properly.')

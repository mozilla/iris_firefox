# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Bug 1285328 - Hitting Escape or the X on the "Restart Firefox" dialog when enabling "Never '
                    'remember history" is treated as a confirmation',
        test_case_id='145294',
        test_suite_id='2241',
        locale=['en-US'],
    )
    def run(self, firefox):
        history_dropdown_pattern = Pattern('history_dropdown_button.png')
        never_remember_history_pattern = Pattern('never_remember_history.png')
        restart_browser_pattern = Pattern('restart_browser.png')

        navigate('about:preferences#privacy')

        paste('firefox will remember')

        history_dropdown = exists(history_dropdown_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert history_dropdown, 'History dropdown list can be accessed.'

        click(history_dropdown_pattern)

        never_remember_history = exists(never_remember_history_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert never_remember_history, 'Never Remember History option is present in the dropdown list.'

        click(never_remember_history_pattern)

        restart_browser_popup_assert = exists(restart_browser_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert restart_browser_popup_assert is True, 'History option can be changed.'

        type(Key.ESC)

        try:
            restart_browser_dismissed = wait_vanish(restart_browser_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
            assert restart_browser_dismissed, 'Restart browser popup was dismissed.'

        except FindError:
            raise FindError('Browser restart popup was not closed.')

        try:
            never_remember_history_not_saved = wait_vanish(never_remember_history_pattern,
                                                           FirefoxSettings.FIREFOX_TIMEOUT)
            assert never_remember_history_not_saved, 'Never Remember History option was not saved.'

        except FindError:
            raise FindError('Never Remember History option was changed')

        firefox_not_restarted = exists(AboutPreferences.PRIVACY_AND_SECURITY_BUTTON_NOT_SELECTED,
                                       FirefoxSettings.FIREFOX_TIMEOUT)

        assert restart_browser_dismissed and firefox_not_restarted and never_remember_history_not_saved, \
            'Restart browser popup was dismissed. Never Remember History option was not saved. ' \
            'Firefox was not restarted. NOTE: On the builds affected by this bug Firefox restarted after Esc was ' \
            'pressed and all the history was deleted. '

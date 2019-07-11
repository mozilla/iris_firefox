# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Firefox can be set to no longer accept third-party cookies.',
        locale=['en-US'],
        test_case_id='106156',
        test_suite_id='1826',
    )
    def run(self, firefox):
        clear_data_button_pattern = Pattern('clear_button.png')
        confirm_clear_data_pattern = Pattern('confirm_clear_data.png')
        open_clear_data_window_pattern = Pattern('open_clear_data_window.png')
        zero_bytes_cache_pattern = Pattern('zero_bytes_cache.png')

        navigate('about:preferences#privacy')
        preferences_opened = exists(AboutPreferences.PRIVACY_AND_SECURITY_BUTTON_SELECTED)
        assert preferences_opened, 'Preferences page is opened'

        paste('clear data')
        clear_data_button_selected = exists(open_clear_data_window_pattern)
        assert clear_data_button_selected, '"Clear data" button is selected'

        click(open_clear_data_window_pattern)

        clear_data_window_opened = exists(clear_data_button_pattern.similar(0.9))
        assert clear_data_window_opened, 'Subwindow is opened'

        click(clear_data_button_pattern)

        clear_message_appeared = exists(confirm_clear_data_pattern)
        assert clear_message_appeared, '"Clear cookies data" message window is opened'

        click(confirm_clear_data_pattern)

        data_cleared = exists(zero_bytes_cache_pattern)
        assert data_cleared, 'Data was cleared'

        click(zero_bytes_cache_pattern)




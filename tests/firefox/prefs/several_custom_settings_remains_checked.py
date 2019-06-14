# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Bug 1524995 - Several custom settings for browser history remains checked and grayed out after '
                    'selecting the “Always use private browsing mode” option',
        test_case_id='249028',
        test_suite_id='2241',
        locale=['en-US'],
    )
    def run(self, firefox):
        custom_history_settings_pattern = Pattern('custom_history_settings.png')

        if OSHelper.is_windows():
            value = Screen.SCREEN_HEIGHT/2
        elif OSHelper.is_linux():
            value = 5
        else:
            value = 100

        navigate('about:preferences#privacy')

        page_loaded = exists(AboutPreferences.PRIVACY_AND_SECURITY_BUTTON_SELECTED, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert page_loaded, 'about:preferences#privacy page loaded'

        click(AboutPreferences.PRIVACY_AND_SECURITY_BUTTON_NOT_SELECTED)

        privacy_selected = exists(AboutPreferences.PRIVACY_AND_SECURITY_BUTTON_SELECTED,
                                  FirefoxSettings.TINY_FIREFOX_TIMEOUT)
        assert privacy_selected, 'The about:preferences page is successfully loaded. The options' \
                                 ' for "Privacy & Security" section are displayed.'

        remember_history = scroll_until_pattern_found(remember_history_pattern, Mouse().scroll, (0, -value), 100)
        assert remember_history, '"Remember history" option from the History dropdown list found.'

        click(remember_history_pattern)

        use_custom_settings_for_history = exists(use_custom_settings_for_history_pattern)
        assert use_custom_settings_for_history, 'The option "Use custom settings for history" found.'

        click(use_custom_settings_for_history_pattern)

        always_use_private_browsing_unticked = exists(always_use_private_browsing_mode_unticked_pattern)
        assert always_use_private_browsing_unticked, '"Always use private browsing mode" checkbox.'

        click(always_use_private_browsing_mode_unticked_pattern)






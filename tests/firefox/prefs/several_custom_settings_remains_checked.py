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
        use_custom_settings_for_history_pattern = Pattern('custom_history_settings.png')
        remember_history_pattern = Pattern('remember_history.png')
        restart_browser_pattern = Pattern('restart_browser.png')
        always_use_private_browsing_mode_unticked_pattern = Pattern('always_use_private_browsing_mode_unticked.png')
        remember_browsing_search_clear_history_unticked_pattern = \
            Pattern('remember_browsing_search_clear_history_unticked.png')

        if OSHelper.is_windows():
            scroll_length = Screen.SCREEN_HEIGHT // 2
        elif OSHelper.is_linux():
            scroll_length = 5
        else:
            scroll_length = 100

        navigate('about:preferences#privacy')

        page_loaded = exists(AboutPreferences.PRIVACY_AND_SECURITY_BUTTON_SELECTED, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert page_loaded, 'about:preferences#privacy page loaded'

        click(AboutPreferences.PRIVACY_AND_SECURITY_BUTTON_NOT_SELECTED)

        privacy_selected = exists(AboutPreferences.PRIVACY_AND_SECURITY_BUTTON_SELECTED,
                                  FirefoxSettings.TINY_FIREFOX_TIMEOUT)
        assert privacy_selected, 'The about:preferences page is successfully loaded. The options' \
                                 ' for "Privacy & Security" section are displayed.'

        center_screen_location = Location(Screen.SCREEN_WIDTH // 2, Screen.SCREEN_HEIGHT // 2)
        move(center_screen_location)

        remember_history = scroll_until_pattern_found(remember_history_pattern, Mouse().scroll,
                                                      (0, -scroll_length), 100)

        assert remember_history, '"Remember history" option from the History dropdown list found.'

        click(remember_history_pattern)

        use_custom_settings_for_history = exists(use_custom_settings_for_history_pattern)
        assert use_custom_settings_for_history, 'The option "Use custom settings for history" found.'

        click(use_custom_settings_for_history_pattern)

        always_use_private_browsing_unticked = exists(always_use_private_browsing_mode_unticked_pattern)
        assert always_use_private_browsing_unticked, '"Always use private browsing mode" checkbox.'

        click(always_use_private_browsing_mode_unticked_pattern)

        restart_browser = exists(restart_browser_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert restart_browser, 'Restart browser button available'

        click(restart_browser_pattern)

        firefox_restarted = exists(Tabs.NEW_TAB_HIGHLIGHTED, FirefoxSettings.HEAVY_SITE_LOAD_TIMEOUT)
        assert firefox_restarted, 'Firefox is successfully restarted.'

        navigate('about:preferences#privacy')

        privacy_selected = exists(AboutPreferences.PRIVACY_AND_SECURITY_BUTTON_SELECTED,
                                  FirefoxSettings.TINY_FIREFOX_TIMEOUT)
        assert privacy_selected, 'The about:preferences page is successfully loaded.'

        move(center_screen_location)

        remember_browsing_search_clear_history_unticked = scroll_until_pattern_found(
            remember_browsing_search_clear_history_unticked_pattern, Mouse().scroll, (0, -scroll_length), 100)

        assert remember_browsing_search_clear_history_unticked, \
            '"Use custom settings for history" option from the History dropdown list found.' \
            '\nNOTE: In the affected builds, the following options are ticked and grayed out: ' \
            '\n"Remember browsing and download history" ' \
            '\n"Remember search and form history"' \
            '\nTo see the behaviour click here. [https://bug1524995.bmoattachments.org/attachment.cgi?id=9041165]'

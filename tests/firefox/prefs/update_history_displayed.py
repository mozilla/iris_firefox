# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Update History list is successfully displayed ',
        test_case_id='143571',
        test_suite_id='2241',
        locale=['en-US'],
    )
    def run(self, firefox):
        show_update_history_button_pattern = Pattern('show_update_history_button.png')
        update_history_popup_title_pattern = Pattern('update_history_popup_title.png')

        if OSHelper.is_windows():
            scroll_height = Screen.SCREEN_HEIGHT * 2
        elif OSHelper.is_linux() or OSHelper.is_mac():
            scroll_height = Screen.SCREEN_HEIGHT // 100

        navigate('about:preferences')

        page_loaded = exists(AboutPreferences.PRIVACY_AND_SECURITY_BUTTON_NOT_SELECTED)
        assert page_loaded, 'about:preferences page loaded.'

        screen_center_location = Location(Screen.SCREEN_WIDTH // 2, Screen.SCREEN_HEIGHT // 2)

        hover(screen_center_location)

        choose_language_button = scroll_until_pattern_found(show_update_history_button_pattern, Mouse().scroll,
                                                            (None, -scroll_height), 140, 1)
        assert choose_language_button, 'Choose language button found.'

        click(show_update_history_button_pattern, 1)

        update_history_popup_title = exists(update_history_popup_title_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert update_history_popup_title, 'The "Update History" subdialog appears.'

        message_region = Region(0, int(Screen.SCREEN_HEIGHT/3), Screen.SCREEN_WIDTH, int(Screen.SCREEN_HEIGHT/3))

        no_updates_installed = exists('No updates installed yet', region=message_region)
        assert no_updates_installed, '"No updates installed yet" displayed. A list with updates that were installed ' \
                                     'is correctly displayed.'

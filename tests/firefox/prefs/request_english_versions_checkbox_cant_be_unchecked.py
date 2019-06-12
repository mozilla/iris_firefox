# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Bug 1435786 - "Request English versions…" checkbox in Preferences can\'t be unchecked '
                    'after being checked',
        locales=['en-US'],
        test_case_id='145063',
        test_suite_id='2241',
    )
    def run(self, firefox):
        choose_button_pattern = Pattern('choose_button.png')
        request_english_checked_pattern = Pattern('request_english_checked.png')
        request_english_unchecked_pattern = Pattern('request_english_unchecked.png')

        if OSHelper.is_windows():
            screen_height = Screen.SCREEN_HEIGHT
        elif OSHelper.is_mac():
            screen_height = 100
        else:
            screen_height = 10

        change_preference('privacy.resistFingerprinting', 'true')

        navigate('about:preferences')

        screen_center = Location(Screen.SCREEN_WIDTH // 2, Screen.SCREEN_HEIGHT // 2)
        move(screen_center)

        language_choose_button_pattern = \
            scroll_until_pattern_found(choose_button_pattern, Mouse().scroll, (0, -screen_height), 20,
                                       FirefoxSettings.TINY_FIREFOX_TIMEOUT)
        assert language_choose_button_pattern, '"Choose…" button, under the Language heading is available.'

        click(choose_button_pattern)

        request_english_unchecked = exists(request_english_unchecked_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert request_english_unchecked, 'The Language pop-up is displayed. The field "Request English versions…" ' \
                                          'is unchecked. '
        click(request_english_unchecked_pattern, 1)

        request_english_checked = exists(request_english_checked_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert request_english_checked, 'The field "Request English versions…" is checked successfully.'

        click(request_english_checked_pattern, 1)

        request_english_unchecked = exists(request_english_unchecked_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert request_english_unchecked, 'The field "Request English versions…" is unchecked successfully.'

        type(Key.ENTER)

        try:
            assert wait_vanish(request_english_unchecked_pattern, FirefoxSettings.TINY_FIREFOX_TIMEOUT)
        except FindError:
            raise FindError('Pop-up is still open.')

        click(choose_button_pattern, 1)

        request_english_unchecked = exists(request_english_unchecked_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert request_english_unchecked, 'The Language pop-up is displayed again. The field "Request English ' \
                                          'versions…" is unchecked. NOTE: The build affected by this bug the field ' \
                                          'remained checked. '

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Bug 1435786 - "Request English versions…" checkbox in Preferences can\'t be unchecked '
                    'after being checked',
        locale=['en-US'],
        test_case_id='145063',
        test_suite_id='2241',
    )
    def run(self, firefox):
        choose_language_button_pattern = Pattern('choose_button.png')
        webpage_language_settings_title_pattern = Pattern('webpage_language_settings_title.png')
        request_english_versions_unchecked_pattern = Pattern('request_english_versions_unchecked.png')

        change_preference('privacy.resistFingerprinting', 'true')

        navigate('about:preferences')

        type(Key.TAB)

        choose_language_button = scroll_until_pattern_found(choose_language_button_pattern, type, (Key.DOWN,), 20,
                                                            timeout=FirefoxSettings.TINY_FIREFOX_TIMEOUT//2)
        assert choose_language_button, 'Choose language button found.'

        click(choose_language_button_pattern)

        webpage_language_settings_title = exists(webpage_language_settings_title_pattern,
                                                 FirefoxSettings.FIREFOX_TIMEOUT)
        assert webpage_language_settings_title, 'Webpage language settings popup loaded.'

        # Check the 'Request English versions…' checkbox, then uncheck it, then click 'OK'.

        request_english_version_unchecked = exists(request_english_versions_unchecked_pattern.similar(.6),
                                                   FirefoxSettings.FIREFOX_TIMEOUT)
        assert request_english_version_unchecked, '"Request English versions..." found.'

        request_checkbox_unchecked = find_in_region_from_pattern(request_english_versions_unchecked_pattern.similar(.6),
                                                                 AboutPreferences.UNCHECKED_BOX.similar(.7),
                                                                 FirefoxSettings.FIREFOX_TIMEOUT)

        assert request_checkbox_unchecked, '"Request English versions..." is unchecked.'

        click(request_english_versions_unchecked_pattern, 1)

        request_checkbox_checked = find_in_region_from_pattern(request_english_versions_unchecked_pattern.similar(.6),
                                                               AboutPreferences.CHECKED_BOX.similar(.7),
                                                               FirefoxSettings.FIREFOX_TIMEOUT)

        assert request_checkbox_checked, '"Request English versions..." checked.'

        click(request_english_versions_unchecked_pattern, 1)

        restore_firefox_focus()

        request_version_unchecked = find_in_region_from_pattern(request_english_versions_unchecked_pattern.similar(0.7),
                                                                AboutPreferences.UNCHECKED_BOX.similar(.7),
                                                                FirefoxSettings.FIREFOX_TIMEOUT)
        assert request_version_unchecked, '"Request English versions..." unchecked.'

        type(Key.ENTER)

        # Click the languages 'Choose…' button again and notice the 'Request English versions…' checkbox.
        click(choose_language_button_pattern)
        
        webpage_language_settings_title = exists(webpage_language_settings_title_pattern,
                                                 FirefoxSettings.FIREFOX_TIMEOUT)
        assert webpage_language_settings_title, 'Webpage language settings popup displayed .'

        request_version_unchecked = find_in_region_from_pattern(request_english_versions_unchecked_pattern,
                                                                AboutPreferences.UNCHECKED_BOX,
                                                                FirefoxSettings.FIREFOX_TIMEOUT)
        assert request_version_unchecked, '"Request English versions..." unchecked. NOTE: The build affected ' \
                                          'by this bug the field remained checked. '

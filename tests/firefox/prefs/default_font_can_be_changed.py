# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='The default font can be successfully changed',
        test_case_id='143553',
        test_suite_id='2241',
        locale=['en-US']
    )
    def run(self, firefox):
        about_preferences_general_url_pattern = Pattern('about_preferences_general_url.png')
        preferences_general_option_pattern = Pattern('preferences_general_option.png')
        default_font_picker_pattern = Pattern('default_font_picker.png')
        page_with_mod_font_pattern = Pattern('modified_text_font.png')
        advanced_button_pattern = Pattern('advanced_button.png')
        proportional_dropdown_pattern = Pattern('proportional_dropdown.png').similar(0.6)

        new_tab()
        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)

        previous_tab()
        navigate('about:preferences#general')

        about_preferences_general_url_exists = exists(about_preferences_general_url_pattern,
                                                      FirefoxSettings.FIREFOX_TIMEOUT)
        assert about_preferences_general_url_exists, 'The about:preferences page is successfully loaded'

        preferences_general_option_exists = exists(preferences_general_option_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert preferences_general_option_exists, 'The options for "General" section are displayed'

        advanced_button_exists = exists(advanced_button_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert advanced_button_exists, 'Advanced settings is present'

        click(advanced_button_pattern)

        proportional_dropdown_exists = exists(proportional_dropdown_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert proportional_dropdown_exists, 'Proportional drop is available'

        if OSHelper.is_mac():
            click(proportional_dropdown_pattern)
        else:
            type(Key.TAB)

        type(Key.DOWN)
        type(Key.ENTER)
        type(Key.ENTER)

        default_font_picker_exists = exists(default_font_picker_pattern.similar(0.6), FirefoxSettings.FIREFOX_TIMEOUT)
        assert default_font_picker_exists, 'Font picker is displayed'

        click(default_font_picker_pattern)

        [type(Key.DOWN) for _ in range(5)]
        type(Key.ENTER)

        next_tab()

        font_is_changed_to_another = exists(page_with_mod_font_pattern, FirefoxSettings.FIREFOX_TIMEOUT)

        assert font_is_changed_to_another, 'Font is successfully changed.'

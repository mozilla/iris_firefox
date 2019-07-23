# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='The default fonts can be successfully customized',
        test_case_id='143558',
        test_suite_id='2241',
        locale=['en-US']
    )
    def run(self, firefox):
        about_preferences_general_url_pattern = Pattern('about_preferences_general_url.png')
        preferences_general_option_pattern = Pattern('preferences_general_option.png')
        advanced_button_pattern = Pattern('advanced_button.png')
        proportional_dropdown_pattern = Pattern('proportional_dropdown.png')
        proportional_font_size_pattern = Pattern('proportional_font_size.png')
        font_sans_serif_drop_pattern = Pattern('font_sans_serif_drop.png')
        page_with_mod_font_size_pattern = Pattern('page_with_mod_font_size.png')

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
            [type(Key.DOWN) for _ in range(2)]
        else:
            type(Key.TAB)
            type(Key.DOWN)
        type(Key.ENTER)

        font_sans_serif_drop_exists = exists(font_sans_serif_drop_pattern)
        assert font_sans_serif_drop_exists, 'Sans serif font can be changed'

        click(font_sans_serif_drop_pattern)
        if OSHelper.is_mac():
            type(Key.DOWN)  # open drop-down

        [type(Key.DOWN) for _ in range(5)]  # choose different font

        if OSHelper.is_mac():
            type(Key.ENTER)  # select size in drop-down

        proportional_font_size_exists = exists(proportional_font_size_pattern)
        assert proportional_font_size_exists, 'Size can be chosen.'

        click(proportional_font_size_pattern)

        [type(Key.DOWN) for _ in range(5)]  # choose different size

        if OSHelper.is_mac():
            type(Key.ENTER)  # select size in drop-down

        type(Key.ENTER)

        next_tab()

        font_is_changed_to_another = exists(page_with_mod_font_size_pattern, FirefoxSettings.FIREFOX_TIMEOUT)

        assert font_is_changed_to_another, 'Font is successfully changed.'

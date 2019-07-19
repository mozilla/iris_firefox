# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='The default size can be successfully changed',
        test_case_id='143554',
        test_suite_id='2241',
        locale=['en-US']
    )
    def run(self, firefox):
        about_preferences_general_url_pattern = Pattern('about_preferences_general_url.png')
        preferences_general_option_pattern = Pattern('preferences_general_option.png')
        default_text_size_pattern = Pattern('default_text_size.png').similar(0.6)
        modified_text_size_pattern = Pattern('modified_text_size.png')

        new_tab()
        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)

        previous_tab()
        navigate('about:preferences#general')

        about_preferences_general_url_exists = exists(about_preferences_general_url_pattern,
                                                      FirefoxSettings.FIREFOX_TIMEOUT)
        assert about_preferences_general_url_exists, 'The about:preferences page is successfully loaded'

        preferences_general_option_exists = exists(preferences_general_option_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert preferences_general_option_exists, 'The options for "General" section are displayed'

        click(AboutPreferences.FIND_IN_OPTIONS)
        type('size')

        default_text_size_exists = exists(default_text_size_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert default_text_size_exists, 'Default size can be changed'

        click(default_text_size_pattern)
        [type(Key.DOWN) for _ in range(5)]
        type(Key.ENTER)

        next_tab()

        text_size_is_modified = exists(modified_text_size_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert text_size_is_modified, 'The size of the text is successfully changed'

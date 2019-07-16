# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='The CTRL + TAB shortcut can be set to cycle through tabs in recently used order',
        test_case_id='143549',
        test_suite_id='2241',
        locale=['en-US']
    )
    def run(self, firefox):
        about_preferences_general_url_pattern = Pattern('about_preferences_general_url.png')
        preferences_general_option_pattern = Pattern('preferences_general_option.png')
        default_font_picker_pattern = Pattern('default_font_picker.png')
        ff_page_with_arial_font_pattern = Pattern('ff_text_arial_font.png')

        new_tab()
        navigate(LocalWeb.FIREFOX_TEST_SITE)

        ff_site_opened = exists(LocalWeb.FIREFOX_LOGO)
        assert ff_site_opened, 'Test site is successfully opened'

        previous_tab()
        navigate('about:preferences#general')

        about_preferences_general_url_exists = exists(about_preferences_general_url_pattern,
                                                      FirefoxSettings.FIREFOX_TIMEOUT)
        assert about_preferences_general_url_exists, 'The about:preferences page is successfully loaded'

        preferences_general_option_exists = exists(preferences_general_option_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert preferences_general_option_exists, 'The options for "General" section are displayed'

        default_font_picker_exists = exists(default_font_picker_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert default_font_picker_exists, 'Font picker is displayed'

        click(default_font_picker_pattern)

        [type(Key.DOWN) for _ in range(13)]
        type(Key.ENTER)

        next_tab()

        font_is_changed_to_another = exists(ff_page_with_arial_font_pattern, FirefoxSettings.FIREFOX_TIMEOUT)

        assert font_is_changed_to_another, 'Font is successfully changed!'

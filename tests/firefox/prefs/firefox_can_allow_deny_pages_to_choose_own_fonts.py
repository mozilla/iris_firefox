# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Firefox can Allow/Deny pages to choose their own fonts',
        test_case_id='143559',
        test_suite_id='2241',
        locale=['en-US'],
    )
    def run(self, firefox):
        preferences_general_option_pattern = Pattern('preferences_general_option.png')
        font_of_site_pattern = Pattern('font_of_site.png')
        font_of_site_changed_pattern = Pattern('font_of_site_changed.png')
        advanced_button_pattern = Pattern('advanced_button.png')
        fonts_subdialog_label_pattern = Pattern('fonts_subdialog_label.png')

        location = Location(Screen.SCREEN_WIDTH/2, Screen.SCREEN_HEIGHT/2)

        if OSHelper.is_windows():
            value = Screen.SCREEN_HEIGHT
        elif OSHelper.is_linux():
            value = Screen.SCREEN_HEIGHT/200
        else:
            value = Screen.SCREEN_HEIGHT/10

        navigate('http://www.psimadethis.com/')

        move(location)

        font_of_site_exists = scroll_until_pattern_found(font_of_site_pattern, Mouse().scroll,
                                                         (0, -value), 20,
                                                         FirefoxSettings.TINY_FIREFOX_TIMEOUT/2)
        assert font_of_site_exists, 'Local font is found'

        new_tab()

        select_tab(1)

        close_tab()

        navigate('about:preferences#general')

        preferences_general_option_exists = exists(preferences_general_option_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert preferences_general_option_exists, 'The about:preferences page is successfully loaded'

        type('Fonts and Colors', interval=0.2)

        advanced_button_exists = exists(advanced_button_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert advanced_button_exists, 'Advanced button exists'

        click(advanced_button_pattern)

        fonts_subdialog_label_exists = exists(fonts_subdialog_label_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert fonts_subdialog_label_exists, 'The "Fonts" subdialog is displayed'

        if OSHelper.is_windows() or OSHelper.is_linux():
            [type(Key.TAB) for _ in range(2)]

            [type(Key.DOWN) for _ in range(6)]

        pages_have_own_fonts_checked_exists = exists(AboutPreferences.CHECKED_BOX, FirefoxSettings.FIREFOX_TIMEOUT)
        assert pages_have_own_fonts_checked_exists, ' "Allow pages to choose their own fonts,' \
                                                    ' instead of your selections above" checked exists'

        click(AboutPreferences.CHECKED_BOX)

        pages_have_own_fonts_unchecked_exists = exists(AboutPreferences.UNCHECKED_BOX, FirefoxSettings.FIREFOX_TIMEOUT)
        assert pages_have_own_fonts_unchecked_exists, ' "Allow pages to choose their own fonts,' \
                                                      ' instead of your selections above" unchecked exists'

        type(Key.ENTER)

        try:
            fonts_subdialog_label_exists = wait_vanish(fonts_subdialog_label_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
            assert fonts_subdialog_label_exists, 'The "Fonts" subdialog is vanished'
        except FindError:
            raise FindError('The "Fonts" subdialog still exists')

        navigate('http://www.psimadethis.com/')

        font_of_site_changed_exists = scroll_until_pattern_found(font_of_site_changed_pattern, Mouse().scroll,
                                                                 (0, -value), 20,
                                                                 FirefoxSettings.TINY_FIREFOX_TIMEOUT/2)
        assert font_of_site_changed_exists, 'All the changes made can be seen'

        font_of_site_exists = exists(font_of_site_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert font_of_site_exists is False, 'Previous fonts is not available'

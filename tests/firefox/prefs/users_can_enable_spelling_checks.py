# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Users can enable/disable language spelling checks',
        test_case_id='143564',
        test_suite_id='2241',
        locale=['en-US'],
    )
    def run(self, firefox):
        text_editor_title_pattern = Pattern('text_editor_title.png')
        check_your_spelling_unchecked_pattern = Pattern('check_your_spelling_unchecked.png')
        check_your_spelling_checked_pattern = Pattern('check_your_spelling_unchecked.png')
        word_underlined_red_pattern = Pattern('word_underlined_red.png')
        text_editor_page = self.get_asset_path('editor.html')

        if OSHelper.is_windows():
            scroll_height = Screen.SCREEN_HEIGHT*2
        elif OSHelper.is_linux() or OSHelper.is_mac():
            scroll_height = Screen.SCREEN_HEIGHT//100

        navigate('about:preferences#general')

        page_loaded = exists(AboutPreferences.PRIVACY_AND_SECURITY_BUTTON_NOT_SELECTED,
                             FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert page_loaded, 'about:preferences page loaded'

        navigate(text_editor_page)

        text_editor_loaded = exists(text_editor_title_pattern)
        assert text_editor_loaded, 'Text editor page loaded.'

        screen_center_location = Location(Screen.SCREEN_WIDTH//2, Screen.SCREEN_HEIGHT//2)

        click(screen_center_location)

        # The word that was spelled wrong is underlined with a red squiggly line.

        paste('test   ttteeesssttt ')

        wrong_spelled_word_underlined_red = exists(word_underlined_red_pattern)
        assert wrong_spelled_word_underlined_red, 'The word that was spelled wrong is underlined with a red ' \
                                                  'squiggly line.'

        # From "Language and Appearance", underneath the "Language", uncheck the box "Check your spelling as you type".

        new_tab()

        navigate('about:preferences#general')

        page_loaded = exists(AboutPreferences.PRIVACY_AND_SECURITY_BUTTON_NOT_SELECTED)
        assert page_loaded, 'about:preferences#general page loaded.'

        screen_center_location = Location(Screen.SCREEN_WIDTH // 2, Screen.SCREEN_HEIGHT // 2)

        hover(screen_center_location)

        check_your_spelling = scroll_until_pattern_found(check_your_spelling_checked_pattern, Mouse().scroll,
                                                         (None, -scroll_height), 40,
                                                         FirefoxSettings.TINY_FIREFOX_TIMEOUT/2)
        assert check_your_spelling, '"Check you spelling..." option found.'

        click(check_your_spelling_checked_pattern)

        check_your_spelling_unchecked = find_in_region_from_pattern(check_your_spelling_unchecked_pattern,
                                                                    AboutPreferences.UNCHECKED_BOX)
        assert check_your_spelling_unchecked, '"Check you spelling..." is unchecked.'

        new_tab()

        navigate(text_editor_page)

        text_editor_loaded = exists(text_editor_title_pattern)
        assert text_editor_loaded, 'Text editor page loaded.'

        click(screen_center_location)

        paste('test   ttteeesssttt ')

        wrong_spelled_word_underlined_red = exists(word_underlined_red_pattern, FirefoxSettings.TINY_FIREFOX_TIMEOUT)
        assert wrong_spelled_word_underlined_red is False, 'The word that was spelled wrong is underlined with a red ' \
                                                           'squiggly line.'

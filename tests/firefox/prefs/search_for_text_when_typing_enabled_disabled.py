# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='The \'Search for text when you start typing\' can be successfully enabled / disabled.',
        test_case_id='143586',
        test_suite_id='2241',
        locale=['en-US'],
    )
    def run(self, firefox):
        search_for_text_start_typing_checkbox_pattern = Pattern('search_for_text_start_typing_checkbox.png')
        general_prefs_section_pattern = Pattern('general_preferences_section.png')
        search_text_highlighted_pattern = Pattern('search_text_highlighted.png')
        quick_find_toolbar_pattern = Pattern('quick_find_toolbar.png')

        box_width, box_heigth = AboutPreferences.UNCHECKED_BOX.get_size()

        navigate('about:preferences#general')

        general_prefs_section_opened = exists(general_prefs_section_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert general_prefs_section_opened, '\'General\' section in \'Preferences\' successfully opened'

        paste('Search for')

        search_for_text_start_typing_checkbox_available = exists(search_for_text_start_typing_checkbox_pattern)
        assert search_for_text_start_typing_checkbox_available, \
            '\'Search for text when you start typing\' checkbox available in \'General\' preferences section'

        search_for_text_start_typing_location = find(search_for_text_start_typing_checkbox_pattern)

        search_start_typing_width, search_start_typing_height = search_for_text_start_typing_checkbox_pattern.get_size()
        search_for_text_start_typing_region = Region(search_for_text_start_typing_location.x - box_width * 2,
                                                     search_for_text_start_typing_location.y,
                                                     search_start_typing_width + box_width * 2,
                                                     search_start_typing_height)

        search_for_text_start_typing_unchecked = exists(AboutPreferences.UNCHECKED_BOX,
                                                        region=search_for_text_start_typing_region)
        assert search_for_text_start_typing_unchecked, \
            '\'Search for text when you start typing\' checkbox unchecked'

        click(AboutPreferences.UNCHECKED_BOX, region=search_for_text_start_typing_region)

        search_for_text_start_typing_checked = exists(AboutPreferences.CHECKED_BOX,
                                                      region=search_for_text_start_typing_region)
        assert search_for_text_start_typing_checked, \
            '\'Search for text when you start typing\' checkbox successfully checked'

        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)

        wiki_opened = exists(LocalWeb.SOAP_WIKI_SOAP_LABEL, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert wiki_opened, '\'Wiki\' page successfully opened'

        type('Log')
        type(' in')

        quick_find_toolbar_appears_while_typing = exists(quick_find_toolbar_pattern)
        assert quick_find_toolbar_appears_while_typing, \
            'The \'Quick find\' toolbar appears at the bottom of the page'

        search_is_done = exists(search_text_highlighted_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert search_is_done, 'Search via \'Quick find\' toolbar is done successfully'

        navigate('about:preferences#general')

        general_prefs_section_opened = exists(general_prefs_section_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert general_prefs_section_opened, '\'General\' section in \'Preferences\' successfully opened'

        paste('Search for')

        search_for_text_start_typing_checkbox_available = exists(search_for_text_start_typing_checkbox_pattern)
        assert search_for_text_start_typing_checkbox_available, \
            '\'Search for text when you start typing\' checkbox available in \'General\' preferences section'

        search_for_text_start_typing_location = find(search_for_text_start_typing_checkbox_pattern)

        search_start_typing_width, search_start_typing_height = search_for_text_start_typing_checkbox_pattern.get_size()
        search_for_text_start_typing_region = Region(search_for_text_start_typing_location.x - box_width * 2,
                                                     search_for_text_start_typing_location.y,
                                                     search_start_typing_width + box_width * 2,
                                                     search_start_typing_height)

        search_for_text_start_typing_checked = exists(AboutPreferences.CHECKED_BOX,
                                                      region=search_for_text_start_typing_region)
        assert search_for_text_start_typing_checked, \
            '\'Search for text when you start typing\' checkbox checked after reentering about:preferences#general'

        click(search_for_text_start_typing_checkbox_pattern)

        search_for_text_start_typing_unchecked = exists(AboutPreferences.UNCHECKED_BOX,
                                                        region=search_for_text_start_typing_region)
        assert search_for_text_start_typing_unchecked, \
            '\'Search for text when you start typing\' checkbox successfully unchecked'

        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)

        wiki_opened = exists(LocalWeb.SOAP_WIKI_SOAP_LABEL, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert wiki_opened, '\'Wiki\' page successfully opened'

        type('Log')
        type(' in')

        quick_find_toolbar_does_not_appear_while_typing = not exists(quick_find_toolbar_pattern,
                                                                     FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert quick_find_toolbar_does_not_appear_while_typing, \
            'The \'Quick find\' toolbar does not appear after unchecking \'Search for text when you start typing\''

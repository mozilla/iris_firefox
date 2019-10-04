# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Firefox can be set to display blank pages in new tabs',
        locale=['en-US'],
        test_case_id='161669',
        test_suite_id='2241'
    )
    def run(self, firefox):
        highlights_options_pattern = Pattern('highlights_option.png')
        home_page_highlights_pattern = Pattern('home_page_highlights.png')

        navigate('about:preferences#home')

        preferences_page_opened = exists(highlights_options_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert preferences_page_opened, 'The about:preferences page is successfully loaded.'

        highlights_option_location = find(highlights_options_pattern)
        highlights_option_width, highlights_option_height = highlights_options_pattern.get_size()
        highlights_option_region = Region(highlights_option_location.x - highlights_option_width,
                                          highlights_option_location.y,
                                          highlights_option_width * 2, highlights_option_height)

        highlights_option_selected = exists(AboutPreferences.CHECKED_BOX, FirefoxSettings.FIREFOX_TIMEOUT,
                                            highlights_option_region)
        assert highlights_option_selected, 'The option is selected by default.'

        navigate('about:home')

        google_logo_content_search_field = exists(home_page_highlights_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert google_logo_content_search_field is True, 'The Highlights section is displayed on the Homepage.'

        navigate('about:newtab')

        google_logo_content_search_field = exists(home_page_highlights_pattern,
                                                  FirefoxSettings.FIREFOX_TIMEOUT)
        assert google_logo_content_search_field is True, 'The Highlights section is displayed on the New Tab page.'

        navigate('about:preferences#home')

        preferences_page_opened = exists(highlights_options_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert preferences_page_opened, 'The about:preferences page is successfully loaded.'

        highlights_option_selected = exists(AboutPreferences.CHECKED_BOX, FirefoxSettings.FIREFOX_TIMEOUT,
                                            highlights_option_region)
        assert highlights_option_selected, 'The option is selected by default.'

        click(AboutPreferences.CHECKED_BOX, region=highlights_option_region)

        web_search_selected = exists(AboutPreferences.UNCHECKED_BOX, FirefoxSettings.FIREFOX_TIMEOUT,
                                     highlights_option_region)
        assert web_search_selected, 'The options is not selected anymore.'

        navigate('about:home')

        highlights_section_displayed = exists(highlights_options_pattern)
        assert highlights_section_displayed is False, 'The Highlights section is not displayed anymore on the ' \
                                                      'Home page.'

        navigate('about:newtab')

        highlights_section_displayed = exists(highlights_options_pattern)
        assert highlights_section_displayed is False, 'The Highlights section is not displayed anymore on the ' \
                                                      'New Tab page.'

        new_window()

        highlights_section_displayed = exists(highlights_options_pattern)
        assert highlights_section_displayed is False, 'The Highlights section is not displayed anymore on the ' \
                                                      'Home page.'

        new_private_window()

        private_window_opened = exists(PrivateWindow.private_window_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert private_window_opened, 'Private window opened'

        highlights_section_displayed = exists(highlights_options_pattern)
        assert highlights_section_displayed is False, 'The Highlights section is not displayed anymore on the New ' \
                                                      'Tab page.'

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='The default search provider can be changed.',
        locale=['en-US'],
        test_case_id='4265',
        test_suite_id='83',
    )
    def run(self, firefox):
        change_search_settings_pattern = Pattern('change_search_settings.png')
        about_preferences_search_page_pattern = Pattern('about_preferences_search_page.png').similar(0.7)
        default_search_engine_dropdown_pattern = Pattern('default_search_engine_dropdown.png')

        change_preference('browser.search.widget.inNavBar', True)

        select_search_bar()
        paste('testing')

        expected = exists(change_search_settings_pattern, 10)
        assert expected is True, 'The \'Change Search Settings\' button found in the page.'

        click(change_search_settings_pattern)

        expected = exists(about_preferences_search_page_pattern, 10)
        assert expected is True, 'The \'about:preferences#search\' page opened.'

        click(default_search_engine_dropdown_pattern)
        repeat_key_down(2)
        type(Key.ENTER)

        select_search_bar()
        type(Key.ENTER)
        time.sleep(Settings.DEFAULT_UI_DELAY_LONG)

        select_location_bar()
        url_text = copy_to_clipboard()

        assert 'https://www.amazon.com/' in url_text, 'Search results are displayed for the newly set default search ' \
                                                      'provider.'

        assert 'testing' in url_text, 'Search results are displayed for that search term.'

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Awesomebar results don\'t show the correct search engine when searching with search engine ' \
                    'keywords.',
        locale=['en-US'],
        test_case_id='111378',
        test_suite_id='83',
    )
    def run(self, firefox):
        about_preferences_search_page_pattern = Pattern('about_preferences_search_page.png')
        keyword_field_pattern = Pattern('keyword_field.png')
        moz_search_bing_pattern = Pattern('moz_search_bing.png').similar(0.6)

        navigate('about:preferences#search')

        expected = exists(about_preferences_search_page_pattern, 10)
        assert expected is True, 'The \'about:preferences#search\' page successfully loaded.'

        paste('keyword')

        expected = exists(keyword_field_pattern, 10)
        assert expected is True, 'The keyword field is visible.'

        double_click(keyword_field_pattern)
        paste('bn')
        time.sleep(Settings.DEFAULT_UI_DELAY_LONG)
        select_location_bar()
        paste('bn moz')

        expected = exists(moz_search_bing_pattern, 10)
        assert expected is True, 'Results from URL bar state that the search will be performed with \'Bing\'.'

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Search Code Testing: Bing - US',
        locale=['en-US'],
        test_case_id='218334',
        test_suite_id='83',
    )
    def run(self, firefox):
        default_search_engine_google_pattern = Pattern('default_search_engine_google.png')
        default_search_engine_dropdown_pattern = Pattern('default_search_engine_dropdown.png')
        test_search_bing_pattern = Pattern('test_search_bing.png')

        change_preference('browser.search.widget.inNavBar', True)

        navigate('about:preferences#search')
        expected = exists(default_search_engine_google_pattern.similar(0.7), 10)
        assert expected is True, 'Google is the default search engine.'

        # Change the default search engine to Bing.
        click(default_search_engine_dropdown_pattern)
        repeat_key_down(1)
        type(Key.ENTER)

        select_location_bar()
        paste('test')
        type(Key.ENTER)

        expected = exists(test_search_bing_pattern, 10)
        assert expected is True, 'The search is performed with the Bing engine.'

        select_location_bar()
        url_text = copy_to_clipboard()

        assert 'pc=MOZI&form=MOZLBR' in url_text, 'The resulted URL contains the \'pc=MOZI&form=MOZLBR\' string.'

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description='The Search Bar provides valid results for specific search terms.',
        locale=['en-US'],
        test_case_id='4264',
        test_suite_id='83',
    )
    def run(self, firefox):
        search_button_pattern = Pattern('search_button.png')
        test_pattern = Pattern('test.png')

        change_preference('browser.search.widget.inNavBar', True)

        select_search_bar()
        paste('test')

        region = Screen.UPPER_RIGHT_CORNER
        expected = region.exists(search_button_pattern, 10)
        assert expected is True, 'Search button found in the page.'

        region.click(search_button_pattern)

        region = Screen.UPPER_LEFT_CORNER
        expected = region.exists(test_pattern, 10)
        assert expected is True, 'The search engine page is opened with the search results for that term.'

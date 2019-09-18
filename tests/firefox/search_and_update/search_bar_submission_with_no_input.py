# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='The Search Bar accepts submission with no input.',
        locale=['en-US'],
        test_case_id='4263',
        test_suite_id='83',
    )
    def run(self, firefox):
        add_search_bar_in_toolbar_pattern = Pattern('add_search_bar_in_toolbar.png').similar(0.6)
        google_search_no_input_pattern = Pattern('google_search_no_input.png')

        navigate('about:preferences#search')

        expected = exists(add_search_bar_in_toolbar_pattern, 10)
        assert expected is True, 'Option found in the page.'

        click(add_search_bar_in_toolbar_pattern)

        expected = exists(LocationBar.SEARCH_BAR_MAGNIFYING_GLASS, 10)
        assert expected is True, 'Search bar successfully enabled in the page.'

        click(LocationBar.SEARCH_BAR_MAGNIFYING_GLASS.similar(.7))

        time.sleep(Settings.DEFAULT_UI_DELAY)

        type(Key.ENTER)

        expected = exists(google_search_no_input_pattern, 10)
        assert expected is True, 'The search engine page is opened with no searches performed.'

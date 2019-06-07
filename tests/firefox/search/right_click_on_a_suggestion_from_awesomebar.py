# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Right click on a result from Awesomebar closes the dropdown.',
        locale=['en-US'],
        test_case_id='111375',
        test_suite_id='83',
    )
    def run(self, firefox):
        wikipedia_search_bar_pattern = Pattern('wikipedia_search_bar.png').similar(0.6)
        mozilla_suggestion_pattern = Pattern('mozilla_suggestion.png')
        test_bold_pattern = Pattern('test_bold.png')

        # Enable the search bar.
        change_preference('browser.search.widget.inNavBar', True)

        navigate(LocalWeb.MOZILLA_TEST_SITE)

        expected = exists(LocalWeb.MOZILLA_LOGO, 10)
        assert expected is True, 'Mozilla page loaded successfully.'

        # Check that the dropdown stays open after right clicking on a suggestion from the location bar.
        select_location_bar()
        paste('127.0.0.1')

        expected = exists(wikipedia_search_bar_pattern, 10)
        assert expected is True, 'Wikipedia one off is successfully displayed.'

        expected = exists(mozilla_suggestion_pattern, 10)
        assert expected is True, 'Search suggestions successfully displayed.'

        right_click(mozilla_suggestion_pattern)

        expected = exists(wikipedia_search_bar_pattern, 10)
        assert expected is True, 'The dropdown stays open after right clicking on a suggestion from the location bar.'

        # Check that the dropdown stays open after right clicking on a suggestion from the search bar.
        select_search_bar()
        paste('test')

        expected = exists(wikipedia_search_bar_pattern, 10)
        assert expected is True, 'Wikipedia one off is successfully displayed.'

        region_int = Screen.UPPER_RIGHT_CORNER
        region = region_int.middle_third_horizontal()

        expected = region.exists(test_bold_pattern, 10)
        assert expected is True, 'Search suggestions are shown for the input in question.'

        region.right_click(test_bold_pattern, 1)

        expected = exists(wikipedia_search_bar_pattern, 10)
        assert expected is True, 'The dropdown stays open after right clicking on a suggestion from search bar.'

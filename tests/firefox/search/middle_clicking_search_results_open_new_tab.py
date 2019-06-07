# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Middle clicking search results does not open a new tab.',
        locale=['en-US'],
        test_case_id='111373',
        test_suite_id='83',
    )
    def run(self, firefox):
        test_bold_pattern = Pattern('test_bold.png')

        # Enable the search bar.
        change_preference('browser.search.widget.inNavBar', True)

        select_search_bar()
        paste('test')
        time.sleep(Settings.DEFAULT_UI_DELAY_LONG)

        expected = exists(test_bold_pattern, 10)
        assert expected is True, 'Search suggestions are displayed in the search bar.'

        middle_click(test_bold_pattern)
        time.sleep(Settings.DEFAULT_UI_DELAY_LONG)

        expected = exists(test_bold_pattern, 10)
        assert expected is True, 'The search box stays in focus after middle click.'

        next_tab()
        select_location_bar()
        url_text = copy_to_clipboard()

        assert 'test' in url_text, 'A new tab is opened and contains the searched item.'

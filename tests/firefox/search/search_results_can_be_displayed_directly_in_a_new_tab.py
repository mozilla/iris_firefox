# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Search results can be displayed directly in a new tab.',
        locale=['en-US'],
        test_case_id='4266',
        test_suite_id='83',
    )
    def run(self, firefox):
        iris_logo_tab_pattern = Pattern('iris_logo_tab.png')
        test_pattern = Pattern('test.png')

        change_preference('browser.search.widget.inNavBar', True)

        select_search_bar()
        paste('test')
        key_down(Key.ALT)
        type(Key.ENTER)
        time.sleep(Settings.DEFAULT_UI_DELAY_LONG)
        key_up(Key.ALT)

        expected = exists(iris_logo_tab_pattern, 10)
        assert expected is True, 'Iris tab is not in focus.'

        close_content_blocking_pop_up()

        expected = exists(test_pattern, 10)
        assert expected is True, 'The search results are shown in a new tab.'

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='A history of previous searches is kept for all the search fields.',
        locale=['en-US'],
        test_case_id='4270',
        test_suite_id='83',
    )
    def run(self, firefox):
        google_logo_content_search_field_pattern = Pattern('google_logo_content_search_field.png')
        search_button_pattern = Pattern('search_button.png')
        history_pattern = Pattern('history_content_search.png')
        history_search_bar_pattern = Pattern('history_search_bar.png')
        recent_history_pattern = Pattern('recent_history.png')

        change_preference('browser.search.widget.inNavBar', True)

        text_list = ['test', 'moz', 'testing', 'mozilla']

        # Make history from the content search field.
        for i in range(int(len(text_list) / 2)):
            navigate('about:newtab')

            if i == 0:
                expected = exists(google_logo_content_search_field_pattern, 10)
                assert expected is True, 'Google logo from content search field found.'

            click(google_logo_content_search_field_pattern)
            paste(text_list[i])

            region = Screen.RIGHT_THIRD
            if i == 0:
                expected = region.exists(search_button_pattern, 10)
                assert expected is True, 'Search button found in the page.'

            region.click(search_button_pattern)
            time.sleep(Settings.DEFAULT_UI_DELAY)

        # Make history from the search bar field.
        for i in range(int(len(text_list) / 2)):
            select_search_bar()
            paste(text_list[i + 2])

            region = Screen.UPPER_RIGHT_CORNER
            if i == 0:
                expected = region.exists(search_button_pattern, 10)
                assert expected is True, 'Search button found in the page.'

            region.click(search_button_pattern)
            time.sleep(Settings.DEFAULT_UI_DELAY)

        firefox.restart()
        navigate(LocalWeb.FIREFOX_TEST_SITE)
        time.sleep(Settings.DEFAULT_UI_DELAY_LONG)

        navigate('about:newtab')
        time.sleep(Settings.DEFAULT_UI_DELAY_LONG)
        click(google_logo_content_search_field_pattern)
        type(Key.DOWN)

        expected = exists(history_pattern, 10)
        assert expected is True, 'The previous searches are visible in the content search field.'

        select_search_bar()
        type(Key.DOWN)

        expected = exists(history_search_bar_pattern, 10)
        assert expected is True, 'The previous searches are visible in the search bar.'

        open_library_menu('History')
        expected = exists(recent_history_pattern, 10)
        assert expected is True, 'The previous searches are kept in history.'

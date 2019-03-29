# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description="This test case perform one-offs searches in private browsing.",
        locale='[en-US]',
        test_case_id="108253",
        test_suite_id="1902",
        locales=['en-US']
    )
    def test_run(self, firefox):
        moz_pattern = Pattern('moz.png')
        url = LocalWeb.FIREFOX_TEST_SITE
        search_settings_pattern = Pattern('search_settings.png')
        twitter_one_off_button_highlight_pattern = Pattern('twitter_one_off_button_highlight.png')
        new_tab_twitter_search_results_pattern = Pattern('new_tab_twitter_search_results.png')
        new_tab_twitter_search_results_pattern2 = Pattern('new_tab_twitter_search_results_2.png')
        google_on_off_button_private_window_pattern = Pattern('google_on_off_button_private_window.png')
        magnifying_glass_pattern = Pattern('magnifying_glass.png')
        test_pattern = Pattern('test.png')

        new_private_window()

        navigate(url)

        region = Region(0, 0, Screen().width, 2 * Screen().height / 3)

        expected = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert expected, 'Page successfully loaded, firefox logo found.'

        select_location_bar()
        paste('moz')

        expected = region.exists(moz_pattern, 10)
        assert expected, 'Searched string found at the bottom of the drop-down list.'

        expected = region.exists(search_settings_pattern, 10)
        assert expected, 'The \'Search settings\' button is displayed in the awesome bar.'

        repeat_key_up(3)
        key_to_one_off_search(twitter_one_off_button_highlight_pattern, )

        expected = region.exists(twitter_one_off_button_highlight_pattern, 10)
        assert expected, 'The \'Twitter\' one-off button is highlighted.'

        type(Key.ENTER)
        time.sleep(Settings.DEFAULT_UI_DELAY_LONG)

        expected = exists(new_tab_twitter_search_results_pattern, 10) \
                   or exists(new_tab_twitter_search_results_pattern2, 5)
        assert expected, 'Twitter search results are opened in the same tab.'

        new_tab()
        time.sleep(Settings.DEFAULT_UI_DELAY_LONG)

        select_location_bar()
        paste('test')

        expected = region.exists(google_on_off_button_private_window_pattern, 10)
        assert expected, 'The\'Google\' one-off button found.'

        if OSHelper.is_mac():
            key_down(Key.CMD)
        else:
            key_down(Key.CTRL)

        click(google_on_off_button_private_window_pattern)

        if OSHelper.is_mac():
            key_up(Key.CMD)
        else:
            key_up(Key.CTRL)

        next_tab()

        expected = region.exists(magnifying_glass_pattern, 10)
        assert expected, 'Page successfully loaded using the \'Google\' engine.'

        expected = region.exists(test_pattern, 10)
        assert expected, 'Searched item is successfully found in the page opened by the \'Google\' search engine.'

        close_window()

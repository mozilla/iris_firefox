# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description='Default Search Code: Baidu - China.',
        locale=['zh-CN'],
        test_case_id='218337',
        test_suite_id='83',
        profile=Profiles.BRAND_NEW,
        preferences={'browser.search.region': 'CN'}
    )
    def run(self, firefox):
        url = LocalWeb.FOCUS_TEST_SITE
        text_pattern = Pattern('focus_text.png')
        default_search_engine_baidu_pattern = Pattern('default_search_engine_baidu.png')

        change_preference('browser.search.widget.inNavBar', True)
        change_preference('browser.tabs.warnOnClose', True)
        time.sleep(Settings.DEFAULT_UI_DELAY)

        navigate('about:preferences#search')
        expected = exists(default_search_engine_baidu_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, 'Baidu is the default search engine.'

        # Perform a search using the awesome bar and then clear the content from it.
        select_location_bar()
        paste('test')
        type(Key.ENTER)
        time.sleep(Settings.DEFAULT_UI_DELAY_LONG)
        select_location_bar()
        url_text = copy_to_clipboard()

        assert '/baidu?wd=test&tn=monline_7_dg' in url_text, 'The resulting URL contains the ' \
                                                             '\'monline_7_dg\' string.'

        select_location_bar()
        type(Key.DELETE)

        # Perform a search using the search bar.
        select_search_bar()
        paste('test')
        type(Key.ENTER)
        time.sleep(Settings.DEFAULT_UI_DELAY_LONG)
        select_location_bar()
        url_text = copy_to_clipboard()

        assert '/baidu?wd=test&tn=monline_7_dg' in url_text, 'The resulting URL contains the ' \
                                                             '\'monline_7_dg\' string.'

        # Highlight some text and right click it.
        new_tab()
        navigate(url)
        expected = exists(text_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert expected, 'Page successfully loaded, focus text found.'

        double_click(text_pattern)
        time.sleep(Settings.DEFAULT_UI_DELAY_SHORT)
        right_click(text_pattern)
        time.sleep(Settings.DEFAULT_UI_DELAY_SHORT)
        repeat_key_down(3)
        type(Key.ENTER)
        time.sleep(Settings.DEFAULT_UI_DELAY_LONG)
        select_location_bar()
        url_text = copy_to_clipboard()

        assert '/baidu?wd=Focus&tn=monline_7_dg' in url_text, 'The resulting URL contains the ' \
                                                              '\'monline_7_dg\' string.'

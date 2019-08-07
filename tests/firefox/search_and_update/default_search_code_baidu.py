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
        blocked_by={'id': 'issue_3509', 'platform': OSPlatform.ALL}
    )
    def run(self, firefox):
        url = LocalWeb.FOCUS_TEST_SITE
        text_pattern = Pattern('focus_text.png')
        default_search_engine_baidu_pattern = Pattern('default_search_engine_baidu.png')

        change_preference('browser.search.widget.inNavBar', True)
        change_preference('browser.search.region', 'CN')

        # Remove the file 'search.json.mozlz4' from the profile directory.
        profile_temp = PathManager.get_temp_dir()
        parent, test = PathManager.parse_module_path()
        search_json_mozlz4_path = os.path.join(profile_temp, '%s_%s' % (parent, test))
        if os.path.isfile(search_json_mozlz4_path):
            os.remove(os.path.join(search_json_mozlz4_path, 'search.json.mozlz4'))

        firefox.restart(url=LocalWeb.FIREFOX_TEST_SITE,
                        image=LocalWeb.FIREFOX_LOGO)
        time.sleep(Settings.DEFAULT_UI_DELAY_LONG)

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
        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)
        right_click(text_pattern)
        time.sleep(Settings.DEFAULT_FX_DELAY)
        repeat_key_down(3)
        type(Key.ENTER)
        time.sleep(Settings.DEFAULT_UI_DELAY_LONG)
        select_location_bar()
        url_text = copy_to_clipboard()

        assert '/baidu?wd=focus&tn=monline_7_dg' in url_text, 'The resulting URL contains the ' \
                                                                                   '\'monline_7_dg\' string.'

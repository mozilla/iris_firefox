# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Default Search Code: Baidu - China.'
        self.test_case_id = '218337'
        self.test_suite_id = '83'
        self.locale = ['zh-CN']

    def setup(self):
        BaseTest.setup(self)
        self.profile = Profile.BRAND_NEW

    def run(self):
        url = LocalWeb.FOCUS_TEST_SITE
        text_pattern = Pattern('focus_text.png')
        default_search_engine_baidu_pattern = Pattern('default_search_engine_baidu.png')

        change_preference('browser.search.widget.inNavBar', True)
        change_preference('browser.search.region', 'CN')

        # Remove the file 'search.json.mozlz4' from the profile directory.
        profile_temp = IrisCore.get_tempdir()
        parent, test = IrisCore.parse_module_path()
        search_json_mozlz4_path = os.path.join(profile_temp, '%s_%s' % (parent, test))
        os.remove(os.path.join(search_json_mozlz4_path, 'search.json.mozlz4'))

        restart_firefox(self,
                        self.browser.path,
                        self.profile_path,
                        LocalWeb.FIREFOX_TEST_SITE,
                        image=LocalWeb.FIREFOX_LOGO)
        time.sleep(DEFAULT_UI_DELAY_LONG)

        navigate('about:preferences#search')
        expected = exists(default_search_engine_baidu_pattern, 10)
        assert_true(self, expected, 'Baidu is the default search engine.')

        # Perform a search using the awesome bar and then clear the content from it.
        select_location_bar()
        paste('test')
        type(Key.ENTER)
        time.sleep(DEFAULT_UI_DELAY_LONG)
        select_location_bar()
        url_text = copy_to_clipboard()

        assert_contains(self, url_text, 'monline_dg', 'The resulting URL contains the \'monline_dg\' string.')

        select_location_bar()
        type(Key.DELETE)

        # Perform a search using the search bar.
        select_search_bar()
        paste('test')
        type(Key.ENTER)
        time.sleep(DEFAULT_UI_DELAY_LONG)
        select_location_bar()
        url_text = copy_to_clipboard()

        assert_contains(self, url_text, 'monline_dg', 'The resulting URL contains the \'monline_dg\' string.')

        # Highlight some text and right click it.
        new_tab()
        navigate(url)
        expected = exists(text_pattern, 50)
        assert_true(self, expected, 'Page successfully loaded, focus text found.')

        double_click(text_pattern)
        right_click(text_pattern)
        time.sleep(DEFAULT_FX_DELAY)
        repeat_key_down(3)
        type(Key.ENTER)
        time.sleep(DEFAULT_UI_DELAY_LONG)
        select_location_bar()
        url_text = copy_to_clipboard()

        assert_contains(self, url_text, 'monline_dg', 'The resulting URL contains the \'monline_dg\' string.')

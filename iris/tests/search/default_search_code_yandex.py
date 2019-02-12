# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Default Search Code: Yandex: Russia.'
        self.test_case_id = '218336'
        self.test_suite_id = '83'
        self.exclude = Platform.ALL

    def setup(self):
        BaseTest.setup(self)
        self.profile = Profile.BRAND_NEW

    def run(self):
        url = LocalWeb.FOCUS_TEST_SITE
        text_pattern = Pattern('focus_text.png')

        # Detect the build.
        if get_firefox_channel(self.browser.path) == 'beta' or get_firefox_channel(self.browser.path) == 'release':
            default_search_engine_yandex_pattern = Pattern('default_search_engine_yandex.png')
            yandex_logo_content_search_field_pattern = Pattern('yandex_logo_content_search_field.png')
        elif get_firefox_channel(self.browser.path) == 'esr':
            default_search_engine_yandex_pattern = Pattern('default_search_engine_yandex_esr_build.png')
            yandex_logo_content_search_field_pattern = Pattern('yandex_logo_content_search_field_esr_build.png')

        regions_by_locales = {'ru': ['RU'], 'be': ['BY'], 'kk': ['KZ'], 'tr': ['TR']}

        change_preference('browser.search.widget.inNavBar', True)

        # Detect the locale.
        for value in regions_by_locales.get(self.browser.locale):
            change_preference('browser.search.region', value)

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
        expected = exists(default_search_engine_yandex_pattern, 10)
        assert_true(self, expected, 'Yandex is the default search engine.')

        # Perform a search using the awesome bar and then clear the content from it.
        select_location_bar()
        paste('test')
        type(Key.ENTER)
        time.sleep(DEFAULT_UI_DELAY_LONG)
        select_location_bar()
        time.sleep(DEFAULT_UI_DELAY)
        edit_copy()
        time.sleep(DEFAULT_UI_DELAY)
        url_text = Env.get_clipboard()

        assert_contains(self, url_text, 'search/?clid=2186621',
                        'Client search code is correct for searches from awesome bar, region ' + value + '.')

        select_location_bar()
        type(Key.DELETE)

        # Perform a search using the search bar.
        select_search_bar()
        paste('test')
        type(Key.ENTER)
        time.sleep(DEFAULT_UI_DELAY_LONG)
        select_location_bar()
        time.sleep(DEFAULT_UI_DELAY)
        edit_copy()
        time.sleep(DEFAULT_UI_DELAY)
        url_text = Env.get_clipboard()

        assert_contains(self, url_text, 'search/?clid=2186618',
                        'Client search code is correct for searches from search bar, region ' + value + '.')

        # Highlight some text and right click it.
        new_tab()
        navigate(url)
        expected = exists(text_pattern, 10)
        assert_true(self, expected, 'Page successfully loaded, focus text found.')

        double_click(text_pattern)
        right_click(text_pattern)
        time.sleep(DEFAULT_FX_DELAY)
        repeat_key_down(3)
        type(Key.ENTER)
        time.sleep(DEFAULT_UI_DELAY_LONG)
        select_location_bar()
        time.sleep(DEFAULT_UI_DELAY)
        edit_copy()
        time.sleep(DEFAULT_UI_DELAY)
        url_text = Env.get_clipboard()

        assert_contains(self, url_text, 'search/?clid=2186623',
                        'Client search code is correct for searches with context menu, region ' + value + '.')

        # Perform a search from about:newtab page, content search field.
        new_tab()
        expected = exists(yandex_logo_content_search_field_pattern, 10)
        assert_true(self, expected, 'Yandex logo from content search field found.')
        click(yandex_logo_content_search_field_pattern)
        paste('beats')
        type(Key.ENTER)
        time.sleep(DEFAULT_UI_DELAY_LONG)
        select_location_bar()
        time.sleep(DEFAULT_UI_DELAY)
        edit_copy()
        time.sleep(DEFAULT_UI_DELAY)
        url_text = Env.get_clipboard()

        assert_contains(self, url_text, 'search/?clid=2186620',
                        'Client search code is correct for searches from about:newtab page, content search '
                        'field, region ' + value + '.')

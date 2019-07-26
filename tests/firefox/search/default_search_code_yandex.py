# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description='Default Search Code: Yandex: Russia.',
        locale=['ru', 'be', 'kk', 'tr', 'en-US', 'en-GB', 'en-ZA'],
        test_case_id='218336',
        test_suite_id='83',
        profile=Profiles.BRAND_NEW,
        blocked_by={'id': 'issue_3509', 'platform': OSPlatform.ALL}
    )
    def run(self, firefox):
        url = LocalWeb.FOCUS_TEST_SITE

        # Detect the build.
        if FirefoxUtils.get_firefox_channel(firefox.application.path) == 'beta' \
                or FirefoxUtils.get_firefox_channel(firefox.application.path) == 'release':
            default_search_engine_yandex_pattern = Pattern('default_search_engine_yandex.png').similar(0.5)
            yandex_logo_content_search_field_pattern = Pattern('yandex_logo_content_search_field.png')
        elif FirefoxUtils.get_firefox_channel(firefox.application.path) == 'esr':
            default_search_engine_yandex_pattern = Pattern('default_search_engine_yandex_esr_build.png').similar(0.5)
            yandex_logo_content_search_field_pattern = Pattern('yandex_logo_content_search_field_esr_build.png')

        regions_by_locales = {'ru': ['RU'], 'be': ['BY'], 'kk': ['KZ'], 'tr': ['TR'],
                              'en-US': ['RU', 'BY', 'KZ', 'TR'],
                              'en-GB': ['RU', 'BY', 'KZ', 'TR'],
                              'en-ZA': ['RU', 'BY', 'KZ', 'TR']}

        change_preference('browser.search.widget.inNavBar', True)

        # Detect the locale.
        for value in regions_by_locales.get(firefox.application.locale):
            change_preference('browser.search.region', value)

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
            expected = exists(default_search_engine_yandex_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
            assert expected, 'Yandex is the default search engine.'

            # Perform a search using the awesome bar and then clear the content from it.
            select_location_bar()
            paste('test')
            type(Key.ENTER)
            time.sleep(Settings.DEFAULT_UI_DELAY_LONG)
            select_location_bar()
            url_text = copy_to_clipboard()

            assert '/search/?text=test&clid=2186621' in url_text, 'Client search code is correct for searches from awesome ' \
                                                       'bar, region ' + value + '.'

            select_location_bar()
            type(Key.DELETE)

            # Perform a search using the search bar.
            select_search_bar()
            paste('test')
            type(Key.ENTER)
            time.sleep(Settings.DEFAULT_UI_DELAY_LONG)
            select_location_bar()
            url_text = copy_to_clipboard()

            assert '/search/?text=test&clid=2186618' in url_text, 'Client search code is correct for searches from ' \
                                                       'search bar, region ' + value + '.'

            # Highlight some text and right click it.
            new_tab()
            navigate(url)
            expected = exists(LocalWeb.FOCUS_LOGO, 10)
            assert expected, 'Page successfully loaded, Focus logo found.'

            area = Screen().new_region(0, 0, Screen.SCREEN_WIDTH / 5, Screen.SCREEN_HEIGHT / 4)
            area.double_click('Focus')
            time.sleep(Settings.DEFAULT_UI_DELAY_SHORT)
            click_loc = Location(400, 300)
            area.right_click(click_loc)
            time.sleep(Settings.DEFAULT_UI_DELAY_SHORT)
            repeat_key_down(3)
            type(Key.ENTER)
            time.sleep(Settings.DEFAULT_UI_DELAY_LONG)
            select_location_bar()
            url_text = copy_to_clipboard()

            assert '/search/?text=Focus&clid=2186623' in url_text, 'Client search code is correct for searches ' \
                                                       'with context menu, region ' + value + '.'

            # Perform a search from about:newtab page, content search field.
            new_tab()
            expected = exists(yandex_logo_content_search_field_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
            assert expected, 'Yandex logo from content search field found.'

            click(yandex_logo_content_search_field_pattern)

            paste('beats')
            type(Key.ENTER)
            time.sleep(Settings.DEFAULT_UI_DELAY_LONG)
            select_location_bar()
            url_text = copy_to_clipboard()

            assert '/search/?text=beats&clid=2186620' in url_text, 'Client search code is correct for searches ' \
                                                       'from about:newtab page, content search field, region ' + value + '.'

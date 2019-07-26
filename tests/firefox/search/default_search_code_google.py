# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description='Default Search Code: Google.',
        locale=['en-US', 'de', 'fr', 'pl', 'it', 'pt-BR', 'ja', 'es-ES', 'en-GB', 'ru'],
        test_case_id='218333',
        test_suite_id='83',
        profile=Profiles.BRAND_NEW,
        blocked_by={'id': 'issue_3509', 'platform': OSPlatform.ALL}
    )
    def run(self, firefox):
        url = LocalWeb.FOCUS_TEST_SITE
        text_pattern = Pattern('focus_text.png')
        text_pattern_selected = Pattern('focus_text_selected.png')

        # Detect the build.
        if FirefoxUtils.get_firefox_channel(firefox.application.path) == 'beta' or \
                FirefoxUtils.get_firefox_channel(firefox.application.path) == 'release':
            default_search_engine_google_pattern = Pattern('default_search_engine_google.png').similar(0.5)
            google_logo_content_search_field_pattern = Pattern('google_logo_content_search_field.png')
        elif FirefoxUtils.get_firefox_channel(firefox.application.path) == 'esr':
            default_search_engine_google_pattern = Pattern('default_search_engine_google_esr_build.png').similar(0.5)
            google_logo_content_search_field_pattern = Pattern('google_logo_content_search_field_esr_build.png')

        regions_by_locales = {'en-US': ['US', 'in', 'id', 'ca'], 'de': ['de', 'ru'], 'fr': ['fr'], 'pl': ['pl'],
                              'it': ['it'], 'pt-BR': ['BR'], 'ja': ['ja'], 'es-ES': ['ES'], 'en-GB': ['GB'],
                              'ru': ['de']}

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

            firefox.restart(url=LocalWeb.FIREFOX_TEST_SITE, image=LocalWeb.FIREFOX_LOGO)
            time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)

            navigate('about:preferences#search')

            default_search_engine_check = exists(default_search_engine_google_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
            assert default_search_engine_check, 'Google is the default search engine.'

            # Perform a search using the awesome bar and then clear the content from it.
            select_location_bar()
            time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)
            paste('test')
            time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)
            type(Key.ENTER)
            time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)
            select_location_bar()
            url_text = copy_to_clipboard()

            if FirefoxUtils.get_firefox_channel(firefox.application.path) == 'beta' \
                    or FirefoxUtils.get_firefox_channel(firefox.application.path) == 'release':
                if value != 'US':
                    assert url_text == 'https://www.google.com/search?client=firefox-b-d&q=test', \
                        'Client search code is correct for searches from awesome bar, region ' + value + '.'
                else:
                    assert url_text == 'https://www.google.com/search?client=firefox-b-1-d&q=test', \
                        'Client search code is correct for searches from awesome bar, region ' + value + '.'
            elif FirefoxUtils.get_firefox_channel(firefox.application.path) == 'esr':
                if value != 'US':
                    assert url_text == 'https://www.google.com/search?q=test&ie=utf-8&oe=utf-8&client=firefox-b-e', \
                        'Client search code is correct for searches from awesome bar, region ' + value + '.'
                else:
                    assert url_text == 'https://www.google.com/search?q=test&ie=utf-8&oe=utf-8&client=firefox-b-1-e', \
                        'Client search code is correct for searches from awesome bar, region ' + value + '.'

            select_location_bar()
            type(Key.DELETE)

            # Perform a search using the search bar.
            select_search_bar()
            time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)
            paste('test')
            time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)
            type(Key.ENTER)
            time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)
            select_location_bar()
            url_text = copy_to_clipboard()

            if FirefoxUtils.get_firefox_channel(firefox.application.path) == 'beta' or \
                    FirefoxUtils.get_firefox_channel(firefox.application.path) == 'release':
                if value != 'US':
                    assert url_text == 'https://www.google.com/search?client=firefox-b-d&q=test', \
                                       'Client search code is correct for searches from search bar, region ' + \
                                       value + '.'
                else:
                    assert url_text == 'https://www.google.com/search?client=firefox-b-1-d&q=test',\
                        'Client search code is correct for searches from search bar, region ' + value + '.'

            elif FirefoxUtils.get_firefox_channel(firefox.application.path) == 'esr':
                if value != 'US':
                    assert url_text == 'https://www.google.com/search?q=test&ie=utf-8&oe=utf-8&client=firefox-b-e', \
                        'Client search code is correct for searches from search bar, region ' + value + '.'
                else:
                    assert url_text == 'https://www.google.com/search?q=test&ie=utf-8&oe=utf-8&client=firefox-b-1-e',\
                        'Client search code is correct for searches from search bar, region ' + value + '.'

            # Highlight some text and right click it.
            new_tab()

            navigate(url)

            focus_page_loaded = exists(text_pattern, FirefoxSettings.HEAVY_SITE_LOAD_TIMEOUT)
            assert focus_page_loaded, 'Page successfully loaded, focus text found.'

            double_click(text_pattern)
            time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)
            right_click(text_pattern_selected)
            time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)
            repeat_key_down(3)
            type(Key.ENTER)
            time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)
            select_location_bar()
            url_text = copy_to_clipboard()

            if FirefoxUtils.get_firefox_channel(firefox.application.path) == 'beta' or \
                    FirefoxUtils.get_firefox_channel(firefox.application.path) == 'release':
                if value != 'US':
                    assert url_text == 'https://www.google.com/search?client=firefox-b-d&q=Focus', \
                        'Client search code is correct, region ' + value + '.'
                else:
                    assert url_text == 'https://www.google.com/search?client=firefox-b-1-d&q=Focus', \
                        'Client search code is correct, region ' + value + '.'
            elif FirefoxUtils.get_firefox_channel(firefox.application.path) == 'esr':
                if value != 'US':
                    assert url_text == 'https://www.google.com/search?q=Focus&ie=utf-8&oe=utf-8&client=firefox-b-e', \
                        'Client search code is correct, region ' + value + '.'
                else:
                    assert url_text == 'https://www.google.com/search?q=Focus&ie=utf-8&oe=utf-8&client=firefox-b-1-e',\
                        'Client search code is correct, region ' + value + '.'

            # Perform a search from about:newtab page, content search field.
            new_tab()

            google_logo_found = exists(google_logo_content_search_field_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
            assert google_logo_found, 'Google logo from content search field found.'

            click(google_logo_content_search_field_pattern)
            time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)
            paste('beats')
            time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)
            type(Key.ENTER)
            time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)
            select_location_bar()
            url_text = copy_to_clipboard()

            if FirefoxUtils.get_firefox_channel(firefox.application.path) == 'beta' or \
                    FirefoxUtils.get_firefox_channel(firefox.application.path) == 'release':
                if value != 'US':
                    assert url_text == 'https://www.google.com/search?client=firefox-b-d&q=beats',\
                        'Client search code is correct for searches from about:newtab page, content search field, ' \
                        'region ' + value + '.'
                else:
                    assert url_text == 'https://www.google.com/search?client=firefox-b-1-d&q=beats',\
                        'Client search code is correct for searches from about:newtab page, content search field, ' \
                        'region ' + value + '.'
            elif FirefoxUtils.get_firefox_channel(firefox.application.path) == 'esr':
                if value != 'US':
                    assert url_text == 'https://www.google.com/search?q=beats&ie=utf-8&oe=utf-8&client=firefox-b-e', \
                        'Client search code is correct for searches from about:newtab page, content search field, ' \
                        'region ' + value + '.'
                else:
                    assert url_text == 'https://www.google.com/search?q=beats&ie=utf-8&oe=utf-8&client=firefox-b-1-e', \
                        'Client search code is correct for searches from about:newtab page, content search field, ' \
                        'region ' + value + '.'

        if firefox.application.locale == 'en-US':
            change_preference('browser.search.region', 'US')

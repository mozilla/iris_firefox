# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from src.core.util.arg_parser import get_core_args
from targets.firefox.fx_testcase import *
from targets.firefox.main import *


class Test(FirefoxTest):
    # Set the region from command line flag, if given.
    # Command line flag is for testing en-US locale in IN, ID and CA regions, de locale in RU and ru locale in DE.
    # Otherwise, we'll automatically set the region based on the Firefox locale under test.
    global fx_region_code
    region_arg = Target().get_target_args().region
    if region_arg != '':
        fx_region_code = region_arg
    else:
        regions_by_locales = {'en-US': 'US', 'de': 'DE', 'fr': 'FR', 'pl': 'PL', 'it': 'IT', 'pt-BR': 'BR',
                              'ja': 'JA', 'es-ES': 'ES', 'en-GB': 'GB', 'ru': 'DE'}
        fx_locale_code = get_core_args().locale
        fx_region_code = regions_by_locales[fx_locale_code]

    @pytest.mark.details(
        description='Default Search Code: Google.',
        locale=['en-US', 'de', 'fr', 'pl', 'it', 'pt-BR', 'ja', 'es-ES', 'en-GB', 'ru'],
        test_case_id='218333',
        test_suite_id='83',
        profile=Profiles.BRAND_NEW,
        preferences={'browser.search.region': fx_region_code,
                     'browser.search.cohort': 'nov17-1'}
    )
    def run(self, firefox):
        url = LocalWeb.FOCUS_TEST_SITE
        text_pattern = Pattern('focus_text.png')
        text_pattern_selected = Pattern('focus_text_selected.png')

        change_preference('browser.search.widget.inNavBar', True)
        change_preference('browser.tabs.warnOnClose', True)

        default_search_engine_google_pattern = Pattern('default_search_engine_google.png')
        google_logo_content_search_field_pattern = Pattern('google_logo_content_search_field.png')

        navigate('about:preferences#search')

        default_search_engine_check = exists(default_search_engine_google_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert default_search_engine_check, 'Google is the default search engine.'

        # Perform a search using the awesome bar and then clear the content from it.
        select_location_bar()
        paste('test')
        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)
        type(Key.ENTER)
        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)
        select_location_bar()
        url_text = copy_to_clipboard()

        if FirefoxUtils.get_firefox_channel(firefox.application.path) == 'beta' \
                or FirefoxUtils.get_firefox_channel(firefox.application.path) == 'release':
            if fx_region_code != 'US':
                assert url_text == 'https://www.google.com/search?client=firefox-b-d&q=test', \
                    'Client search code is correct for searches from awesome bar, region ' + fx_region_code + '.'
            else:
                assert url_text == 'https://www.google.com/search?client=firefox-b-1-d&q=test', \
                    'Client search code is correct for searches from awesome bar, region ' + fx_region_code + '.'
        elif FirefoxUtils.get_firefox_channel(firefox.application.path) == 'esr':
            if fx_region_code != 'US':
                assert url_text == 'https://www.google.com/search?client=firefox-b-e&q=test', \
                    'Client search code is correct for searches from awesome bar, region ' + fx_region_code + '.'
            else:
                assert url_text == 'https://www.google.com/search?client=firefox-b-1-e&q=test', \
                    'Client search code is correct for searches from awesome bar, region ' + fx_region_code + '.'

        select_location_bar()
        type(Key.DELETE)

        # Perform a search using the search bar.
        select_search_bar()
        paste('test')
        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)
        type(Key.ENTER)
        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)
        select_location_bar()
        url_text = copy_to_clipboard()

        if FirefoxUtils.get_firefox_channel(firefox.application.path) == 'beta' or \
                FirefoxUtils.get_firefox_channel(firefox.application.path) == 'release':
            if fx_region_code != 'US':
                assert url_text == 'https://www.google.com/search?client=firefox-b-d&q=test', \
                                   'Client search code is correct for searches from search bar, region ' + \
                                   fx_region_code + '.'
            else:
                assert url_text == 'https://www.google.com/search?client=firefox-b-1-d&q=test',\
                    'Client search code is correct for searches from search bar, region ' + fx_region_code + '.'

        elif FirefoxUtils.get_firefox_channel(firefox.application.path) == 'esr':
            if fx_region_code != 'US':
                assert url_text == 'https://www.google.com/search?client=firefox-b-e&q=test', \
                    'Client search code is correct for searches from search bar, region ' + fx_region_code + '.'
            else:
                assert url_text == 'https://www.google.com/search?client=firefox-b-1-e&q=test', \
                    'Client search code is correct for searches from search bar, region ' + fx_region_code + '.'

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
            if fx_region_code != 'US':
                assert url_text == 'https://www.google.com/search?client=firefox-b-d&q=Focus', \
                    'Client search code is correct, region ' + fx_region_code + '.'
            else:
                assert url_text == 'https://www.google.com/search?client=firefox-b-1-d&q=Focus', \
                    'Client search code is correct, region ' + fx_region_code + '.'
        elif FirefoxUtils.get_firefox_channel(firefox.application.path) == 'esr':
            if fx_region_code != 'US':
                assert url_text == 'https://www.google.com/search?client=firefox-b-e&q=Focus', \
                    'Client search code is correct, region ' + fx_region_code + '.'
            else:
                assert url_text == 'https://www.google.com/search?client=firefox-b-1-e&q=Focus', \
                    'Client search code is correct, region ' + fx_region_code + '.'

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
            if fx_region_code != 'US':
                assert url_text == 'https://www.google.com/search?client=firefox-b-d&q=beats',\
                    'Client search code is correct for searches from about:newtab page, content search field, ' \
                    'region ' + fx_region_code + '.'
            else:
                assert url_text == 'https://www.google.com/search?client=firefox-b-1-d&q=beats',\
                    'Client search code is correct for searches from about:newtab page, content search field, ' \
                    'region ' + fx_region_code + '.'
        elif FirefoxUtils.get_firefox_channel(firefox.application.path) == 'esr':
            if fx_region_code != 'US':
                assert url_text == 'https://www.google.com/search?client=firefox-b-e&q=beats', \
                    'Client search code is correct for searches from about:newtab pageq, region ' + fx_region_code + '.'
            else:
                assert url_text == 'https://www.google.com/search?client=firefox-b-1-e&q=beats', \
                    'Client search code is correct for searches from about:newtab page, region ' + fx_region_code + '.'

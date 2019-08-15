# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from src.core.util.arg_parser import get_core_args
from targets.firefox.fx_testcase import *
from targets.firefox.main import *


class Test(FirefoxTest):
    # Set the region from command line argument, if given. Otherwise, set the region based on Firefox locale.
    # Use -g <region> for testing the English locales of Firefox in the four Yandex regions; RU, BY, KZ and TR.
    global fx_region_code
    region_arg = Target().get_target_args().region
    if region_arg != '':
        fx_region_code = region_arg
    else:
        regions_by_locales = {'ru': 'RU', 'be': 'BY', 'kk': 'KZ', 'tr': 'TR',
                              'en-US': 'RU', 'en-GB': 'RU', 'en-CA': 'RU'}
        fx_locale_code = get_core_args().locale
        fx_region_code = regions_by_locales[fx_locale_code]

    @pytest.mark.details(
        description='Default Search Code: Yandex: Russia.',
        locale=['ru', 'be', 'kk', 'tr', 'en-US', 'en-GB', 'en-CA'],
        test_case_id='218336',
        test_suite_id='83',
        profile=Profiles.BRAND_NEW,
        preferences={'browser.search.region': fx_region_code,
                     'browser.search.cohort': 'jan18-1'}
    )
    def run(self, firefox):
        url = LocalWeb.FOCUS_TEST_SITE
        text_pattern = Pattern('focus_text.png')

        change_preference('browser.search.widget.inNavBar', True)
        change_preference('browser.tabs.warnOnClose', True)

        default_search_engine_yandex_pattern = Pattern('default_search_engine_yandex.png')
        yandex_logo_content_search_field_pattern = Pattern('yandex_logo_content_search_field.png')

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

        assert '/search/?text=test&clid=2186621' in url_text, 'Client search code is correct for searches from' \
                                                              'awesomebar, region ' + fx_region_code + '.'

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
                                                              'search bar, region ' + fx_region_code + '.'

        # Highlight some text and right click it.
        new_tab()
        navigate(url)
        expected = exists(LocalWeb.FOCUS_LOGO, 10)
        assert expected, 'Page successfully loaded, Focus logo found.'

        double_click(text_pattern)
        time.sleep(Settings.DEFAULT_UI_DELAY_SHORT)
        right_click(text_pattern)
        time.sleep(Settings.DEFAULT_UI_DELAY_SHORT)
        repeat_key_down(3)
        type(Key.ENTER)
        time.sleep(Settings.DEFAULT_UI_DELAY_LONG)
        select_location_bar()
        url_text = copy_to_clipboard()

        assert '/search/?text=Focus&clid=2186623' in url_text, 'Client search code is correct for searches ' \
                                                               'with context menu, region ' + fx_region_code + '.'

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
                                                               'from content search field, region ' \
                                                               + fx_region_code + '.'

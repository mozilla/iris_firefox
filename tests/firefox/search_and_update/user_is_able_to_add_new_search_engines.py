# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='The user is able to add new search engines.',
        locale=['en-US'],
        test_case_id='4272',
        test_suite_id='83',
    )
    def run(self, firefox):
        add_startpage_https_privacy_search_engine_pattern = Pattern('add_startpage_https_privacy_search_engine.png')
        change_search_settings_pattern = Pattern('change_search_settings.png').similar(0.6)
        about_preferences_search_page_pattern = Pattern('about_preferences_search_page.png').similar(0.6)
        find_more_search_engines_pattern = Pattern('find_more_search_engines.png').similar(0.6)
        startpage_https_search_engine_pattern = Pattern('startpage_https_search_engine.png')
        find_add_ons_pattern = Pattern('find_add_ons.png')
        add_to_firefox_pattern = Pattern('add_to_firefox.png')
        add_button_pattern = Pattern('add_button.png')
        add_google_play_pattern = Pattern('add_google_play.png')
        google_play_search_engine_pattern = Pattern('google_play_search_engine.png')
        test_search_google_play_pattern = Pattern('test_search_google_play.png')
        google_logo_content_search_field_pattern = Pattern('google_logo_content_search_field.png')
        google_play_store_loaded_pattern = Pattern('google_play_store_loaded.png')

        # Enable the search bar.
        change_preference('browser.search.widget.inNavBar', True)

        select_search_bar()
        type(Key.DOWN)

        change_search_settings_button = exists(change_search_settings_pattern, Settings.DEFAULT_UI_DELAY)
        assert change_search_settings_button is True, 'The \'Change Search Settings\' button found in the page.'

        click(change_search_settings_pattern, 1)

        about_preferences_page_loaded = exists(about_preferences_search_page_pattern, Settings.DEFAULT_UI_DELAY)
        assert about_preferences_page_loaded is True, 'The \'about:preferences#search\' page opened.'

        time.sleep(Settings.DEFAULT_UI_DELAY)

        # Add a new search engine.
        for i in range(12):
            type(Key.TAB)

        if OSHelper.is_windows() or OSHelper.is_linux():
            type(Key.SPACE)
            scroll(-10)
        else:
            type(Key.TAB)

        expected = exists(find_more_search_engines_pattern, 10)
        assert expected is True, '\'Find more search engines\' link found.'

        click(find_more_search_engines_pattern)

        find_add_ons_button = exists(find_add_ons_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert find_add_ons_button is True, 'Find add-ons field is present on the page.'

        click(find_add_ons_pattern, 1)

        paste('startpage')

        add_startpage_search_engine_button = exists(add_startpage_https_privacy_search_engine_pattern,
                                                    FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert add_startpage_search_engine_button is True, '\'Startpage HTTPS Privacy Search Engine\' engine ' \
                                                           'successfully found.'

        click(add_startpage_https_privacy_search_engine_pattern)

        add_to_firefox_button = exists(add_to_firefox_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert add_to_firefox_button is True, '\'Add to Firefox\' button found.'

        click(add_to_firefox_pattern)

        add_button_found = exists(add_button_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert add_button_found is True, '\'Add\' button found.'

        click(add_button_pattern)

        previous_tab()

        startpage_search_engine_added = exists(startpage_https_search_engine_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert startpage_search_engine_added is True, 'The search engine added found in the \'One-Click Search ' \
                                                      'Engines\' section.'

        # Navigate to a page that could contain different search engines and can be added to Firefox.
        new_tab()
        navigate('https://play.google.com/store')
        time.sleep(Settings.DEFAULT_UI_DELAY_LONG)

        google_play_store_loaded = exists(google_play_store_loaded_pattern, Settings.DEFAULT_HEAVY_SITE_LOAD_TIMEOUT)
        assert google_play_store_loaded is True, 'Google play store website loaded'

        select_search_bar()
        type(Key.DOWN)

        add_google_play_button = exists(add_google_play_pattern, Settings.DEFAULT_HEAVY_SITE_LOAD_TIMEOUT)
        assert add_google_play_button is True, 'The \'Add \'Google Play\' button is found in the page.'

        click(add_google_play_pattern)

        # Prevent Unknown icon in search drop-down menu
        type(Key.ESC)
        select_search_bar()
        type(Key.DOWN)

        google_play_search_engine_added = exists(google_play_search_engine_pattern,
                                                 FirefoxSettings.HEAVY_SITE_LOAD_TIMEOUT)
        assert google_play_search_engine_added is True, 'The \'Google Play\' search engine is added to Firefox.'

        # Search using the search bar, the content search field and the location bar.
        paste('test')
        time.sleep(Settings.DEFAULT_UI_DELAY)

        google_play_search_engine_added = exists(google_play_search_engine_pattern,
                                                 FirefoxSettings.HEAVY_SITE_LOAD_TIMEOUT)
        assert google_play_search_engine_added is True, 'The \'Google Play\' search engine is available.'

        click(google_play_search_engine_pattern)

        test_search_google_play = exists(test_search_google_play_pattern.similar(0.7), FirefoxSettings.FIREFOX_TIMEOUT)
        assert test_search_google_play is True, 'Search performed using the search bar works properly.'

        navigate('about:newtab')

        google_logo_content_search_field = exists(google_logo_content_search_field_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert google_logo_content_search_field is True, 'Google logo from the content search found.'

        click(google_logo_content_search_field_pattern)

        paste('test')
        time.sleep(Settings.DEFAULT_UI_DELAY)

        google_play_search_engine_added = exists(google_play_search_engine_pattern,
                                                 FirefoxSettings.HEAVY_SITE_LOAD_TIMEOUT)
        assert google_play_search_engine_added is True, 'The \'Google Play\' search engine is available.'

        click(google_play_search_engine_pattern)

        test_search_google_play = exists(test_search_google_play_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert test_search_google_play is True, 'Search performed using the content search field works properly.'

        select_location_bar()

        paste('test')
        time.sleep(Settings.DEFAULT_UI_DELAY)

        google_play_search_engine_added = exists(google_play_search_engine_pattern,
                                                 FirefoxSettings.HEAVY_SITE_LOAD_TIMEOUT)
        assert google_play_search_engine_added is True, 'The \'Google Play\' search engine is available.'

        click(google_play_search_engine_pattern)

        test_search_google_play = exists(test_search_google_play_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert test_search_google_play is True, 'Search performed using the location bar works properly.'

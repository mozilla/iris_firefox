# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from iris.api.core import mouse
from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'The user is able to add new search engines.'
        self.test_case_id = '4272'
        self.test_suite_id = '83'
        self.locale = ['en-US']

    def run(self):
        add_startpage_https_privacy_search_engine_pattern = Pattern('add_startpage_https_privacy_search_engine.png')
        change_search_settings_pattern = Pattern('change_search_settings.png')
        about_preferences_search_page_pattern = Pattern('about_preferences_search_page.png')
        find_more_search_engines_pattern = Pattern('find_more_search_engines.png')
        startpage_https_search_engine_pattern = Pattern('startpage_https_search_engine.png')
        find_add_ons = Pattern('find_add_ons.png')
        add_to_firefox_pattern = Pattern('add_to_firefox.png')
        add_button_pattern = Pattern('add_button.png')
        add_google_play_pattern = Pattern('add_google_play.png')
        google_play_search_engine_pattern = Pattern('google_play_search_engine.png')
        test_search_google_play_pattern = Pattern('test_search_google_play.png')
        google_logo_content_search_field_pattern = Pattern('google_logo_content_search_field.png')

        # Enable the search bar.
        change_preference('browser.search.widget.inNavBar', True)

        select_search_bar()
        type(Key.DOWN)

        expected = exists(change_search_settings_pattern, 10)
        assert_true(self, expected, 'The \'Change Search Settings\' button found in the page.')

        click(change_search_settings_pattern)

        expected = exists(about_preferences_search_page_pattern, 10)
        assert_true(self, expected, 'The \'about:preferences#search\' page opened.')

        # Add a new search engine.
        for i in range(12):
            type(Key.TAB)

        if Settings.get_os() == Platform.WINDOWS or Settings.get_os() == Platform.LINUX:
            type(Key.SPACE)
            mouse.scroll(-10)
        else:
            type(Key.TAB)

        expected = exists(find_more_search_engines_pattern, 10)
        assert_true(self, expected, '\'Find more search engines\' link found.')

        click(find_more_search_engines_pattern)

        try:
            wait(find_add_ons, 10)
            logger.debug('Find add-ons field is present on the page.')
            click(find_add_ons)
        except FindError:
            raise FindError('Find add-ons field is NOT present on the page, aborting.')

        paste('startpage')

        expected = exists(add_startpage_https_privacy_search_engine_pattern, 10)
        assert_true(self, expected, '\'Startpage HTTPS Privacy Search Engine\' engine successfully found.')

        click(add_startpage_https_privacy_search_engine_pattern)

        expected = exists(add_to_firefox_pattern, 10)
        assert_true(self, expected, '\'Add to Firefox\' button found.')

        click(add_to_firefox_pattern)

        expected = exists(add_button_pattern, 10)
        assert_true(self, expected, '\'Add\' button found.')

        click(add_button_pattern)

        previous_tab()

        expected = exists(startpage_https_search_engine_pattern, 10)
        assert_true(self, expected, 'The search engine added found in the \'One-Click Search Engines\' section.')

        # Navigate to a page that could contain different search engines and can be added to Firefox.
        navigate('https://play.google.com/store')
        time.sleep(DEFAULT_UI_DELAY_LONG)

        select_search_bar()
        type(Key.DOWN)
        expected = exists(add_google_play_pattern, 10)
        assert_true(self, expected, 'The \'Add \'Google Play\' button is found in the page.')

        click(add_google_play_pattern)
        expected = exists(google_play_search_engine_pattern, 10)
        assert_true(self, expected, 'The \'Google Play\' search engine is added to Firefox.')

        # Search using the search bar, the content search field and the location bar.
        paste('test')
        time.sleep(DEFAULT_UI_DELAY)

        click(google_play_search_engine_pattern)

        expected = exists(test_search_google_play_pattern.similar(0.7), 10)
        assert_true(self, expected, 'Search performed using the search bar works properly.')

        navigate('about:newtab')

        expected = exists(google_logo_content_search_field_pattern, 10)
        assert_true(self, expected, 'Google logo from the content search found.')

        click(google_logo_content_search_field_pattern)

        paste('test')
        time.sleep(DEFAULT_UI_DELAY)

        click(google_play_search_engine_pattern)

        expected = exists(test_search_google_play_pattern, 10)
        assert_true(self, expected, 'Search performed using the content search field works properly.')

        select_location_bar()

        paste('test')
        time.sleep(DEFAULT_UI_DELAY)

        click(google_play_search_engine_pattern)

        expected = exists(test_search_google_play_pattern, 10)
        assert_true(self, expected, 'Search performed using the location bar works properly.')

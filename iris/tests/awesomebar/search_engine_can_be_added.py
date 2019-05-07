# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'This test case checks that more search engines can be added and are well displayed on one-off ' \
                    'searches bar.'
        self.test_case_id = '108261'
        self.test_suite_id = '1902'
        self.locales = ['en-US']

    def run(self):
        moz_pattern = Pattern('moz.png')
        one_click_search_engine_pattern = Pattern('search_engine.png')
        search_settings_pattern = Pattern('search_settings.png')
        amazon_one_off_button_pattern = Pattern('amazon_one_off_button.png')
        bing_one_off_button_pattern = Pattern('bing_one_off_button.png')
        duck_duck_go_one_off_button_pattern = Pattern('duck_duck_go_one_off_button.png')
        google_one_off_button_pattern = Pattern('google_one_off_button.png')
        twitter_one_off_button_pattern = Pattern('twitter_one_off_button.png')
        wikipedia_one_off_button_pattern = Pattern('wikipedia_one_off_button.png')
        google_search_engine_pattern = Pattern('google_search_engine.png')
        about_preferences_search_page_pattern = Pattern('about_preferences_search_page.png')
        default_search_engine_dropdown_pattern = Pattern('default_search_engine_dropdown.png')
        moz_search_amazon_search_engine_pattern = Pattern('moz_search_amazon_search_engine.png')
        add_startpage_https_privacy_search_engine_pattern = Pattern('add_startpage_https_privacy_search_engine.png')
        find_more_search_engines_pattern = Pattern('find_more_search_engines.png')
        add_to_firefox_pattern = Pattern('add_to_firefox.png')
        add_button_pattern = Pattern('add_button.png')
        startpage_https_search_engine_pattern = Pattern('startpage_https_search_engine.png')
        startpage_one_off_button_pattern = Pattern('startpage_one_off_button.png')
        find_add_ons_pattern = Pattern('find_add_ons.png')
        pref_default_search_engine_amazon_pattern = Pattern('pref_default_search_engine_amazon.png')

        top_two_thirds_of_screen_region = Region(0, 0, SCREEN_WIDTH, 2 * SCREEN_HEIGHT / 3)

        navigate(LocalWeb.FIREFOX_TEST_SITE)

        site_loaded = exists(LocalWeb.FIREFOX_LOGO, Settings.SITE_LOAD_TIMEOUT)
        assert_true(self, site_loaded, 'Page successfully loaded, firefox logo found.')

        select_location_bar()
        paste('moz')

        one_off_pattern_list = [moz_pattern, search_settings_pattern, amazon_one_off_button_pattern,
                               bing_one_off_button_pattern, duck_duck_go_one_off_button_pattern,
                               google_one_off_button_pattern, twitter_one_off_button_pattern,
                               wikipedia_one_off_button_pattern]

        # Deleted assert for ebay because we no longer have the ebay search engine in some locations.

        # Check that the default one-off list is displayed in the awesomebar.
        for one_search_engine in range(len(one_off_pattern_list)):
            if Settings.get_os() == Platform.MAC:
                one_off_pattern_exists = exists(one_off_pattern_list[one_search_engine].similar(0.7),
                                                Settings.FIREFOX_TIMEOUT, top_two_thirds_of_screen_region)
            else:
                one_off_pattern_exists = exists(one_off_pattern_list[one_search_engine].similar(0.9),
                                                Settings.FIREFOX_TIMEOUT, top_two_thirds_of_screen_region)
            assert_true(self, one_off_pattern_exists, 'Search engine Pattern {0} - {1} is displayed.'.format(
                one_search_engine+1, one_off_pattern_list[one_search_engine].image_name))

        click(search_settings_pattern, Settings.TINY_FIREFOX_TIMEOUT)

        search_page = exists(about_preferences_search_page_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, search_page, 'The \'about:preferences#search\' page successfully loaded.')

        search_engine_dropdown = exists(default_search_engine_dropdown_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, search_engine_dropdown, 'Default search engine dropdown found.')

        click(default_search_engine_dropdown_pattern)

        # Change the default search engine.
        amazon_search_engine = exists(pref_default_search_engine_amazon_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, amazon_search_engine, 'Amazon search engine is available.')

        click(pref_default_search_engine_amazon_pattern)

        # Check that default search engine successfully changed.
        previous_tab()

        select_location_bar()
        type(Key.DELETE)

        paste('moz')
        type(Key.SPACE)

        amazon_search_engine = exists(moz_search_amazon_search_engine_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, amazon_search_engine, 'Default search engine successfully changed.')

        # Remove the 'Google' search engine.
        next_tab()

        google_one_off_button = scroll_until_pattern_found(google_search_engine_pattern, scroll, (-25,), 20, 1)
        assert_true(self, google_one_off_button, 'Google one off search engine button is displayed.')

        google_check_box_location = find(google_search_engine_pattern)
        click(Location(google_check_box_location.x+5, google_check_box_location.y+10), 1)

        one_click_search_engine_pattern = exists(one_click_search_engine_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, one_click_search_engine_pattern, 'One-Click Search Engines section found.')

        # Check that unchecked search engine is successfully removed from the one-off searches bar.
        previous_tab()
        
        select_location_bar()
        type(Key.DELETE)

        paste('moz')
        type(Key.SPACE)

        if Settings.get_os() == Platform.WINDOWS or Settings.get_os() == Platform.LINUX:
            google_one_off_search_engine = exists(google_one_off_button_pattern, Settings.SHORT_FIREFOX_TIMEOUT)
        else:
            google_one_off_search_engine = exists(google_one_off_button_pattern.similar(0.9),
                                                  Settings.SHORT_FIREFOX_TIMEOUT)
        assert_false(self, google_one_off_search_engine, 'Unchecked search engine successfully removed from the '
                                                         'one-off searches bar.')

        # Add a new search engine.
        next_tab()

        find_more_search_button = scroll_until_pattern_found(find_more_search_engines_pattern, scroll, (-25,), 20, 1)
        assert_true(self, find_more_search_button, '\'Find more search engines\' link found.')

        click(find_more_search_engines_pattern)

        find_add_ons = exists(find_add_ons_pattern, Settings.SITE_LOAD_TIMEOUT)
        assert_true(self, find_add_ons, 'Find add-ons field is present on the page.')

        click(find_add_ons_pattern, Settings.TINY_FIREFOX_TIMEOUT)

        paste('startpage')

        startpage_search_engine = exists(add_startpage_https_privacy_search_engine_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, startpage_search_engine, '\'Startpage HTTPS Privacy Search Engine\' engine successfully '
                                                   'found.')

        click(add_startpage_https_privacy_search_engine_pattern)

        add_to_firefox_button = exists(add_to_firefox_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, add_to_firefox_button, '\'Add to Firefox\' button found.')

        click(add_to_firefox_pattern)

        add_button = exists(add_button_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, add_button, '\'Add\' button found.')

        click(add_button_pattern, 1)

        previous_tab()

        startpage_search_engine = exists(startpage_https_search_engine_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, startpage_search_engine, 'The search engine added found in the \'One-Click Search Engines\' '
                                                   'section.')

        # Perform a new search in the url bar and make sure that everything looks ok after all the above changes.
        previous_tab()

        select_location_bar()
        type(Key.DELETE)

        paste('moz')
        type(Key.SPACE)

        moz_search_amazon_search_engine = exists(moz_search_amazon_search_engine_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, moz_search_amazon_search_engine, 'Default search engine is still changed.')

        startpage_one_off_button = exists(startpage_one_off_button_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, startpage_one_off_button, 'Newly added search engine successfully found in the one-off '
                                                    'searches bar.')

        if Settings.get_os() == Platform.MAC:
            google_one_off_button = exists(google_one_off_button_pattern.similar(0.9), Settings.SHORT_FIREFOX_TIMEOUT)
        else:
            google_one_off_button = exists(google_one_off_button_pattern, Settings.SHORT_FIREFOX_TIMEOUT)
        assert_false(self, google_one_off_button, 'Unchecked search engine is still removed from the one-off searches '
                                                  'bar.')

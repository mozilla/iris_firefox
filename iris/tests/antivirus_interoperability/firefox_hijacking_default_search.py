# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Firefox hijacking - default search engine'
        self.test_case_id = '219663'
        self.test_suite_id = '3063'
        self.locales = ['en-US']

    def run(self):
        picker_pattern = Pattern('search_engines_picker.png')
        about_preferences_search_pattern = Pattern('about_preferences_search.png')
        amazon_one_click_search_pattern = Pattern('amazon_one_click_search.png')
        bing_one_click_search_pattern = Pattern('bing_one_click_search.png')
        duck_one_click_search_pattern = Pattern('duck_one_click_search.png')
        ebay_one_click_search_pattern = Pattern('ebay_one_click_search.png')
        google_one_click_search_pattern = Pattern('google_one_click_search.png')
        twitter_one_click_search_pattern = Pattern('twitter_one_click_search.png')
        google_search_engine_pattern = Pattern('google_search_engine.png')
        wiki_one_click_search_pattern = Pattern('wiki_one_click_search.png')
        bing_search_engine_pattern = Pattern('bing_search_engine.png')
        amazon_search_engine_pattern = Pattern('amazon_search_engine.png')
        duck_search_engine_pattern = Pattern('duck_search_engine.png')
        ebay_search_engine_pattern = Pattern('ebay_search_engine.png')
        twitter_search_engine_pattern = Pattern('twitter_search_engine.png')
        wiki_search_engine_pattern = Pattern('wiki_search_engine.png')

        one_click_search_engines = [google_one_click_search_pattern, bing_one_click_search_pattern,
                                    amazon_one_click_search_pattern, duck_one_click_search_pattern,
                                    ebay_one_click_search_pattern, twitter_one_click_search_pattern]

        default_search_engines = [google_search_engine_pattern, bing_search_engine_pattern,
                                  amazon_search_engine_pattern, duck_search_engine_pattern,
                                  ebay_search_engine_pattern, twitter_search_engine_pattern]

        navigate('about:preferences#search')

        about_preferences_search_opened = exists(about_preferences_search_pattern, Settings.SITE_LOAD_TIMEOUT)
        assert_true(self, about_preferences_search_opened, 'About preferences search page is successfully opened')

        picker_exists = exists(picker_pattern)
        assert_true(self, picker_exists, 'Picker displayed')

        click(picker_pattern)

        default_search_engines_displayed = exists(google_search_engine_pattern, Settings.SHORT_FIREFOX_TIMEOUT)
        assert_true(self, default_search_engines_displayed, 'Default Search Engines drop down displayed')

        default_engines_location = find(google_search_engine_pattern)
        default_search_engines_width, default_search_engines_height = google_search_engine_pattern.get_size()

        coordinate_y = default_engines_location.y

        for engine in default_search_engines:
            num = default_search_engines.index(engine) + 1
            default_search_engines_region = Region(default_engines_location.x, coordinate_y,
                                                   default_search_engines_width, default_search_engines_height)

            search_engine_exists = exists(engine, in_region=default_search_engines_region)
            assert_true(self, search_engine_exists, 'The Default search engine #' + str(num) + ' exists')

            coordinate_y += default_search_engines_height

        search_engine_list_is_default = exists(wiki_search_engine_pattern)
        assert_true(self, search_engine_list_is_default, 'The default search engine list is not changed')

        restore_firefox_focus()

        open_find()

        paste('One-click')

        one_click_search_engines_exists = exists(google_one_click_search_pattern, Settings.SHORT_FIREFOX_TIMEOUT)
        assert_true(self, one_click_search_engines_exists, 'One-click Search Engines list displayed')

        one_click_search_engines_location = find(google_one_click_search_pattern)
        one_click_search_engines_width, one_click_search_engines_height = google_one_click_search_pattern.get_size()

        coordinate_y = one_click_search_engines_location.y

        for engine in one_click_search_engines:
            num = one_click_search_engines.index(engine) + 1
            one_click_search_engines_region = Region(one_click_search_engines_location.x, coordinate_y,
                                                     one_click_search_engines_width, one_click_search_engines_height)

            search_engine_exists = exists(engine, in_region=one_click_search_engines_region)
            assert_true(self, search_engine_exists, 'The One-click search engine #' + str(num) + ' exists')

            coordinate_y += one_click_search_engines_height

        one_click_search_engine_list_is_default = exists(wiki_one_click_search_pattern)
        assert_true(self, one_click_search_engine_list_is_default, 'The default One-click search engine list '
                                                                   'is not changed')

        restart_firefox(self,
                        self.browser.path,
                        self.profile_path,
                        'about:preferences#search',
                        image=about_preferences_search_pattern
                        )

        click(picker_pattern)

        default_search_engines_displayed = exists(google_search_engine_pattern, Settings.SHORT_FIREFOX_TIMEOUT)
        assert_true(self, default_search_engines_displayed, 'Default Search Engines drop down displayed')

        default_engines_location = find(google_search_engine_pattern)
        default_search_engines_width, default_search_engines_height = google_search_engine_pattern.get_size()

        coordinate_y = default_engines_location.y

        for engine in default_search_engines:
            num = default_search_engines.index(engine) + 1
            default_search_engines_region = Region(default_engines_location.x, coordinate_y,
                                                   default_search_engines_width, default_search_engines_height)

            search_engine_exists = exists(engine, in_region=default_search_engines_region)
            assert_true(self, search_engine_exists, 'The Default search engine #' + str(num) + ' exists')

            coordinate_y += default_search_engines_height

        search_engine_list_is_default = exists(wiki_search_engine_pattern)
        assert_true(self, search_engine_list_is_default, 'The default search engine list is not changed after restart')

        restore_firefox_focus()

        open_find()

        paste('One-click')

        one_click_search_engines_exists = exists(google_one_click_search_pattern, Settings.SHORT_FIREFOX_TIMEOUT)
        assert_true(self, one_click_search_engines_exists, 'One-click Search Engines list displayed')

        one_click_search_engines_location = find(google_one_click_search_pattern)
        one_click_search_engines_width, one_click_search_engines_height = google_one_click_search_pattern.get_size()

        coordinate_y = one_click_search_engines_location.y

        for engine in one_click_search_engines:
            num = one_click_search_engines.index(engine) + 1
            one_click_search_engines_region = Region(one_click_search_engines_location.x, coordinate_y,
                                                     one_click_search_engines_width, one_click_search_engines_height)

            search_engine_exists = exists(engine, in_region=one_click_search_engines_region)
            assert_true(self, search_engine_exists, 'The One-click search engine #' + str(num) + ' exists')

            coordinate_y += one_click_search_engines_height

        one_click_search_engine_list_is_default = exists(wiki_one_click_search_pattern)
        assert_true(self, one_click_search_engine_list_is_default, 'The default One-click search engine list '
                                                                   'is not changed after restart')

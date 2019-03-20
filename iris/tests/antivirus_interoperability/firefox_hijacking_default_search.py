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
        default_search_engines_list_pattern_for_small_screens = Pattern('default_search_engines_list_small.png')
        default_search_engines_list_pattern = Pattern('default_search_engines_list.png')
        amazon_one_click_search_pattern = Pattern('amazon_one_click_search.png')
        bing_one_click_search_pattern = Pattern('bing_one_click_search.png')
        duck_one_click_search_pattern = Pattern('duck_one_click_search.png')
        ebay_one_click_search_pattern = Pattern('ebay_one_click_search.png')
        google_one_click_search_pattern = Pattern('google_one_click_search.png')
        one_click_search_pattern = Pattern('one_click_search.png')
        twitter_one_click_search_pattern = Pattern('twitter_one_click_search.png')
        wiki_one_click_search_pattern = Pattern('wiki_one_click_search.png')

        one_click_search_engines = [google_one_click_search_pattern, bing_one_click_search_pattern,
                                    amazon_one_click_search_pattern, duck_one_click_search_pattern,
                                    ebay_one_click_search_pattern, twitter_one_click_search_pattern]

        navigate('about:preferences#search')

        about_preferences_search_opened = exists(about_preferences_search_pattern, Settings.SITE_LOAD_TIMEOUT)
        assert_true(self, about_preferences_search_opened, 'About preferences search page is successfully opened')

        picker_exists = exists(picker_pattern)
        assert_true(self, picker_exists, 'Picker displayed')

        click(picker_pattern)
        
        search_engine_list_is_default = exists(default_search_engines_list_pattern)
        search_engine_list_is_default_small_screens = exists(default_search_engines_list_pattern_for_small_screens)
        assert_true(self, search_engine_list_is_default or search_engine_list_is_default_small_screens,
                    'The default search engine list is not changed')

        restore_firefox_focus()

        open_find()

        paste('One-click')

        one_click_search_engines_exists = exists(google_one_click_search_pattern, Settings.SHORT_FIREFOX_TIMEOUT)
        assert_true(self, one_click_search_engines_exists, 'one_click_search_engines_exists')

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





        # one_click_search_engine_list_is_default = exists(one_click_search_engines_pattern)
        # assert_true(self, one_click_search_engine_list_is_default, 'The default One-click search engine list '
        #                                                            'is not changed')

        restart_firefox(self,
                        self.browser.path,
                        self.profile_path,
                        'about:preferences#search',
                        image=about_preferences_search_pattern
                        )

        time.sleep(DEFAULT_UI_DELAY)

        click(picker_pattern)

        search_engine_list_is_default_with_antivirus = exists(default_search_engines_list_pattern)
        search_engine_list_is_default_small_screens_with_antivirus = \
            exists(default_search_engines_list_pattern_for_small_screens)
        assert_true(self, search_engine_list_is_default_with_antivirus or
                    search_engine_list_is_default_small_screens_with_antivirus,
                    'The default search engine list is not changed after antivirus was installed')

        restore_firefox_focus()
        open_find()
        paste('One-click')

        time.sleep(10)

        # one_click_search_engine_list_is_default_with_antivirus = exists(one_click_search_engines_pattern)
        # assert_true(self, one_click_search_engine_list_is_default_with_antivirus,
        #             'The default One-click search engine list is not changed after antivirus was installed')

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
        one_click_search_engines_pattern = Pattern('one_click_search_engines.png')

        navigate('about:preferences#search')

        about_preferences_search_opened = exists(about_preferences_search_pattern, DEFAULT_SITE_LOAD_TIMEOUT)
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

        one_click_search_engine_list_is_default = exists(one_click_search_engines_pattern)
        assert_true(self, one_click_search_engine_list_is_default, 'The default One-click search engine list '
                                                                   'is not changed')

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

        one_click_search_engine_list_is_default_with_antivirus = exists(one_click_search_engines_pattern)
        assert_true(self, one_click_search_engine_list_is_default_with_antivirus,
                    'The default One-click search engine list is not changed after antivirus was installed')

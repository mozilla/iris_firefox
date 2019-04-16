# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'This test case performs a search using one-offs while maximizing/minimizing the browser\'s window.'
        self.test_case_id = '108252'
        self.test_suite_id = '1902'
        self.locales = ['en-US']
        self.set_profile_pref({'browser.contentblocking.enabled': False})

    def run(self):
        search_settings_pattern = Pattern('search_settings.png')
        window_controls_restore_pattern = Pattern('window_controls_restore.png')
        magnifying_glass_pattern = Pattern('magnifying_glass.png')
        window_controls_maximize_pattern = Pattern('window_controls_maximize.png')
        wikipedia_one_off_button_pattern = Pattern('wikipedia_one_off_button.png')
        wikipedia_search_results_moz_pattern = Pattern('wikipedia_search_results_moz.png')
        moz_wiki_item_pattern = Pattern('moz_wiki_item.png')
        one_offs_bar_moz_pattern = Pattern('moz.png')

        top_two_thirds_of_screen = Region(0, 0, SCREEN_WIDTH, 2 * SCREEN_HEIGHT / 3)
        navigate(LocalWeb.FIREFOX_TEST_SITE)

        figefox_site_loaded = exists(LocalWeb.FIREFOX_LOGO, Settings.FIREFOX_TIMEOUT)
        assert_true(self, figefox_site_loaded, 'Page successfully loaded, firefox logo found.')

        if Settings.get_os() == Platform.WINDOWS or Settings.get_os() == Platform.LINUX:
            minimize_window()
        else:
            reset_mouse()
            window_controls_pattern = Pattern('window_controls.png')
            width, height = window_controls_pattern.get_size()
            maximize_button = window_controls_pattern.target_offset(width - 10, height / 2)

            key_down(Key.ALT)
            click(maximize_button)
            key_up(Key.ALT)

        maximize_button_exists = exists(window_controls_maximize_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, maximize_button_exists, 'Window successfully minimized.')

        top_region_location = find(window_controls_maximize_pattern)

        select_location_bar()

        paste('moz')
        type(Key.SPACE)

        one_offs_bar_exists = top_two_thirds_of_screen.exists(one_offs_bar_moz_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, one_offs_bar_exists, 'Searched string found at the bottom of the drop-down list.')

        left_bottom_search_result_location = find(one_offs_bar_moz_pattern)

        one_offs_settings = top_two_thirds_of_screen.exists(search_settings_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, one_offs_settings, 'The \'Search settings\' button is displayed in the awesome bar.')

        type(Key.ENTER)
        time.sleep(Settings.TINY_FIREFOX_TIMEOUT)

        magnifying_glass_google = top_two_thirds_of_screen.exists(magnifying_glass_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, magnifying_glass_google, 'The default search engine is \'Google\', page successfully loaded.')

        magnifying_glass_location = find(magnifying_glass_pattern)

        search_results_region = Region(left_bottom_search_result_location.x, top_region_location.y,
                                       magnifying_glass_location.x - left_bottom_search_result_location.x,
                                       (left_bottom_search_result_location.y - top_region_location.y) * 2)

        moz_word_available = exists('moz', Settings.FIREFOX_TIMEOUT, search_results_region)
        assert_true(self, moz_word_available,
                    'Searched item is successfully found in the page opened by the default search engine.')

        reset_mouse()
        maximize_window()

        if Settings.get_os() == Platform.LINUX:
            reset_mouse()

        restore_window_button = exists(window_controls_restore_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, restore_window_button, 'Window successfully maximized.')

        select_location_bar()
        paste('moz')
        type(Key.SPACE)

        one_offs_bar_moz = top_two_thirds_of_screen.exists(one_offs_bar_moz_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, one_offs_bar_moz, 'Searched string found at the bottom of the drop-down list.')

        one_offs_settings = top_two_thirds_of_screen.exists(search_settings_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, one_offs_settings, 'The \'Search settings\' button is displayed in the awesome bar.')

        hover(wikipedia_one_off_button_pattern)

        try:
            one_offs_bar = top_two_thirds_of_screen.wait_vanish(one_offs_bar_moz_pattern, Settings.FIREFOX_TIMEOUT)
            assert_true(self, one_offs_bar, 'The \'Wikipedia\' one-off button is highlighted.')
        except FindError:
            raise FindError('The \'Wikipedia\' one-off button is not highlighted.')

        click(wikipedia_one_off_button_pattern)
        time.sleep(Settings.TINY_FIREFOX_TIMEOUT)

        wikipedia_search_tab = top_two_thirds_of_screen.exists(wikipedia_search_results_moz_pattern,
                                                               Settings.SITE_LOAD_TIMEOUT)
        assert_true(self, wikipedia_search_tab, 'Wikipedia results are opened.')

        moz_wiki_item = Screen.LEFT_HALF.exists(moz_wiki_item_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, moz_wiki_item, 'Searched item is successfully found in the page opened by the wikipedia '
                                         'search engine.')

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
        window_controls_maximize_pattern = Pattern('window_controls_maximize.png')
        wikipedia_one_off_button_pattern = Pattern('wikipedia_one_off_button.png')
        wikipedia_search_results_moz_pattern = Pattern('wikipedia_search_results_moz.png')
        moz_wiki_item_pattern = Pattern('moz_wiki_item.png')
        one_offs_bar_moz_pattern = Pattern('moz.png')
        google_one_click_search_pattern = Pattern('google_one_click_search.png')

        top_two_thirds_of_screen = Region(0, 0, SCREEN_WIDTH, 2 * SCREEN_HEIGHT / 3)
        navigate(LocalWeb.FIREFOX_TEST_SITE)

        firefox_site_loaded = exists(LocalWeb.FIREFOX_LOGO, Settings.FIREFOX_TIMEOUT)
        assert_true(self, firefox_site_loaded, 'Page successfully loaded, firefox logo found.')

        if Settings.get_os() == Platform.WINDOWS or Settings.get_os() == Platform.LINUX:
            minimize_window()
        else:
            reset_mouse()
            window_controls_pattern = Pattern('window_controls.png')
            window_controls_width, window_controls_height = window_controls_pattern.get_size()
            maximize_button = window_controls_pattern.target_offset(window_controls_width - 10,
                                                                    window_controls_height / 2)

            key_down(Key.ALT)

            click(maximize_button)

            key_up(Key.ALT)

        reset_mouse()

        maximize_button_exists = exists(window_controls_maximize_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, maximize_button_exists, 'Window successfully minimized.')

        select_location_bar()

        type('moz ', interval=0.5)

        one_offs_bar_exists = top_two_thirds_of_screen.exists(one_offs_bar_moz_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, one_offs_bar_exists, 'Searched string found at the bottom of the drop-down list.')

        one_offs_settings = top_two_thirds_of_screen.exists(search_settings_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, one_offs_settings, 'The \'Search settings\' button is displayed in the awesome bar.')

        type(Key.ENTER)

        home_location = find(NavBar.HOME_BUTTON)
        home_height = NavBar.HOME_BUTTON.get_size()[1]
        tabs_region = Region(0, home_location.y-home_height * 4, SCREEN_WIDTH, home_height * 4)

        google_search_successful = tabs_region.exists(google_one_click_search_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, google_search_successful, 'The default search engine \'Google\' website with searched item is'
                                                    'loaded.')

        maximize_window()

        if Settings.get_os() == Platform.LINUX:
            reset_mouse()

        restore_window_button = exists(window_controls_restore_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, restore_window_button, 'Window successfully maximized.')

        select_location_bar()

        type('moz ', interval=0.5)

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

        wikipedia_one_off_button = top_two_thirds_of_screen.exists(wikipedia_one_off_button_pattern,
                                                                   Settings.FIREFOX_TIMEOUT)
        assert_true(self, wikipedia_one_off_button, 'Wikipedia one off button exists')

        click(wikipedia_one_off_button_pattern)

        wikipedia_search_tab = top_two_thirds_of_screen.exists(wikipedia_search_results_moz_pattern,
                                                               Settings.SITE_LOAD_TIMEOUT)
        assert_true(self, wikipedia_search_tab, 'Wikipedia results are opened.')

        moz_wiki_item = Screen.LEFT_HALF.exists(moz_wiki_item_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, moz_wiki_item, 'Searched item is successfully found in the page opened by the wikipedia '
                                         'search engine.')

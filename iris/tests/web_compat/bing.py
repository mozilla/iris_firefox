# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.assets = os.path.join(os.path.split(__file__)[0], 'assets')
        self.meta = 'Web compatibility test for bing.com'
        self.enabled = False

    def run(self):
        url = 'www.bing.com'
        search_item = 'Barack Obama'
        home_pattern = Pattern('bing_home.png')
        search_page_pattern = Pattern('bing_search.png')
        language_changed_pattern = Pattern('language_changed.png')
        page_bottom_pattern = Pattern('page_bottom.png')
        change_language_pattern = Pattern('change_language.png')
        changed_language_pattern = Pattern('changed_language.png')
        coordinates_pattern = Pattern('coordinates.png')
        languages_list_pattern = Pattern('languages_list.png')
        menu = NavBar.HAMBURGER_MENU
        save_button_pattern = Pattern('save_button.png')
        settings_pattern = Pattern('settings.png')
        switch_language_pattern = Pattern('switch_language.png')

        logger.debug('Accessing %s ...' % url)
        navigate(url)

        expected_1 = exists(home_pattern, 10)
        assert_true(self, expected_1, 'The page is successfully loaded')

        logger.debug('%s successfully loaded' % url)
        paste(search_item)
        type(Key.ENTER)

        logger.debug('Searching: %s' % search_item)

        expected_2 = exists(search_page_pattern, 10)
        assert_true(self, expected_2, 'Search results are being displayed')

        try:
            wait(coordinates_pattern, 10)
        except (FindError, ValueError):
            assert_true(self, False, 'Unable to find region marker')

        coord = find(coordinates_pattern)
        bing_menu_region = Region(coord.x, coord.y, 200, 200)

        expected_3 = bing_menu_region.exists(menu, 10)
        assert_true(self, expected_3, 'Menu can be accessed')

        bing_menu_region.click(menu)

        expected_4 = exists(settings_pattern, 10)
        assert_true(self, expected_4, 'Menu Settings can be accessed')

        click(settings_pattern)

        expected_5 = exists(change_language_pattern, 10)
        assert_true(self, expected_5, 'Language menu can be accessed')

        click(change_language_pattern)

        expected_6 = exists(languages_list_pattern, 10)
        assert_true(self, expected_6, 'Language can be changed')

        click(languages_list_pattern)

        expected_7 = exists(switch_language_pattern, 10)
        assert_true(self, expected_7, 'Changing language')

        click(switch_language_pattern)

        expected_8 = exists(changed_language_pattern, 10)
        assert_true(self, expected_8, 'Language has been changed')

        expected_9 = exists(save_button_pattern, 10)
        assert_true(self, expected_9, 'Changes can be saved')

        click(save_button_pattern)

        expected_10 = exists(language_changed_pattern, 10)
        assert_true(self, expected_10, 'Language has been successfully changed')

        page_end()

        if exists(page_bottom_pattern, 10):
            assert_true(self, True, 'Page has been scrolled down')
        else:
            logger.debug('Pop-up appeared on page. Executing another scroll down to reach the bottom of the page.')
            page_end()
            assert_true(self, exists(page_bottom_pattern, 10), 'Page has been scrolled down')

        page_home()

        expected_12 = exists(language_changed_pattern, 10)
        assert_true(self, expected_12, 'Page has been scrolled up')

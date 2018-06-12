# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.assets = os.path.join(os.path.split(__file__)[0], 'assets')
        self.meta = 'Web compatibility test for bing.com'

    def run(self):
        url = 'www.bing.com'
        search_item = 'Barack Obama'
        home = 'bing_home.png'
        search_page = 'bing_search.png'
        language_changed = 'language_changed.png'
        page_bottom = 'page_bottom.png'
        change_language = 'change_language.png'
        changed_language = 'changed_language.png'
        coordinates = 'coordinates.png'
        languages_list = 'languages_list.png'
        menu = 'menu.png'
        save_button = 'save_button.png'
        settings = 'settings.png'
        switch_language = 'switch_language.png'

        logger.debug('Accessing ' + url + '...')
        navigate(url)

        expected_1 = exists(home, 10)
        assert_true(self, expected_1, 'The page is successfully loaded')

        logger.info(url + ' successfully loaded')
        paste(search_item)
        type(Key.ENTER)

        logger.debug('Searching ' + search_item)

        expected_2 = exists(search_page, 10)
        assert_true(self, expected_2, 'Search results are being displayed')

        coord = find(coordinates)
        bing_menu_region = Region(coord.x, coord.y, 200, 200)

        expected_3 = bing_menu_region.exists(menu, 10)
        assert_true(self, expected_3, 'Menu can be accessed')

        bing_menu_region.click(menu)

        expected_4 = exists(settings, 10)
        assert_true(self, expected_4, 'Menu Settings can be accessed')

        click(settings)

        expected_5 = exists(change_language, 10)
        assert_true(self, expected_5, 'Language menu can be accessed')

        click(change_language)

        expected_6 = exists(languages_list, 10)
        assert_true(self, expected_6, 'Language can be changed')

        click(languages_list)

        expected_7 = exists(switch_language, 10)
        assert_true(self, expected_7, 'Changing language')

        click(switch_language)

        expected_8 = exists(changed_language, 10)
        assert_true(self, expected_8, 'Language has been changed')

        expected_9 = exists(save_button, 10)
        assert_true(self, expected_9, 'Changes can be saved')

        click(save_button)

        expected_10 = exists(language_changed, 10)
        assert_true(self, expected_10, 'Language has been changed successfully changed')

        page_end()

        expected_7 = exists(page_bottom, 10)
        assert_true(self, expected_7, 'Page has been scrolled down')

        page_home()

        expected_8 = exists(language_changed, 10)
        assert_true(self, expected_8, 'Page has been scrolled up')

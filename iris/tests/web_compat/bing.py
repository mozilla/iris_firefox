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
        search_field = 'search_field.png'
        language = 'language.png'
        language_changed = 'language_changed.png'
        page_bottom = 'page_bottom.png'
        bing_menu = 'bing_menu.png'
        access_language = 'access_language.png'
        save_button = 'save_button.png'

        logger.debug('Accessing ' + url + '...')
        navigate(url)

        expected_1 = exists(home, 10)
        assert_true(self, expected_1, 'The page is successfully loaded')

        logger.info(url + ' successfully loaded')
        type(search_item)
        type(Key.ENTER)

        logger.debug('Searching ' + search_item)

        expected_2 = exists(search_page, 10)
        assert_true(self, expected_2, 'Search results are being displayed')

        # I added the implementation for Mac and I tried to keep
        # the keyboard navigation in place as much as i could

        if Settings.getOS() == Platform.MAC:

            expected_button = exists(bing_menu, 10)
            assert_true(self, expected_button, 'Bing menu can be accessed')

            click(bing_menu)
            time.sleep(2)
            type(Key.TAB)
            time.sleep(1)
            type(Key.ENTER)
            time.sleep(2)
            click(access_language)
            time.sleep(3)
            type(Key.TAB)
            for i in range(2):
                type(Key.DOWN)
            time.sleep(2)
            type(Key.ENTER)
            time.sleep(2)

            expected_save_button = exists(save_button, 10)
            assert_true(self, expected_save_button, 'Changes can be saved')

            click(save_button)

            expected_3 = exists(language_changed, 10)
            assert_true(self, expected_3, 'Language has been changed successfully')

        else:

            expected_4 = exists(search_field, 10)
            assert_true(self, expected_4, 'Search field exists')

            click(search_field)
            time.sleep(2)
            for i in range(2):
                type(Key.TAB)
            time.sleep(2)
            type(Key.ENTER)
            time.sleep(2)
            type(Key.TAB)
            time.sleep(2)
            type(Key.ENTER)

            expected_5 = exists(language, 10)
            assert_true(self, expected_5, 'Language can be changed')

            click(language)
            time.sleep(3)
            type(Key.TAB)
            type(Key.DOWN)
            for i in range(7):
                type(Key.TAB)
            time.sleep(2)
            type(Key.ENTER)
            time.sleep(1)

            expected_6 = exists(language_changed, 10)
            assert_true(self, expected_6, 'Language has been changed')

        page_end()

        expected_7 = exists(page_bottom, 10)
        assert_true(self, expected_7, 'Page has been scrolled down')

        page_home()

        expected_8 = exists(language_changed, 10)
        assert_true(self, expected_8, 'Page has been scrolled up')

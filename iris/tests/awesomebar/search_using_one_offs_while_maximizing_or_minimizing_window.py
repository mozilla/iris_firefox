# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This test case performs a search using one-offs while maximizing/minimizing the browser\'s window.'

    def run(self):
        url = LocalWeb.FIREFOX_TEST_SITE
        one_off_searches_minimized_browser = 'one_off_searches_minimized_browser.png'
        one_off_searches = 'one_off_searches.png'
        search_settings = 'search_settings.png'
        window_controls_restore = 'window_controls_restore.png'
        magnifying_glass = 'magnifying_glass.png'
        window_controls_maximize = 'window_controls_maximize.png'
        wikipedia_one_off_button = 'wikipedia_one_off_button.png'
        wikipedia_search_results_moz = 'wikipedia_search_results_moz.png'
        moz = 'moz.png'

        region = Region(0, 0, SCREEN_WIDTH, 2 * SCREEN_HEIGHT / 3)

        navigate(url)

        expected = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert_true(self, expected, 'Page successfully loaded, firefox logo found.')

        if Settings.get_os() == Platform.WINDOWS or Settings.get_os() == Platform.LINUX:
            minimize_window()
        else:
            click(window_controls_restore)

        expected = exists(window_controls_maximize, 10)
        assert_true(self, expected, 'Window successfully minimized.')

        select_location_bar()
        paste('moz')

        expected = region.exists(moz, 10)
        assert_true(self, expected, 'Searched string found at the bottom of the drop-down list.')

        expected = region.exists(search_settings, 10)
        assert_true(self, expected, 'The \'Search settings\' button is displayed in the awesome bar.')

        expected = region.exists(one_off_searches_minimized_browser, 10)
        assert_true(self, expected, 'The one-off searches are displayed in the awesome bar.')

        type(Key.ENTER)
        time.sleep(DEFAULT_UI_DELAY_LONG)

        expected = region.exists(magnifying_glass, 10)
        assert_true(self, expected, 'The default search engine is \'Google\', page successfully loaded.')

        expected = region.exists('Moz', 10)
        assert_true(self, expected, 'Searched item is successfully found in the page opened by the default search '
                                    'engine.')
        maximize_window()

        if Settings.get_os() == Platform.LINUX:
            reset_mouse()

        expected = exists(window_controls_restore, 10)
        assert_true(self, expected, 'Window successfully maximized.')

        select_location_bar()
        paste('moz')

        expected = region.exists(moz, 10)
        assert_true(self, expected, 'Searched string found at the bottom of the drop-down list.')

        expected = region.exists(search_settings, 10)
        assert_true(self, expected, 'The \'Search settings\' button is displayed in the awesome bar.')

        expected = region.exists(one_off_searches, 10)
        assert_true(self, expected, 'The one-off searches are displayed in the awesome bar.')

        hover(wikipedia_one_off_button)

        try:
            expected = region.wait_vanish(moz, 10)
            assert_true(self, expected, 'The \'Wikipedia\' one-off button is highlighted.')
        except FindError:
            raise FindError('The \'Wikipedia\' one-off button is not highlighted.')

        click(wikipedia_one_off_button)
        time.sleep(DEFAULT_UI_DELAY_LONG)

        expected = region.exists(wikipedia_search_results_moz, 10)
        assert_true(self, expected, 'Wikipedia results are opened.')

        expected = exists('Moz', 10)
        assert_true(self, expected, 'Searched item is successfully found in the page opened by the wikipedia search '
                                    'engine.')

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This test case performs a search using one-offs while maximizing/minimizing the browser\'s window.'
        self.test_case_id = '108252'
        self.test_suite_id = '1902'
        self.locales = ['en-US']

    def run(self):
        url = LocalWeb.FIREFOX_TEST_SITE
        search_settings_pattern = Pattern('search_settings.png')
        window_controls_restore_pattern = Pattern('window_controls_restore.png')
        magnifying_glass_pattern = Pattern('magnifying_glass.png')
        window_controls_maximize_pattern = Pattern('window_controls_maximize.png')
        wikipedia_one_off_button_pattern = Pattern('wikipedia_one_off_button.png')
        wikipedia_search_results_moz_pattern = Pattern('wikipedia_search_results_moz.png')
        moz_pattern = Pattern('moz.png')

        left_upper_corner = Region(0, 0, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

        region = Region(0, 0, SCREEN_WIDTH, 2 * SCREEN_HEIGHT / 3)
        navigate(url)

        expected = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert_true(self, expected, 'Page successfully loaded, firefox logo found.')

        if Settings.get_os() == Platform.WINDOWS or Settings.get_os() == Platform.LINUX:
            minimize_window()
        else:
            reset_mouse()
            window_controls_pattern = Pattern('window_controls.png')
            width, height = get_image_size(window_controls_pattern)
            maximize_button = window_controls_pattern.target_offset(width - 10, height / 2)

            key_down(Key.ALT)
            click(maximize_button)
            key_up(Key.ALT)

        expected = exists(window_controls_maximize_pattern, 10)
        assert_true(self, expected, 'Window successfully minimized.')

        select_location_bar()
        paste('moz')
        type(Key.SPACE)

        expected = region.exists(moz_pattern, 10)
        assert_true(self, expected, 'Searched string found at the bottom of the drop-down list.')

        expected = region.exists(search_settings_pattern, 10)
        assert_true(self, expected, 'The \'Search settings\' button is displayed in the awesome bar.')

        type(Key.ENTER)
        time.sleep(DEFAULT_UI_DELAY_LONG)

        expected = region.exists(magnifying_glass_pattern, 10)
        assert_true(self, expected, 'The default search engine is \'Google\', page successfully loaded.')

        expected = region.exists('Moz', 10)
        assert_true(self, expected,
                    'Searched item is successfully found in the page opened by the default search engine.')

        reset_mouse()
        maximize_window()

        if Settings.get_os() == Platform.LINUX:
            reset_mouse()

        expected = exists(window_controls_restore_pattern, 10)
        assert_true(self, expected, 'Window successfully maximized.')

        select_location_bar()
        paste('moz')
        type(Key.SPACE)

        expected = region.exists(moz_pattern, 10)
        assert_true(self, expected, 'Searched string found at the bottom of the drop-down list.')

        expected = region.exists(search_settings_pattern, 10)
        assert_true(self, expected, 'The \'Search settings\' button is displayed in the awesome bar.')

        hover(wikipedia_one_off_button_pattern)

        try:
            expected = region.wait_vanish(moz_pattern, 10)
            assert_true(self, expected, 'The \'Wikipedia\' one-off button is highlighted.')
        except FindError:
            raise FindError('The \'Wikipedia\' one-off button is not highlighted.')

        click(wikipedia_one_off_button_pattern)
        time.sleep(DEFAULT_UI_DELAY_LONG)

        expected = region.exists(wikipedia_search_results_moz_pattern, 10)
        assert_true(self, expected, 'Wikipedia results are opened.')

        expected = left_upper_corner.exists('Moz', 10)
        assert_true(self, expected,
                    'Searched item is successfully found in the page opened by the wikipedia search engine.')

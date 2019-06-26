# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='This test case performs a search using one-offs while maximizing/minimizing the browser\'s '
                    'window.',
        locale=['en-US'],
        test_case_id='108252',
        test_suite_id='1902',
        preferences={'browser.contentblocking.enabled': False}
    )
    def run(self, firefox):
        url = LocalWeb.FIREFOX_TEST_SITE
        search_settings_pattern = Pattern('search_settings.png')
        window_controls_restore_pattern = Pattern('window_controls_restore.png')
        magnifying_glass_pattern = Pattern('magnifying_glass.png')
        window_controls_maximize_pattern = Pattern('window_controls_maximize.png')
        wikipedia_one_off_button_pattern = Pattern('wikipedia_one_off_button.png').similar(.7)
        wikipedia_search_results_moz_pattern = Pattern('wikipedia_search_results_moz.png')
        moz_wiki_item = Pattern('moz_wiki_item.png')
        moz_pattern = Pattern('moz.png')

        left_upper_corner = Region(0, 0, Screen().width, 2 * Screen().height / 3)

        region = Region(0, 0, Screen().width, 2 * Screen().height / 3)
        navigate(url)

        test_page_opened = exists(LocalWeb.FIREFOX_LOGO, FirefoxSettings.FIREFOX_TIMEOUT)
        assert test_page_opened, 'Page successfully loaded, firefox logo found.'

        if OSHelper.is_windows() or OSHelper.is_linux():
            minimize_window()
        else:
            mouse_reset()
            window_controls_pattern = Pattern('window_controls.png')
            width, height = window_controls_pattern.get_size()
            maximize_button = window_controls_pattern.target_offset(width - 10, height / 2)

            key_down(Key.ALT)
            click(maximize_button)
            key_up(Key.ALT)

        window_minimized = exists(window_controls_maximize_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert window_minimized, 'Window successfully minimized.'

        select_location_bar()
        paste('moz')
        type(Key.SPACE)

        moz_pattern_found = region.exists(moz_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert moz_pattern_found, 'Searched string found at the bottom of the drop-down list.'

        settings_button_displayed = region.exists(search_settings_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert settings_button_displayed, 'The \'Search settings\' button is displayed in the awesome bar.'

        type(Key.ENTER)
        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT/3)

        google_page_opened = region.exists(magnifying_glass_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert google_page_opened, 'The default search engine is \'Google\', page successfully loaded.'

        searched_item_found = region.exists('moz', FirefoxSettings.FIREFOX_TIMEOUT)
        assert searched_item_found, 'Searched item is successfully found in the page opened by the default search ' \
                                    'engine.'

        mouse_reset()
        maximize_window()

        if OSHelper.is_linux():
            mouse_reset()

        window_maximized = exists(window_controls_restore_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert window_maximized, 'Window successfully maximized.'

        select_location_bar()
        paste('moz')
        type(Key.SPACE)

        moz_pattern_found = region.exists(moz_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert moz_pattern_found, 'Searched string found at the bottom of the drop-down list.'

        settings_button_displayed = region.exists(search_settings_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert settings_button_displayed, 'The \'Search settings\' button is displayed in the awesome bar.'

        wiki_button_displayed = region.exists(wikipedia_one_off_button_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert wiki_button_displayed, 'wikipedia_one_off_button_pattern'

        hover(wikipedia_one_off_button_pattern)

        try:
            wiki_highlighted = region.wait_vanish(moz_pattern, 3)
            assert wiki_highlighted, 'The \'Wikipedia\' one-off button is highlighted.'
        except FindError:
            raise FindError('The \'Wikipedia\' one-off button is not highlighted.')

        click(wikipedia_one_off_button_pattern)
        time.sleep(Settings.DEFAULT_UI_DELAY_LONG)

        wiki_page_opened = region.exists(wikipedia_search_results_moz_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert wiki_page_opened, 'Wikipedia results are opened.'

        searched_item_found = left_upper_corner.exists(moz_wiki_item, FirefoxSettings.FIREFOX_TIMEOUT)
        assert searched_item_found, 'Searched item is successfully found in the page opened by the wikipedia search' \
                                    ' engine.'

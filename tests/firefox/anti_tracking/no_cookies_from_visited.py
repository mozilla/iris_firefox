# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Firefox can be set to no longer accept cookies from visited websites.',
        locale=['en-US'],
        test_case_id='105525',
        test_suite_id='1826',
    )
    def run(self, firefox):
        block_all_cookies_pattern = Pattern('block_all_cookies.png')
        cookies_blocking_strictness_menu_pattern = Pattern('cookies_blocking_strictness_menu.png')
        block_cookies_ticked_pattern = Pattern('block_cookies_ticked.png').similar(0.9)
        block_cookies_unticked_pattern = Pattern('block_cookies_unticked.png').similar(0.9)
        cookies_window_title_pattern = Pattern('cookies_window_title.png')
        custom_content_blocking_unticked_pattern = Pattern('custom_content_blocking_unticked.png')
        custom_content_blocking_ticked_patten = Pattern('custom_content_blocking_ticked.png').similar(0.9)
        manage_cookies_data_pattern = Pattern('manage_cookies_data.png')
        site_cookies_pattern = Pattern('site_cookies.png')
        youtube_logo_pattern = Pattern('youtube_logo.png')

        if OSHelper.is_windows():
            value = 200
        else:
            value = 10

        navigate('about:preferences#privacy')

        Mouse().move(Location(Screen.SCREEN_WIDTH // 2, Screen.SCREEN_HEIGHT // 2),
                     FirefoxSettings.TINY_FIREFOX_TIMEOUT)

        preferences_opened = scroll_until_pattern_found(custom_content_blocking_unticked_pattern, Mouse().scroll,
                                                        (0, -value), 100)
        assert preferences_opened, 'The "about:preferences#privacy" page is successfully displayed.'

        click(custom_content_blocking_unticked_pattern)

        cookies_blocking_unticked = exists(block_cookies_unticked_pattern)

        if cookies_blocking_unticked:

            click(block_cookies_unticked_pattern, 1)

        cookies_blocking_ticked = exists(block_cookies_ticked_pattern.similar(0.6))
        assert cookies_blocking_ticked, 'Ticked blocking cookies checkbox'

        strictness_menu_appeared = exists(cookies_blocking_strictness_menu_pattern)
        assert strictness_menu_appeared, 'Strictness menu appeared.'

        click(cookies_blocking_strictness_menu_pattern)

        dropdown_opened = exists(block_all_cookies_pattern)
        assert dropdown_opened, 'Strictness dropdown menu opened'

        click(block_all_cookies_pattern)

        navigate('https://www.youtube.com/')

        site_loaded = exists(youtube_logo_pattern, FirefoxSettings.HEAVY_SITE_LOAD_TIMEOUT)
        assert site_loaded, 'The website is successfully displayed.'

        navigate('about:preferences#privacy')

        preferences_opened = exists(custom_content_blocking_ticked_patten)
        assert preferences_opened, 'The "about:preferences#privacy" page is successfully displayed.'

        paste('manage data')

        cookies_data_button_located = exists(manage_cookies_data_pattern)
        assert cookies_data_button_located, '\"Manage cookies data\" button displayed.'

        click(manage_cookies_data_pattern)

        cookies_window_opened = exists(cookies_window_title_pattern)
        assert cookies_window_opened, 'Cookies window displayed.'

        paste('yout')

        site_cookies_not_saved = not exists(site_cookies_pattern)
        assert site_cookies_not_saved, 'No cookies are saved from the YouTube website.'

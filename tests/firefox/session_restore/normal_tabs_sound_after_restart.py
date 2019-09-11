# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Bug 1387976 - Normal tabs are not remembering their previously muted state and outputs sound after '\
                    'restart',
        test_case_id='178002',
        test_suite_id='68',
        locales=Locales.ENGLISH
    )
    def run(self, firefox):
        youtube_logo_inactive_tab_pattern = Pattern('youtube_logo_unactive_tab.png')
        youtube_autoplay_switch_pattern = Pattern('youtube_autoplay_switch.png')
        youtube_logo_pattern = Pattern('youtube_logo.png')
        tab_muted_pattern = Pattern('tab_muted.png')

        mute_tab = 2
        click_duration = 1

        navigate('https://www.youtube.com/watch?v=dQw4w9WgXcQ')

        youtube_page_is_downloaded = exists(youtube_autoplay_switch_pattern, FirefoxSettings.HEAVY_SITE_LOAD_TIMEOUT)
        assert youtube_page_is_downloaded, 'Youtube is properly loaded'

        tabs_region = Rectangle(0, 0, Screen.SCREEN_WIDTH//3, Screen.SCREEN_HEIGHT // 10)

        youtube_tab = exists(youtube_logo_pattern, FirefoxSettings.FIREFOX_TIMEOUT, tabs_region)
        assert youtube_tab, 'Youtube tab is available'

        youtube_logo_location = find(youtube_logo_pattern, tabs_region)
        logo_height = youtube_logo_pattern.get_size()[1]
        mute_icon_region = Rectangle(youtube_logo_location.x, youtube_logo_location.y - logo_height,
                                     Screen.SCREEN_WIDTH // 3, logo_height * 5)

        right_click(youtube_logo_pattern, click_duration)

        repeat_key_down(mute_tab)

        type(Key.ENTER)

        tab_muted_icon = exists(tab_muted_pattern, FirefoxSettings.FIREFOX_TIMEOUT, mute_icon_region)
        assert tab_muted_icon, 'Tab successfully muted.'

        firefox.restart()

        click_hamburger_menu_option('Restore')

        youtube_logo_inactive = exists(youtube_logo_inactive_tab_pattern.similar(0.6), FirefoxSettings.FIREFOX_TIMEOUT,
                                       tabs_region)
        assert youtube_logo_inactive, 'Youtube inactive tab found.'

        click(youtube_logo_inactive_tab_pattern, click_duration)

        youtube_tab = exists(youtube_logo_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT, tabs_region)
        assert youtube_tab, 'Youtube tab is active.'

        tab_muted_icon = exists(tab_muted_pattern, FirefoxSettings.FIREFOX_TIMEOUT, mute_icon_region)
        assert tab_muted_icon, 'Tab is muted after restart.'

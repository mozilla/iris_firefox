# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Bug 1387976 - Normal tabs are not remembering their previously muted state and outputs sound' \
                    ' after restart'
        self.test_case_id = '178002'
        self.test_suite_id = '68'
        self.locales = ['en-US']

    def run(self):
        youtube_logo_pattern = Pattern('youtube_logo.png')
        youtube_logo_inactive_tab_pattern = Pattern('youtube_logo_unactive_tab.png')
        youtube_autoplay_switch_pattern = Pattern('youtube_autoplay_switch.png')
        tab_muted_pattern = Pattern('tab_muted.png')
        mute_tab = 2
        click_duration = 1

        navigate('https://www.youtube.com/watch?v=dQw4w9WgXcQ')

        youtube_page_is_downloaded = exists(youtube_autoplay_switch_pattern, Settings.HEAVY_SITE_LOAD_TIMEOUT)
        assert_true(self, youtube_page_is_downloaded, 'Youtube is properly loaded')

        tabs_region = Region(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT // 10)

        youtube_tab = exists(youtube_logo_pattern, Settings.FIREFOX_TIMEOUT, tabs_region)
        assert_true(self, youtube_tab, 'Youtube tab is available')

        youtube_logo_location = find(youtube_logo_pattern, tabs_region)
        logo_height = youtube_logo_pattern.get_size()[1]
        mute_icon_region = Region(youtube_logo_location.x, youtube_logo_location.y - logo_height,
                                  SCREEN_WIDTH // 3, logo_height * 5)

        right_click(youtube_logo_pattern, click_duration)

        repeat_key_down(mute_tab)
        type(Key.ENTER)

        tab_muted_icon = exists(tab_muted_pattern, Settings.FIREFOX_TIMEOUT, mute_icon_region)
        assert_true(self, tab_muted_icon, 'Tab successfully muted.')

        restart_firefox(self, self.browser.path, self.profile_path, LocalWeb.FIREFOX_TEST_SITE,
                        image=LocalWeb.FIREFOX_LOGO)

        click_hamburger_menu_option('Restore Previous Session')

        youtube_logo_inactive = exists(youtube_logo_inactive_tab_pattern.similar(0.7), Settings.FIREFOX_TIMEOUT,
                                       tabs_region)
        assert_true(self, youtube_logo_inactive, 'Youtube inactive tab found.')

        click(youtube_logo_inactive_tab_pattern, click_duration)

        youtube_tab = exists(youtube_logo_pattern, Settings.SITE_LOAD_TIMEOUT, tabs_region)
        assert_true(self, youtube_tab, 'Youtube tab is active.')

        tab_muted_icon = exists(tab_muted_pattern, Settings.FIREFOX_TIMEOUT, mute_icon_region)
        assert_true(self, tab_muted_icon, 'Tab is muted after restart.')

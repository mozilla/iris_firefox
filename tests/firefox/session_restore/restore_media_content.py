# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Session restore with media content in the background',
        test_case_id='117045',
        test_suite_id='68',
        locales=Locales.ENGLISH,
        blocked_by={'id': '1520733', 'platform': OSPlatform.WINDOWS}
    )
    def run(self, firefox):
        speaker_icon_active_pattern = Pattern('speaker_icon_active.png').similar(0.9)
        web_developer_tools_tab_pattern = Pattern('web_developer_tools_tab.png')
        blocked_media_icon_pattern = Pattern('blocked_media_icon.png')
        second_label_pattern = Pattern('two_label.png')
        first_label_pattern = Pattern('one_label.png')
        double_icons = Pattern('double_icons.png')

        test_page_local = self.get_asset_path('index.html')
        navigate(test_page_local)

        first_label_exists = exists(first_label_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert first_label_exists, 'Page loaded'

        right_click(first_label_pattern)

        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT / 2)
        type('t')

        blocked_media_icon_exists = exists(blocked_media_icon_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert blocked_media_icon_exists, 'Blocked media tab opened'

        second_label_exists = exists(second_label_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert second_label_exists, 'Second link exists'

        right_click(second_label_pattern)

        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT / 2)
        type('t')

        new_tab()
        navigate('https://videos.cdn.mozilla.net/uploads/Web_Developer_Tools_in_Firefox_Aurora_10.webm')

        speaker_icon_active_exists = exists(speaker_icon_active_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert speaker_icon_active_exists, 'Third website loaded'

        right_click(blocked_media_icon_pattern)
        type('p')

        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)

        right_click(blocked_media_icon_pattern)
        type('p')

        blocked_media_tab_pinned_exists = exists(double_icons, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert blocked_media_tab_pinned_exists, 'Tabs pinned'

        firefox.restart()

        click_hamburger_menu_option('Restore Previous Session')

        last_tab_restored = exists(web_developer_tools_tab_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        blocked_media_icon_exists = exists(double_icons, FirefoxSettings.FIREFOX_TIMEOUT)
        no_speaker_tabs = exists(speaker_icon_active_pattern)
        restore_session_check_result = last_tab_restored and blocked_media_icon_exists and (not no_speaker_tabs)
        assert restore_session_check_result, 'Tabs are loaded and media blocked for all tabs'

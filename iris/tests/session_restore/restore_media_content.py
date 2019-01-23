# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Session restore with media content in the background'
        self.test_case_id = '117045'
        self.test_suite_id = '68'
        self.blocked_by = {'id': '1520733', 'platform': Platform.WINDOWS}
        self.locales = ['en-US']

    def run(self):
        speaker_icon_active_pattern = Pattern('speaker_icon_active.png').similar(0.9)
        blocked_media_icon_pattern = Pattern('blocked_media_icon.png')
        first_label_pattern = Pattern('one_label.png')
        second_label_pattern = Pattern('two_label.png')
        web_developer_tools_tab_pattern = Pattern('web_developer_tools_tab.png')
        double_icons = Pattern('double_icons.png')

        test_page_local = self.get_asset_path('index.html')
        navigate(test_page_local)

        first_label_exists = exists(first_label_pattern, 10)
        assert_true(self, first_label_exists, 'Page loaded')

        right_click(first_label_pattern)
        if Settings.is_linux():
            time.sleep(DEFAULT_UI_DELAY_LONG)
            type('t')
        else:
            type(Key.DOWN)
            type(Key.ENTER)

        blocked_media_icon_exists = exists(blocked_media_icon_pattern, 10)
        assert_true(self, blocked_media_icon_exists, 'Blocked media tab opened')

        second_label_exists = exists(second_label_pattern, 5)
        assert_true(self, second_label_exists, 'Second link exists')

        right_click(second_label_pattern)
        if Settings.is_linux():
            time.sleep(DEFAULT_UI_DELAY)
            type('t')
        else:
            type(Key.DOWN)
            type(Key.ENTER)

        new_tab()
        navigate('https://videos.cdn.mozilla.net/uploads/Web_Developer_Tools_in_Firefox_Aurora_10.webm')

        speaker_icon_active_exists = exists(speaker_icon_active_pattern, 10)
        assert_true(self, speaker_icon_active_exists, 'Third website loaded')

        right_click(blocked_media_icon_pattern)
        type('p')

        time.sleep(DEFAULT_UI_DELAY)

        right_click(blocked_media_icon_pattern)
        type('p')

        blocked_media_tab_pinned_exists = exists(double_icons, 5)
        assert_true(self, blocked_media_tab_pinned_exists, 'Tabs pinned')

        restart_firefox(self,
                        self.browser.path,
                        self.profile_path,
                        self.base_local_web_url)

        click_hamburger_menu_option('Restore Previous Session')

        last_tab_restored = exists(web_developer_tools_tab_pattern, 5)
        blocked_media_icon_exists = exists(double_icons, 10)
        no_speaker_tabs = exists(speaker_icon_active_pattern, 2)
        restore_session_check_result = last_tab_restored and blocked_media_icon_exists and (not no_speaker_tabs)
        assert_true(self, restore_session_check_result, 'Tabs are loaded and media blocked for all tabs')



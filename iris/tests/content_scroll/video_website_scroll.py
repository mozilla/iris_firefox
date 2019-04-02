# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Scrolling works properly on websites providing video content.'
        self.test_case_id = '4662'
        self.test_suite_id = '102'
        self.locales = ['en-US']

    def run(self):
        speaker_icon_pattern = Pattern('speaker_icon.png')
        youtube_subscribe_button_pattern = Pattern('subscribe_button.png')
        youtube_autoplay_switch_pattern = Pattern('youtube_autoplay_switch.png')

        mouse_wheel_steps = 5
        if Settings.is_windows():
            mouse_wheel_steps = 1000

        change_preference('media.autoplay.default', '0')

        navigate('https://www.youtube.com/watch?v=dQw4w9WgXcQ')

        youtube_page_is_downloaded = exists(youtube_autoplay_switch_pattern, Settings.HEAVY_SITE_LOAD_TIMEOUT)
        assert_true(self, youtube_page_is_downloaded, 'Youtube is properly loaded')

        speaker_icon_displayed = exists(speaker_icon_pattern, Settings.HEAVY_SITE_LOAD_TIMEOUT)
        assert_true(self, speaker_icon_displayed, 'The video content is playing')

        focusing_inside_the_page = find(NavBar.HOME_BUTTON).offset(300, 300)
        hover(focusing_inside_the_page)

        # Scroll by mouse wheel
        youtube_subscribe_button_displayed = scroll_until_pattern_found(youtube_subscribe_button_pattern,
                                                                        scroll, (-mouse_wheel_steps,))
        assert_true(self, youtube_subscribe_button_displayed, 'The Youtube subscribe button is displayed')

        for times_scroll_down in range(20):
            scroll(-mouse_wheel_steps)
            youtube_subscribe_button_disappeared = exists(youtube_subscribe_button_pattern)
            if not youtube_subscribe_button_disappeared:
                break

        youtube_subscribe_button_disappeared = exists(youtube_subscribe_button_pattern)
        assert_false(self, youtube_subscribe_button_disappeared, 'Successfully scrolled to comment section'
                                                                 ' by mouse scroll')

        top_of_the_page_destinated = scroll_until_pattern_found(youtube_autoplay_switch_pattern,
                                                                scroll, (mouse_wheel_steps,), 25)
        assert_true(self, top_of_the_page_destinated, 'Successfully scrolled to the top of the page by mouse scroll')

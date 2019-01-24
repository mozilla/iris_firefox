# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Scrolling works properly on websites providing video content.'
        self.test_case_id = 'C4662'
        self.test_suite_id = '102'
        self.locales = ['en-US']

    def run(self):
        show_more_button_pattern = Pattern('show_more_button.png')
        speaker_icon_pattern = Pattern('speaker_icon.png')
        youtube_info_button_pattern = Pattern('youtube_info_button.png')
        youtube_like_button_pattern = Pattern('subscribe_button.png')

        mouse_wheel_steps = 20
        if Settings.is_windows():
            mouse_wheel_steps = 1000

        navigate('https://www.youtube.com/watch?v=dQw4w9WgXcQ')

        speaker_icon_displayed = exists(speaker_icon_pattern, DEFAULT_HEAVY_SITE_LOAD_TIMEOUT)
        youtube_page_is_downloaded = exists(speaker_icon_pattern, DEFAULT_HEAVY_SITE_LOAD_TIMEOUT)
        assert_true(self, youtube_page_is_downloaded and speaker_icon_displayed, 'Youtube is properly loaded')

        focusing_inside_the_page = find(NavBar.HOME_BUTTON).offset(300, 300)
        hover(focusing_inside_the_page)

        # Scroll by mouse wheel
        for times_scroll_down in range(20):
            scroll(-mouse_wheel_steps)
            youtube_like_button_displayed = exists(youtube_like_button_pattern)
            if youtube_like_button_displayed:
                assert_true(self, youtube_like_button_displayed, 'Successfully scrolled to like button by mouse scroll')
                break

        for times_scroll_down in range(20):
            scroll(-mouse_wheel_steps)
            youtube_like_button_displayed = exists(youtube_like_button_pattern)
            if not youtube_like_button_displayed:
                assert_false(self, youtube_like_button_displayed, 'Successfully scrolled to comment section'
                                                                  ' by mouse scroll')
                break

        for times_scroll_down in range(20):
            scroll(-mouse_wheel_steps)
            show_more_button_displayed = exists(show_more_button_pattern)
            if show_more_button_displayed:
                assert_true(self, show_more_button_displayed, 'Successfully scrolled to the end of the suggestions'
                                                              ' by mouse scroll')
                break

        for times_scroll_up in range(20):
            scroll(mouse_wheel_steps)
            hover(focusing_inside_the_page)
            top_of_the_page_destinated = exists(youtube_info_button_pattern)
            if top_of_the_page_destinated:
                assert_true(self, top_of_the_page_destinated, 'Successfully scrolled to the top of the page by mouse '
                                                              'scroll')
                break

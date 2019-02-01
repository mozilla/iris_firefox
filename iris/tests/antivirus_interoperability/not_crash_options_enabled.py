# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Firefox does not crash - all antivirus options enabled.'
        self.test_case_id = '217878'
        self.test_suite_id = '3063'
        self.locales = ['en-US']

    def setup(self):
        BaseTest.setup(self)
        self.set_profile_pref({'media.autoplay.default': 0})

    def run(self):
        soundcloud_logo_pattern = Pattern('soundcloud_logo.png')
        sound_on_pattern = Pattern('sound_on.png').similar(0.9)
        youtube_autoplay_switch_pattern = Pattern('youtube_autoplay_switch.png')
        google_images_page_mark_pattern = Pattern('google_images_page_mark.png')
        show_more_results_button_pattern = Pattern('show_more_results_button.png')

        mouse_wheel_steps = 100
        if Settings.is_windows():
            mouse_wheel_steps = SCREEN_HEIGHT

        navigate('https://www.youtube.com/watch?v=dQw4w9WgXcQ')

        youtube_page_is_downloaded = exists(youtube_autoplay_switch_pattern, DEFAULT_HEAVY_SITE_LOAD_TIMEOUT)
        assert_true(self, youtube_page_is_downloaded, 'Youtube is properly loaded')

        sound_video_played = exists(sound_on_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, sound_video_played, 'The video is properly loaded and displayed.')

        navigate('https://soundcloud.com/')

        soundcloud_logo_exists = exists(soundcloud_logo_pattern, DEFAULT_FIREFOX_TIMEOUT*10)
        assert_true(self, soundcloud_logo_exists, 'Soundcloud is properly loaded')

        type(Key.SPACE)

        sound_on_exists = exists(sound_on_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, sound_on_exists, 'The sound is properly loaded and played.')

        navigate('https://images.google.com/?gws_rd=ssl&hl=en')

        google_images_page_opened = exists(google_images_page_mark_pattern, 20)
        assert_true(self, google_images_page_opened, 'Google images site is properly loaded')

        paste('cute kittens:3')
        type(Key.ENTER)

        mouse_move(google_images_page_mark_pattern)

        show_more_results_button_exists = scroll_until_pattern_found(show_more_results_button_pattern, scroll,
                                                                     (-mouse_wheel_steps,), 100, DEFAULT_UI_DELAY)
        assert_true(self, show_more_results_button_exists, 'The images are properly displayed.')






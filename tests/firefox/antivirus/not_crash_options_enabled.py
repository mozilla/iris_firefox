# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Firefox does not crash - all antivirus options enabled.',
        locale=['en-US'],
        test_case_id='217878',
        test_suite_id='3063',
        preferences={'media.autoplay.default': 0}
    )
    def run(self, firefox):
        soundcloud_logo_pattern = Pattern('soundcloud_logo.png')
        sound_on_pattern = Pattern('sound_on.png').similar(0.9)
        youtube_autoplay_switch_pattern = Pattern('youtube_autoplay_switch.png')
        google_images_page_mark_pattern = Pattern('google_images_page_mark.png')
        show_more_results_button_pattern = Pattern('show_more_results_button.png')

        mouse_wheel_steps = 100
        if OSHelper.is_windows():
            mouse_wheel_steps = Screen.SCREEN_HEIGHT

        navigate('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
        assert exists(youtube_autoplay_switch_pattern, Settings.DEFAULT_HEAVY_SITE_LOAD_TIMEOUT), \
            'Youtube is properly loaded.'
        assert exists(sound_on_pattern, 10), 'The video is properly loaded and displayed.'

        navigate('https://soundcloud.com/martycanfly-1/never-gonna-give-you-up-rick')
        assert exists(soundcloud_logo_pattern, 100), 'Soundcloud is properly loaded.'

        assert exists(sound_on_pattern, 10), 'The sound is properly loaded and played.'

        navigate('https://images.google.com/?gws_rd=ssl&hl=en')
        assert exists(google_images_page_mark_pattern, 20), 'Google images site is properly loaded.'

        paste('cute kittens:3')
        type(Key.ENTER)

        hover(google_images_page_mark_pattern)

        assert scroll_until_pattern_found(show_more_results_button_pattern, scroll_down, (mouse_wheel_steps,), 100,
                                          timeout=Settings.DEFAULT_UI_DELAY), 'The images are properly displayed.'

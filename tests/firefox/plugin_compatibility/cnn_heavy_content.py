# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='"CNN" heavy content website is properly loaded and works as intended',
        locale=['en-US'],
        test_case_id='125534',
        test_suite_id='2074'
    )
    def run(self, firefox):
        new_private_browsing_tab_pattern = PrivateWindow.private_window_pattern
        speaker_icon_pattern = Pattern('speaker_icon.png')
        play_icon_pattern = Pattern('play_icon.png').similar(.75)
        related_video_pattern = Pattern('related_video.png')
        north_text_mark_pattern = Pattern('north_text_mark.png')
        cnn_weather_page_tab_pattern = Pattern('cnn_logo_tab.png')

        home_width, home_height = NavBar.HOME_BUTTON.get_size()
        tabs_region = Region(0, 0, Screen.SCREEN_WIDTH/2, home_height * 4)

        change_preference('media.autoplay.default', '0')

        new_private_window()

        private_window_opened = exists(new_private_browsing_tab_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert private_window_opened is True, 'A new private window is successfully opened'

        navigate('http://www.cnn.com/2016/10/10/us/weather-matthew/index.html')

        cnn_weather_page_loaded = exists(cnn_weather_page_tab_pattern, FirefoxSettings.HEAVY_SITE_LOAD_TIMEOUT,
                                         tabs_region)
        assert cnn_weather_page_loaded is True, 'The specified website is successfully loaded.'

        video_playing = exists(speaker_icon_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert video_playing is True, 'The video is playing and the speaker icon is displayed'

        first_video_centred = scroll_until_pattern_found(north_text_mark_pattern, type, (Key.DOWN,), 20)
        assert first_video_centred is True, 'First video is centred among the page'

        click(north_text_mark_pattern.target_offset(0, -100))

        try:
            speaker_icon_vanished = wait_vanish(speaker_icon_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT, tabs_region)
            play_icon_appeared = exists(play_icon_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
            assert (speaker_icon_vanished and play_icon_appeared) is True, 'Video is stopped'
        except FindError:
            raise FindError('Video is not stopped')

        another_video_exists = scroll_until_pattern_found(related_video_pattern, page_down, (None,), 20)
        assert another_video_exists is True, 'Another video is displayed'

        click(related_video_pattern)

        related_video_playing = exists(speaker_icon_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT, tabs_region)
        assert related_video_playing is True, 'The video is playing and there is no browser crashes'

        close_window()

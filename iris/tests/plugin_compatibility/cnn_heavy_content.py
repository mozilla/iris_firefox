from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = '"CNN" heavy content website is properly loaded and works as intended'
        self.test_case_id = '125534'
        self.test_suite_id = '2074'
        self.locales = ['en-US']

    def run(self):
        new_private_browsing_tab_pattern = PrivateWindow.private_window_pattern
        speaker_icon_pattern = Pattern('speaker_icon.png')
        play_icon_pattern = Pattern('play_icon.png').similar(.75)
        related_video_pattern = Pattern('related_video.png')
        north_text_mark_pattern = Pattern('north_text_mark.png')
        cnn_weather_page_tab_pattern = Pattern('cnn_logo_tab.png')

        home_width, home_height = NavBar.HOME_BUTTON.get_size()
        tabs_region = Region(0, 0, SCREEN_WIDTH/2, home_height * 4)

        change_preference('media.autoplay.default', '0')

        new_private_window()

        private_window_opened = exists(new_private_browsing_tab_pattern, Settings.SITE_LOAD_TIMEOUT)
        assert_true(self, private_window_opened, 'A new private window is successfully opened')

        navigate('http://www.cnn.com/2016/10/10/us/weather-matthew/index.html')

        cnn_weather_page_loaded = exists(cnn_weather_page_tab_pattern, Settings.HEAVY_SITE_LOAD_TIMEOUT)
        assert_true(self, cnn_weather_page_loaded, 'The specified website is successfully loaded.')

        video_playing = exists(speaker_icon_pattern, Settings.SITE_LOAD_TIMEOUT, tabs_region)
        assert_true(self, video_playing, 'The video is playing and the speaker icon is displayed')

        first_video_centred = scroll_until_pattern_found(north_text_mark_pattern, type, (Key.DOWN,), 20)
        assert_true(self, first_video_centred, 'First video is centred among the page')

        video_window = find(north_text_mark_pattern).above(100)

        click(video_window)

        try:
            speaker_icon_vanished = wait_vanish(speaker_icon_pattern, Settings.SITE_LOAD_TIMEOUT, tabs_region)
            play_icon_appeared = exists(play_icon_pattern, Settings.SITE_LOAD_TIMEOUT)
            assert_true(self, speaker_icon_vanished and play_icon_appeared, 'Video is stopped')
        except FindError:
            raise FindError('Video is not stopped')

        another_video_exists = scroll_until_pattern_found(related_video_pattern, page_down, (None,), 20)
        assert_true(self, another_video_exists, 'Another video is displayed')

        click(related_video_pattern)

        related_video_playing = exists(speaker_icon_pattern, Settings.SITE_LOAD_TIMEOUT, tabs_region)
        assert_true(self, related_video_playing, 'The video is playing and there is no browser crashes')

        close_window()

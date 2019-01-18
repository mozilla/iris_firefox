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
        cnn_page_downloaded_pattern = Pattern('cnn_page_downloaded.png')
        speaker_icon_pattern = Pattern('speaker_icon.png')
        play_icon_pattern = Pattern('play_icon.png').similar(0.75)
        related_video_pattern = Pattern('related_video.png')
        share_button_pattern = Pattern('share_button.png')

        new_private_window()

        private_window_opened = exists(new_private_browsing_tab_pattern, 20)
        assert_true(self, private_window_opened, 'A new private window is successfully opened')

        navigate('http://www.cnn.com/2016/10/10/us/weather-matthew/index.html')

        cnn_weather_page_loaded = exists(cnn_page_downloaded_pattern, 100)
        assert_true(self, cnn_weather_page_loaded, 'The specified website is successfully loaded.')

        video_playing = exists(speaker_icon_pattern, 100)
        assert_true(self, video_playing, 'The video is playing and the speaker icon is displayed')

        share_button_exists = exists(share_button_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, share_button_exists, 'Share button displayed.')

        share_button_location = find(share_button_pattern)
        video_window = Location.offset(share_button_location, -350, 250)

        click(video_window)

        try:
            speaker_icon_vanished = wait_vanish(speaker_icon_pattern, 20)
            play_icon_appeared = exists(play_icon_pattern, 20)
            assert_true(self, speaker_icon_vanished and play_icon_appeared, 'Video is stopped')
        except FindError:
            raise FindError('Video is not stopped')

        for page_down_pressing in range(5):
            page_down()
            another_video_exists = exists(related_video_pattern)
            if another_video_exists:
                break

        another_video_exists = exists(related_video_pattern)
        assert_true(self, another_video_exists, 'The video is playing and the speaker icon is displayed')

        click(related_video_pattern)

        related_video_playing = exists(speaker_icon_pattern, 100)
        assert_true(self, related_video_playing, 'The video is playing and there is no browser crashes')

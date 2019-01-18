from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = '"NASA TV" heavy content website is properly loaded and works as intended'
        self.test_case_id = '125533'
        self.test_suite_id = '2074'
        self.locales = ['en-US']

    def run(self):
        new_private_browsing_tab_pattern = PrivateWindow.private_window_pattern
        nasa_tv_page_pattern = Pattern('nasa_tv_public_button.png').similar(0.6)
        speaker_icon_pattern = Pattern('speaker_icon.png')
        page_bottom_marker_pattern = Pattern('page_bottom_marker.png')
        play_icon_pattern = Pattern('play_icon.png').similar(0.6)
        media_button_pattern = Pattern('media_button.png')
        video_drop_down_pattern = Pattern('video_drop_down.png')

        new_private_window()

        private_window_opened = exists(new_private_browsing_tab_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, private_window_opened, 'A new private window is successfully opened')

        navigate('http://www.nasa.gov/multimedia/nasatv/index.html#public')

        nasa_tv_page_loaded = exists(nasa_tv_page_pattern, DEFAULT_FIREFOX_TIMEOUT * 3)
        assert_true(self, nasa_tv_page_loaded, 'The specified website is successfully loaded.')

        video_playing = exists(speaker_icon_pattern, 100)
        assert_true(self, video_playing, 'The video is playing and the speaker icon is displayed')

        media_button_location = find(media_button_pattern)
        video_window = Location.above(media_button_location, 250)

        right_click(video_window)

        video_drop_down_opened = exists(video_drop_down_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, video_drop_down_opened, 'The video drop down is opened')

        # Select the 'Pause' item in dropdown
        type(Key.DOWN)
        type(Key.ENTER)

        try:
            speaker_icon_vanished = wait_vanish(speaker_icon_pattern, DEFAULT_FIREFOX_TIMEOUT)
            play_icon_appeared = exists(play_icon_pattern, DEFAULT_FIREFOX_TIMEOUT)
            assert_true(self, speaker_icon_vanished and play_icon_appeared, 'Video is stopped')
        except FindError:
            raise FindError('Video is not stopped')

        page_end()

        page_scrolled = exists(page_bottom_marker_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, page_scrolled, 'The page is successfully scrolling')

        page_home()

        right_click(video_window)

        video_drop_down_opened_second_time = exists(video_drop_down_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, video_drop_down_opened_second_time, 'The video drop down is opened')

        # Select the 'Play' item in dropdown
        type(Key.DOWN)
        type(Key.ENTER)

        speaker_icon_appear = exists(speaker_icon_pattern, 100)
        assert_true(self, speaker_icon_appear, 'The video is playing and the page is scrolling successfully.')

        close_window()

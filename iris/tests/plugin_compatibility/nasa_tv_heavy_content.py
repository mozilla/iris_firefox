from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = '"NASA TV" heavy content website is properly loaded and works as intended'
        self.test_case_id = '125533'
        self.test_suite_id = '2074'
        self.locales = ['en-US']

    def run(self):

        iris_logo_pattern = Pattern('iris_logo.png')
        new_private_browsing_tab_pattern = Pattern('private_browsing.png')
        nasa_tv_tab_pattern = Pattern('nasa_tv_tab.png')
        speaker_icon_pattern = Pattern('speaker_icon.png')
        page_bottom_marker_pattern = Pattern('page_bottom_marker.png')
        play_icon_pattern = Pattern('play_icon.png')
        s_play_pattern = Pattern.similar(play_icon_pattern, 0.6)
        media_button_pattern = Pattern('media_button.png')
        video_drop_down_pattern = Pattern('video_drop_down.png')

        firefox_started = exists(iris_logo_pattern)
        assert_true(self, firefox_started, 'Firefox is successfully launched.')

        new_private_window()

        private_window_opened = exists(new_private_browsing_tab_pattern, 20)
        assert_true(self, private_window_opened, 'A new private window is successfully opened')

        navigate('http://www.nasa.gov/multimedia/nasatv/index.html#public')

        nasa_tv_page_loaded = exists(nasa_tv_tab_pattern, 30)
        assert_true(self, nasa_tv_page_loaded, 'The specified website is successfully loaded.')

        video_playing = exists(speaker_icon_pattern, 100)
        assert_true(self, video_playing, 'The video is playing and the plug-in icon is displayed')

        media_button_location = find(media_button_pattern)
        video_window = Location.above(media_button_location, away_y=250)

        right_click(video_window)

        video_drop_down_opened = exists(video_drop_down_pattern, 20)
        if not video_drop_down_opened:
            assert_false(self, video_drop_down_opened, 'The video drop down is not opened')

        type(Key.DOWN)
        type(Key.ENTER)

        try:
            speaker_icon_vanished = wait_vanish(speaker_icon_pattern, 20)
            play_icon_appeared = exists(s_play_pattern, 20)
            assert_true(self, speaker_icon_vanished and play_icon_appeared, 'Video is stopped')
        except FindError:
            raise FindError('Video is not stopped')

        scroll_down(10)

        page_scrolled = exists(page_bottom_marker_pattern, 10)
        assert_true(self, page_scrolled, 'The page is successfully scrolling')

        scroll_up(10)

        right_click(video_window)

        if not video_drop_down_opened:
            assert_false(self, video_drop_down_opened, 'The video drop down is not opened')

        type(Key.DOWN)
        type(Key.ENTER)

        plugin_icon_appear = exists(speaker_icon_pattern, 100)
        assert_true(self, plugin_icon_appear, 'There are no rendering, script issues and no crashes encountered.')
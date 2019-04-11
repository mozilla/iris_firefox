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

        home_width, home_height = NavBar.HOME_BUTTON.get_size()
        tabs_region = Region(0, 0, SCREEN_WIDTH/2, home_height * 4)

        change_preference('media.autoplay.default', '0')

        new_private_window()

        private_window_opened = exists(new_private_browsing_tab_pattern, Settings.SITE_LOAD_TIMEOUT)
        assert_true(self, private_window_opened, 'A new private window is successfully opened')

        navigate('http://www.nasa.gov/multimedia/nasatv/index.html#public')

        nasa_tv_page_loaded = exists(nasa_tv_page_pattern, Settings.HEAVY_SITE_LOAD_TIMEOUT)
        assert_true(self, nasa_tv_page_loaded, 'The specified website is successfully loaded.')

        video_playing = exists(speaker_icon_pattern, Settings.SITE_LOAD_TIMEOUT, tabs_region)
        assert_true(self, video_playing, 'The video is playing and the speaker icon is displayed')

        media_button_location = find(media_button_pattern)
        video_window = Location.above(media_button_location, 250)

        click(video_window)

        try:
            speaker_icon_vanished = wait_vanish(speaker_icon_pattern, Settings.SITE_LOAD_TIMEOUT, tabs_region)
            play_icon_appeared = exists(play_icon_pattern, Settings.SITE_LOAD_TIMEOUT)
            assert_true(self, speaker_icon_vanished and play_icon_appeared, 'Video is stopped')
        except FindError:
            raise FindError('Video is not stopped')

        page_end()

        page_scrolled = exists(page_bottom_marker_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, page_scrolled, 'The page is successfully scrolling')

        page_home()

        click(video_window)

        speaker_icon_appear = exists(speaker_icon_pattern, Settings.SITE_LOAD_TIMEOUT, tabs_region)
        assert_true(self, speaker_icon_appear, 'The video is playing and the page is scrolling successfully.')

        close_window()

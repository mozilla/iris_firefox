# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='"NASA TV" heavy content website is properly loaded and works as intended',
        locale=['en-US'],
        test_case_id='125533',
        test_suite_id='2074'
    )
    def run(self, firefox):
        new_private_browsing_tab_pattern = PrivateWindow.private_window_pattern
        nasa_tv_page_pattern = Pattern('nasa_tv_public_button.png').similar(0.6)
        speaker_icon_pattern = Pattern('speaker_icon.png')
        page_bottom_marker_pattern = Pattern('page_bottom_marker.png')
        play_icon_pattern = Pattern('play_icon.png').similar(0.6)
        media_button_pattern = Pattern('media_button.png')

        home_width, home_height = NavBar.HOME_BUTTON.get_size()
        tabs_region = Rectangle(0, 0, Screen.SCREEN_WIDTH/2, home_height * 4)

        change_preference('media.autoplay.default', '0')

        new_private_window()

        private_window_opened = exists(new_private_browsing_tab_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert private_window_opened is True, 'A new private window is successfully opened'

        navigate('http://www.nasa.gov/multimedia/nasatv/index.html#public')

        nasa_tv_page_loaded = exists(nasa_tv_page_pattern, FirefoxSettings.HEAVY_SITE_LOAD_TIMEOUT)
        assert nasa_tv_page_loaded is True, 'The specified website is successfully loaded.'

        video_playing = exists(speaker_icon_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT, tabs_region)
        assert video_playing is True, 'The video is playing and the speaker icon is displayed'

        click(media_button_pattern.target_offset(0, -250))

        try:
            speaker_icon_vanished = wait_vanish(speaker_icon_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT, tabs_region)
            play_icon_appeared = exists(play_icon_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
            assert (speaker_icon_vanished and play_icon_appeared) is True, 'Video is stopped'
        except FindError:
            raise FindError('Video is not stopped')

        page_end()

        page_scrolled = exists(page_bottom_marker_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert page_scrolled is True, 'The page is successfully scrolling'

        page_home()

        click(media_button_pattern.target_offset(0, -250))

        speaker_icon_appear = exists(speaker_icon_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT, tabs_region)
        assert speaker_icon_appear is True, 'The video is playing and the page is scrolling successfully.'

        close_window()

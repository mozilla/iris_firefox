# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Scrolling works properly on websites providing video content.',
        test_case_id='4662',
        test_suite_id='102',
        locale=['en-US'],
    )
    def run(self, firefox):
        speaker_icon_pattern = Pattern('speaker_icon.png')
        youtube_subscribe_button_pattern = Pattern('subscribe_button.png')
        youtube_autoplay_switch_pattern = Pattern('youtube_autoplay_switch.png')

        mouse_wheel_steps = 100
        if OSHelper.is_windows():
            mouse_wheel_steps = 1000

        change_preference('media.autoplay.default', '0')

        navigate('https://www.youtube.com/watch?v=dQw4w9WgXcQ')

        youtube_page_is_downloaded = exists(youtube_autoplay_switch_pattern, FirefoxSettings.HEAVY_SITE_LOAD_TIMEOUT)
        assert youtube_page_is_downloaded is True, 'Youtube is properly loaded'

        speaker_icon_displayed = exists(speaker_icon_pattern, FirefoxSettings.HEAVY_SITE_LOAD_TIMEOUT)
        assert speaker_icon_displayed is True, 'The video content is playing'

        focusing_inside_the_page = find(NavBar.HOME_BUTTON).offset(300, 300)
        hover(focusing_inside_the_page)

        # Scroll by mouse wheel
        youtube_subscribe_button_displayed = scroll_until_pattern_found(youtube_subscribe_button_pattern,
                                                                        Mouse().scroll, (None, -mouse_wheel_steps,))
        assert youtube_subscribe_button_displayed is True, 'The Youtube subscribe button is displayed'

        for times_scroll_down in range(20):
            Mouse().scroll(None, -mouse_wheel_steps)
            youtube_subscribe_button_disappeared = exists(youtube_subscribe_button_pattern)
            if not youtube_subscribe_button_disappeared:
                break

        youtube_subscribe_button_disappeared = exists(youtube_subscribe_button_pattern)
        assert youtube_subscribe_button_disappeared is False, 'Successfully scrolled to comment section by mouse scroll'

        top_of_the_page_destinated = scroll_until_pattern_found(youtube_autoplay_switch_pattern,
                                                                Mouse().scroll, (None, mouse_wheel_steps,), 25)
        assert top_of_the_page_destinated is True, 'Successfully scrolled to the top of the page by mouse scroll'

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Unit tests for Settings Class'
    )
    def run(self, firefox):
        url = 'about:home'
        youtube_top_site_image = Pattern('youtube_top_site.png')
        navigate(url)

        # Settings.wait_scan_rate

        default_wait_scan_rate = Settings.wait_scan_rate
        assert Settings.DEFAULT_WAIT_SCAN_RATE == default_wait_scan_rate, \
            'Default wait_scan_rate should be equal to {}'.format(Settings.DEFAULT_WAIT_SCAN_RATE)

        updated_wait_scan_rate = 5
        Settings.wait_scan_rate = updated_wait_scan_rate
        assert Settings.wait_scan_rate == updated_wait_scan_rate, \
            'Updated value for wait_scan_rate should be equal to {}'.format(updated_wait_scan_rate)

        Settings.wait_scan_rate = Settings.DEFAULT_WAIT_SCAN_RATE

        # Settings.type_delay

        default_type_delay = Settings.type_delay
        assert Settings.DEFAULT_TYPE_DELAY == default_type_delay, 'Default type_delay should be 0'

        Settings.type_delay = 2
        assert Settings.type_delay == 1, 'type_delay greater than 1 is defaulted to 1'
        type('Test')
        assert Settings.type_delay == 0, 'type_delay should be defaulted to 0 after type action'

        updated_type_delay = 0.125
        Settings.type_delay = updated_type_delay
        assert updated_type_delay == Settings.type_delay, \
            'Updated value for type_delay should be equal to {}'.format(updated_type_delay)

        Settings.type_delay = Settings.DEFAULT_TYPE_DELAY

        # Settings.move_mouse_delay

        default_move_mouse_delay = Settings.move_mouse_delay
        assert Settings.DEFAULT_MOVE_MOUSE_DELAY == default_move_mouse_delay,\
            'Default move_mouse_delay should be equal to {}'.format(Settings.DEFAULT_MOVE_MOUSE_DELAY)
        updated_move_mouse_delay = 1
        Settings.move_mouse_delay = updated_move_mouse_delay
        assert Settings.move_mouse_delay == updated_move_mouse_delay, \
            'Updated value for move_mouse_delay should be {}'.format(updated_move_mouse_delay)

        Settings.move_mouse_delay = Settings.DEFAULT_MOVE_MOUSE_DELAY

        # Settings.click_delay

        default_click_delay = Settings.click_delay
        assert Settings.DEFAULT_CLICK_DELAY == default_click_delay, \
            'Default click_delay should be equal to {}'.format(Settings.DEFAULT_CLICK_DELAY)

        Settings.click_delay = 2
        assert Settings.click_delay == 1, 'click_delay greater than 1 is defaulted to 1'

        updated_click_delay = 0.5
        Settings.click_delay = updated_click_delay
        assert updated_click_delay == Settings.click_delay, \
            'Updated value for click_delay should be equal to {}'.format(updated_click_delay)

        Settings.click_delay = Settings.DEFAULT_CLICK_DELAY

        # Settings.min_similarity

        default_min_similarity = Settings.min_similarity
        assert Settings.DEFAULT_MIN_SIMILARITY == default_min_similarity, \
            'Default min_similarity should be equal to {}'.format(Settings.DEFAULT_MIN_SIMILARITY)
        updated_min_similarity = 0.5
        Settings.min_similarity = updated_min_similarity
        assert Settings.min_similarity == updated_min_similarity, \
            'Updated value for min_similarity should be {}'.format(updated_min_similarity)

        Settings.min_similarity = 2
        assert Settings.min_similarity == 1, 'min_similarity greater than 1 is defaulted to 1'

        Settings.min_similarity = Settings.DEFAULT_MIN_SIMILARITY

        # Settings.auto_wait_timeout

        default_auto_wait_timeout = Settings.DEFAULT_AUTO_WAIT_TIMEOUT
        assert Settings.DEFAULT_AUTO_WAIT_TIMEOUT == default_auto_wait_timeout, \
            'Default auto_wait_timeout should be equal to {}'.format(Settings.DEFAULT_AUTO_WAIT_TIMEOUT)

        updated_auto_wait_timeout = 3
        Settings.auto_wait_timeout = updated_auto_wait_timeout
        assert Settings.auto_wait_timeout == updated_auto_wait_timeout, \
            'Updated value for auto_wait_timeout should be {}'.format(updated_auto_wait_timeout)

        Settings.auto_wait_timeout = Settings.DEFAULT_AUTO_WAIT_TIMEOUT

        # Settings.delay_before_mouse_down
        # Settings.delay_before_drag
        # Settings.delay_before_drop

        start_location = Location(100, 100)
        end_location = Location(200, 200)

        Settings.delay_before_mouse_down = 1
        Settings.delay_before_drag = 1
        Settings.delay_before_drop = 1
        Settings.move_mouse_delay = 3

        start_time = time.time()
        Mouse().drag_and_drop(start_location, end_location)
        end_time = time.time()

        total_duration = (Settings.delay_before_mouse_down + Settings.delay_before_drag + Settings.delay_before_drop +
                          Settings.move_mouse_delay)

        expected_duration = end_time - start_time >= total_duration
        assert expected_duration, \
            'Total duration for dragDrop should be equal or greater than {}seconds'.format(total_duration)

        Settings.delay_before_mouse_down = Settings.DEFAULT_DELAY_BEFORE_MOUSE_DOWN
        Settings.delay_before_drag = Settings.DEFAULT_DELAY_BEFORE_DRAG
        Settings.delay_before_drop = Settings.DEFAULT_DELAY_BEFORE_DROP
        Settings.move_mouse_delay = Settings.DEFAULT_MOVE_MOUSE_DELAY

        # Settings.slow_motion_delay

        default_slow_motion_delay = Settings.slow_motion_delay
        assert Settings.DEFAULT_SLOW_MOTION_DELAY == default_slow_motion_delay, \
            'Default slow_motion_delay should be equal to {}'.format(Settings.DEFAULT_SLOW_MOTION_DELAY)
        updated_slow_motion_delay = 3
        Settings.slow_motion_delay = updated_slow_motion_delay
        assert Settings.slow_motion_delay == updated_slow_motion_delay, \
            'Updated value for slow_motion_delay should be {}'.format(updated_slow_motion_delay)

        Settings.slow_motion_delay = Settings.DEFAULT_SLOW_MOTION_DELAY

        # Settings.observe_scan_rate

        default_observe_scan_rate = Settings.observe_scan_rate
        assert Settings.DEFAULT_OBSERVE_SCAN_RATE == default_observe_scan_rate, \
            'Default observe_scan_rate should be equal to {}'.format(Settings.DEFAULT_OBSERVE_SCAN_RATE)
        updated_observe_scan_rate = 5
        Settings.observe_scan_rate = updated_observe_scan_rate
        assert Settings.observe_scan_rate == updated_observe_scan_rate, \
            'Updated value for observe_scan_rate should be {}'.format(updated_observe_scan_rate)

        Settings.observe_scan_rate = Settings.DEFAULT_OBSERVE_SCAN_RATE

        # Settings.observe_min_changed_pixels

        default_observe_min_changed_pixels = Settings.observe_min_changed_pixels
        assert Settings.DEFAULT_OBSERVE_MIN_CHANGED_PIXELS == default_observe_min_changed_pixels, \
            'Default observe_min_changed_pixels should be equal to {}'.format(
                Settings.DEFAULT_OBSERVE_MIN_CHANGED_PIXELS)

        updated_observe_min_changed_pixels = 60
        Settings.observe_min_changed_pixels = updated_observe_min_changed_pixels
        assert Settings.observe_min_changed_pixels == updated_observe_min_changed_pixels, \
            'Updated value for observe_min_changed_pixels should be {}'.format(updated_observe_min_changed_pixels)

        Settings.observe_min_changed_pixels = Settings.DEFAULT_OBSERVE_MIN_CHANGED_PIXELS

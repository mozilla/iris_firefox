# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'Unit tests for Settings Class'

    def run(self):
        url = 'about:home'
        youtube_top_site_image = 'youtube_top_site.png'
        navigate(url)

        # Settings.WaitScanRate

        default_wait_scan_rate = Settings.WaitScanRate
        assert_equal(self, DEFAULT_WAIT_SCAN_RATE, default_wait_scan_rate, 'Default WaitScanRate should be equal to %s'
                     % str(DEFAULT_WAIT_SCAN_RATE))

        updated_wait_scan_rate = 5
        Settings.WaitScanRate = updated_wait_scan_rate
        assert_equal(self, Settings.WaitScanRate, updated_wait_scan_rate, 'Updated value for WaitScanRate should be '
                                                                          'equal to %s' % str(updated_wait_scan_rate))

        Settings.WaitScanRate = DEFAULT_WAIT_SCAN_RATE

        # Settings.TypeDelay

        default_type_delay = Settings.TypeDelay
        assert_equal(self, DEFAULT_TYPE_DELAY, default_type_delay, 'Default TypeDelay should be 0')

        Settings.TypeDelay = 2
        assert_equal(self, 1, Settings.TypeDelay, 'TypeDelay greater than 1 is defaulted to 1')
        type('Test')
        assert_equal(self, 0, Settings.TypeDelay, 'TypeDelay should be defaulted to 0 after type action')

        updated_type_delay = 0.125
        Settings.TypeDelay = updated_type_delay
        assert_equal(self, updated_type_delay, Settings.TypeDelay, 'Updated value for TypeDelay should be equal to %s'
                     % str(updated_type_delay))

        Settings.TypeDelay = DEFAULT_TYPE_DELAY

        # Settings.MoveMouseDelay

        default_move_mouse_delay = Settings.MoveMouseDelay
        assert_equal(self, DEFAULT_MOVE_MOUSE_DELAY, default_move_mouse_delay, 'Default MoveMouseDelay should be equal '
                                                                               'to %s' % str(DEFAULT_MOVE_MOUSE_DELAY))
        updated_move_mouse_delay = 1
        Settings.MoveMouseDelay = updated_move_mouse_delay
        assert_equal(self, Settings.MoveMouseDelay, updated_move_mouse_delay, 'Updated value for MoveMouseDelay should'
                                                                              'be %s' % updated_move_mouse_delay)

        Settings.MoveMouseDelay = DEFAULT_MOVE_MOUSE_DELAY

        # Settings.ClickDelay

        default_click_delay = Settings.ClickDelay
        assert_equal(self, DEFAULT_CLICK_DELAY, default_click_delay, 'Default ClickDelay should be equal to %s'
                     % str(DEFAULT_CLICK_DELAY))

        Settings.ClickDelay = 2
        assert_equal(self, 1, Settings.ClickDelay, 'ClickDelay greater than 1 is defaulted to 1')
        click(youtube_top_site_image)
        assert_equal(self, 0, Settings.ClickDelay, 'ClickDelay should be defaulted to 0 after click action')

        updated_click_delay = 0.5
        Settings.ClickDelay = updated_click_delay
        assert_equal(self, updated_click_delay, Settings.ClickDelay, 'Updated value for ClickDelay should be equal to '
                                                                     '%s' % str(updated_click_delay))

        Settings.ClickDelay = DEFAULT_CLICK_DELAY

        # Settings.MinSimilarity

        default_min_similarity = Settings.MinSimilarity
        assert_equal(self, DEFAULT_MIN_SIMILARITY, default_min_similarity, 'Default MinSimilarity should be equal '
                                                                           'to %s' % str(DEFAULT_MIN_SIMILARITY))
        updated_min_similarity = 0.5
        Settings.MinSimilarity = updated_min_similarity
        assert_equal(self, Settings.MinSimilarity, updated_min_similarity, 'Updated value for MinSimilarity should'
                                                                           'be %s' % updated_min_similarity)

        Settings.MinSimilarity = 2
        assert_equal(self, 1, Settings.MinSimilarity, 'MinSimilarity greater than 1 is defaulted to 1')

        Settings.MinSimilarity = DEFAULT_MIN_SIMILARITY

        # Settings.AutoWaitTimeout

        default_auto_wait_timeout = DEFAULT_AUTO_WAIT_TIMEOUT
        assert_equal(self, DEFAULT_AUTO_WAIT_TIMEOUT, default_auto_wait_timeout,
                     'Default AutoWaitTimeout should be equal to %s' % str(DEFAULT_AUTO_WAIT_TIMEOUT))

        updated_auto_wait_timeout = 3
        Settings.AutoWaitTimeout = updated_auto_wait_timeout
        assert_equal(self, Settings.AutoWaitTimeout, updated_auto_wait_timeout,
                     'Updated value for AutoWaitTimeout should be %s' % updated_auto_wait_timeout)

        Settings.AutoWaitTimeout = DEFAULT_AUTO_WAIT_TIMEOUT

        # Settings.DelayBeforeMouseDown
        # Settings.DelayBeforeDrag
        # Settings.DelayBeforeDrop

        start_location = Location(100, 100)
        end_location = Location(200, 200)

        Settings.DelayBeforeMouseDown = 1
        Settings.DelayBeforeDrag = 1
        Settings.DelayBeforeDrop = 1
        Settings.MoveMouseDelay = 3

        region = Region(100, 100, 100, 100)

        start_time = time.time()
        region.dragDrop(start_location, end_location)
        end_time = time.time()

        total_duration = (Settings.DelayBeforeMouseDown + Settings.DelayBeforeDrag + Settings.DelayBeforeDrop +
                          Settings.MoveMouseDelay)

        expected_duration = end_time - start_time >= total_duration
        assert_true(self, expected_duration, 'Total duration for dragDrop should be equal or greater than %s seconds'
                    % total_duration)

        Settings.DelayBeforeMouseDown = DEFAULT_DELAY_BEFORE_MOUSE_DOWN
        Settings.DelayBeforeDrag = DEFAULT_DELAY_BEFORE_DRAG
        Settings.DelayBeforeDrop = DEFAULT_DELAY_BEFORE_DROP
        Settings.MoveMouseDelay = DEFAULT_MOVE_MOUSE_DELAY

        # Settings.SlowMotionDelay

        default_slow_motion_delay = Settings.SlowMotionDelay
        assert_equal(self, DEFAULT_SLOW_MOTION_DELAY, default_slow_motion_delay,
                     'Default SlowMotionDelay should be equal to %s' % str(DEFAULT_SLOW_MOTION_DELAY))
        updated_slow_motion_delay = 3
        Settings.SlowMotionDelay = updated_slow_motion_delay
        assert_equal(self, Settings.SlowMotionDelay, updated_slow_motion_delay,
                     'Updated value for SlowMotionDelay should be %s' % updated_slow_motion_delay)

        Settings.SlowMotionDelay = DEFAULT_SLOW_MOTION_DELAY

        # Settings.ObserveScanRate

        default_observe_scan_rate = Settings.ObserveScanRate
        assert_equal(self, DEFAULT_OBSERVE_SCAN_RATE, default_observe_scan_rate,
                     'Default ObserveScanRate should be equal to %s' % str(DEFAULT_OBSERVE_SCAN_RATE))
        updated_observe_scan_rate = 5
        Settings.ObserveScanRate = updated_observe_scan_rate
        assert_equal(self, Settings.ObserveScanRate, updated_observe_scan_rate,
                     'Updated value for ObserveScanRate should be %s' % updated_observe_scan_rate)

        Settings.ObserveScanRate = DEFAULT_OBSERVE_SCAN_RATE

        # Settings.ObserveMinChangedPixels

        default_observe_min_changed_pixels = Settings.ObserveMinChangedPixels
        assert_equal(self, DEFAULT_OBSERVE_MIN_CHANGED_PIXELS, default_observe_min_changed_pixels,
                     'Default ObserveMinChangedPixels should be equal to %s' % str(DEFAULT_OBSERVE_MIN_CHANGED_PIXELS))
        updated_observe_min_changed_pixels = 60
        Settings.ObserveMinChangedPixels = updated_observe_min_changed_pixels
        assert_equal(self, Settings.ObserveMinChangedPixels, updated_observe_min_changed_pixels,
                     'Updated value for ObserveMinChangedPixels should be %s' % updated_observe_min_changed_pixels)

        Settings.ObserveMinChangedPixels = DEFAULT_OBSERVE_MIN_CHANGED_PIXELS

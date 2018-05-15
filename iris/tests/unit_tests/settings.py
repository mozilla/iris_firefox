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

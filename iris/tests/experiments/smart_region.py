# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'This test case tests the smart region feature.'
        self.enabled = False

    def run(self):
        url = LocalWeb.FOCUS_TEST_SITE
        focus_text_pattern = Pattern('focus_text.png')

        navigate(url)
        expected = exists(LocalWeb.FOCUS_LOGO, 10)
        assert_true(self, expected, 'Page successfully loaded, focus logo found.')

        # Predefined screen regions.
        region1 = Screen.TOP_HALF
        region1.highlight(1)
        region2 = Screen.BOTTOM_HALF
        region2.highlight(1)

        region3 = Screen.LEFT_HALF
        region3.highlight(1)
        region4 = Screen.RIGHT_HALF
        region4.highlight()

        region5 = Screen.TOP_THIRD
        region5.highlight(1)
        region6 = Screen.MIDDLE_THIRD_HORIZONTAL
        region6.highlight(1)
        region7 = Screen.BOTTOM_THIRD
        region7.highlight(1)

        region8 = Screen.LEFT_THIRD
        region8.highlight(1)
        region9 = Screen.MIDDLE_THIRD_VERTICAL
        region9.highlight(1)
        region10 = Screen.RIGHT_THIRD
        region10.highlight(1)

        region11 = Screen.UPPER_LEFT_CORNER
        region11.highlight(1)
        region12 = Screen.UPPER_RIGHT_CORNER
        region12.highlight(1)
        region13 = Screen.LOWER_LEFT_CORNER
        region13.highlight(1)
        region14 = Screen.LOWER_RIGHT_CORNER
        region14.highlight(1)

        region11.highlight(1)
        expected = region11.exists(focus_text_pattern, 10)
        assert_true(self, expected, 'Text successfully found.')

        # Create a smaller region starting from region11.
        region15 = region11.top_half()
        region15.highlight(1)
        expected = region15.exists(focus_text_pattern, 10)
        assert_true(self, expected, 'Text successfully found in the smaller region.')

        # Create an even smaller region.
        region16 = region15.left_half()
        region16.highlight(1)
        expected = region16.exists(focus_text_pattern, 10)
        assert_true(self, expected, 'Text successfully found in the even smaller region.')

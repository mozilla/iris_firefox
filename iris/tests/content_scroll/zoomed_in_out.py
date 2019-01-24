# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Scrolling works properly while being zoomed in or out.'
        self.test_case_id = '4659'
        self.test_suite_id = '102'
        self.locales = ['en-US']

    def run(self):
        after_zooming_in_content_pattern = Pattern('after_zooming_in_content.png')
        after_zooming_out_content_pattern = Pattern('after_zooming_out_content.png')

        # Scroll bar arrows pattern for Windows
        if Settings.is_windows():
            scroll_height = SCREEN_HEIGHT
        else:
            scroll_height = 100

        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)
        web_page_loaded_exists = exists(LocalWeb.SOAP_WIKI_SOAP_LABEL, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, web_page_loaded_exists, 'The website in question is properly loaded.')

        # Scrolling after zoomed in the page
        [zoom_in() for _ in range(2)]
        after_zooming_in_content_exists = exists(after_zooming_in_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, after_zooming_in_content_exists, 'Zoom in action works properly')
        click(after_zooming_in_content_pattern)

        # Scroll up and down using mouse wheel
        before_scroll_content_exists = exists(after_zooming_in_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, before_scroll_content_exists, 'Content before scrolling using mouse wheel is on the page')

        [scroll(-scroll_height) for _ in range(3)]
        after_scroll_down_content_not_exists = exists(after_zooming_in_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_false(self, after_scroll_down_content_not_exists,
                     'After zooming in and scrolling down using mouse wheel content is gone')
        [scroll(scroll_height) for _ in range(3)]

        after_scroll_content_exists = exists(after_zooming_in_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, after_scroll_content_exists, 'Scroll up and down using mouse wheel is successful.')

        # Scroll up and down using arrow keys
        before_scroll_content_exists = exists(after_zooming_in_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, before_scroll_content_exists, 'Content before scrolling using arrow keys is on the page')

        repeat_key_down(10)
        after_scroll_down_content_not_exists = exists(after_zooming_in_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_false(self, after_scroll_down_content_not_exists,
                     'After zooming in and scrolling down using arrow keys content is gone')
        repeat_key_up(10)

        after_scroll_content_exists = exists(after_zooming_in_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, after_scroll_content_exists, 'Scroll up and down using arrow keys is successful.')

        # Scroll up and down using page up/down keys
        before_scroll_content_exists = exists(after_zooming_in_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, before_scroll_content_exists, 'Content before scrolling using page up/down is on the page')

        [type(Key.PAGE_DOWN) for _ in range(4)]
        after_scroll_down_content_not_exists = exists(after_zooming_in_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_false(self, after_scroll_down_content_not_exists,
                     'After zooming in and scrolling down using page up/down keys content is gone')
        [type(Key.PAGE_UP) for _ in range(4)]

        after_scroll_content_exists = exists(after_zooming_in_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, after_scroll_content_exists, 'Scroll up and down using page up/down keys is successful.')

        # Scroll up and down using ctrl + up/down keys
        before_scroll_content_exists = exists(after_zooming_in_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, before_scroll_content_exists, 'Content before scrolling using ctrl + up/down is on the page')

        if Settings.is_mac():
            type(Key.DOWN, modifier=KeyModifier.CMD)
        else:
            type(Key.DOWN, modifier=KeyModifier.CTRL)

        after_scroll_down_content_not_exists = exists(after_zooming_in_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_false(self, after_scroll_down_content_not_exists,
                     'After zooming in and scrolling down using ctrl + up/down keys content is gone')

        if Settings.is_mac():
            type(Key.UP, modifier=KeyModifier.CMD)
        else:
            type(Key.UP, modifier=KeyModifier.CTRL)

        after_scroll_content_exists = exists(after_zooming_in_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, after_scroll_content_exists, 'Scroll up and down using ctrl + up/down keys is successful.')

        # Scroll up and down using space bar
        before_scroll_content_exists = exists(after_zooming_in_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, before_scroll_content_exists, 'Content before scrolling using space bar is on the page')

        [type(Key.SPACE) for _ in range(5)]
        after_scroll_down_content_not_exists = exists(after_zooming_in_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_false(self, after_scroll_down_content_not_exists,
                     'After zooming in and scrolling down using space bar content is gone')
        page_home()

        restore_zoom()

        # Scrolling after zoomed out the page
        [zoom_out() for _ in range(2)]

        after_zooming_out_content_exists = exists(after_zooming_out_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, after_zooming_out_content_exists, 'Zoom out action works properly')

        # Scroll up and down using mouse wheel
        before_scroll_content_exists = exists(after_zooming_out_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, before_scroll_content_exists, 'Content before scrolling using mouse wheel is on the page')

        [scroll(-scroll_height) for _ in range(3)]
        after_scroll_up_content_not_exists = exists(after_zooming_out_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_false(self, after_scroll_up_content_not_exists,
                     'After zooming out and scrolling up using mouse wheel content is gone')
        [scroll(scroll_height) for _ in range(3)]

        after_scroll_content_exists = exists(after_zooming_out_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, after_scroll_content_exists, 'Scroll up and down using mouse wheel is successful.')

        # Scroll up and down using arrow keys
        before_scroll_content_exists = exists(after_zooming_out_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, before_scroll_content_exists, 'Content before scrolling using arrow keys is on the page')

        repeat_key_down(10)
        after_scroll_up_content_not_exists = exists(after_zooming_out_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_false(self, after_scroll_up_content_not_exists,
                     'After zooming out and scrolling up using arrow keys content is gone')
        repeat_key_up(10)

        after_scroll_content_exists = exists(after_zooming_out_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, after_scroll_content_exists, 'Scroll up and down using arrow keys is successful.')

        # Scroll up and down using page up/down keys
        before_scroll_content_exists = exists(after_zooming_out_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, before_scroll_content_exists, 'Content before scrolling using page up/down is on the page')

        [type(Key.PAGE_DOWN) for _ in range(4)]
        after_scroll_up_content_not_exists = exists(after_zooming_out_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_false(self, after_scroll_up_content_not_exists,
                     'After zooming out and scrolling up using page up/down keys content is gone')
        [type(Key.PAGE_UP) for _ in range(4)]

        after_scroll_content_exists = exists(after_zooming_out_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, after_scroll_content_exists, 'Scroll up and down using page up/down keys is successful.')

        # Scroll up and down using ctrl + up/down keys
        before_scroll_content_exists = exists(after_zooming_out_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, before_scroll_content_exists, 'Content before scrolling using ctrl + up/down is on the page')

        if Settings.is_mac():
            type(Key.DOWN, modifier=KeyModifier.CMD)
        else:
            type(Key.DOWN, modifier=KeyModifier.CTRL)

        after_scroll_up_content_not_exists = exists(after_zooming_out_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_false(self, after_scroll_up_content_not_exists,
                     'After zooming out and scrolling up using ctrl + up/down keys content is gone')

        if Settings.is_mac():
            type(Key.UP, modifier=KeyModifier.CMD)
        else:
            type(Key.UP, modifier=KeyModifier.CTRL)

        after_scroll_content_exists = exists(after_zooming_out_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, after_scroll_content_exists, 'Scroll up and down using ctrl + up/down keys is successful.')

        # Scroll up and down using space bar
        before_scroll_content_exists = exists(after_zooming_out_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, before_scroll_content_exists, 'Content before scrolling using space bar is on the page')

        [type(Key.SPACE) for _ in range(5)]
        after_scroll_up_content_not_exists = exists(after_zooming_out_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_false(self, after_scroll_up_content_not_exists,
                     'After zooming out and scrolling up using space bar content is gone')


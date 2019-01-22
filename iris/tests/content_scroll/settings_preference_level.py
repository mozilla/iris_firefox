# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Scrolling with different settings at preferences-level.'
        self.test_case_id = '4713'
        self.test_suite_id = '102'
        self.locales = ['en-US']

    def run(self):
        checked_use_smooth_scrolling_pattern = Pattern('checked_use_smooth_scrolling.png')
        unchecked_use_smooth_scrolling_pattern = Pattern('unchecked_use_smooth_scrolling.png')
        scroll_content_pattern = Pattern('soap_wiki_content.png')

        if Settings.is_windows():
            scroll_height = SCREEN_HEIGHT*2
        else:
            scroll_height = SCREEN_HEIGHT

        # Use smooth scrolling is disabled
        navigate('about:preferences#general')

        inner_location = Location(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        mouse_move(inner_location)
        type(Key.TAB)
        page_end()

        checked_use_smooth_scrolling_exists = exists(checked_use_smooth_scrolling_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, checked_use_smooth_scrolling_exists, 'Use smooth scrolling option is on the page')

        click(checked_use_smooth_scrolling_pattern)

        unchecked_use_smooth_scrolling_exists = exists(unchecked_use_smooth_scrolling_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, unchecked_use_smooth_scrolling_exists, 'Use smooth scrolling option is disabled')

        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)

        # Scroll up and down using mouse wheel
        before_scroll_content_exists = exists(scroll_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, before_scroll_content_exists, 'Content before scrolling using mouse wheel is on the page')
        click(scroll_content_pattern)

        scroll(-scroll_height)
        try:
            wait_vanish(scroll_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        except FindError:
            raise FindError('Content is still on the page after scrolling')
        scroll(scroll_height)

        after_scroll_content_exists = exists(scroll_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, after_scroll_content_exists, 'Scroll up and down using mouse wheel is successful')

        # Scroll up and down using arrow keys
        before_scroll_content_exists = exists(scroll_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, before_scroll_content_exists, 'Content before scrolling using arrow keys is on the page')

        repeat_key_down(20)
        try:
            wait_vanish(scroll_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        except FindError:
            raise FindError('Content is still on the page after scrolling')
        repeat_key_up(20)

        after_scroll_content_exists = exists(scroll_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, after_scroll_content_exists, 'Scroll up and down using arrow keys is successful')

        # Use smooth scrolling is enabled
        navigate('about:preferences#general')

        inner_location = Location(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        mouse_move(inner_location)
        type(Key.TAB)
        page_end()

        unchecked_use_smooth_scrolling_exists = exists(unchecked_use_smooth_scrolling_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, unchecked_use_smooth_scrolling_exists, 'Use smooth scrolling option is on the page')

        click(unchecked_use_smooth_scrolling_pattern)

        checked_use_smooth_scrolling_exists = exists(checked_use_smooth_scrolling_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, checked_use_smooth_scrolling_exists, 'Use smooth scrolling option is enabled')

        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)

        # Scroll up and down using mouse wheel
        before_scroll_content_exists = exists(scroll_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, before_scroll_content_exists,
                    'Content before scrolling using mouse wheel is on the page after use smooth scrolling is enabled')
        click(scroll_content_pattern)

        scroll(-scroll_height)
        try:
            wait_vanish(scroll_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        except FindError:
            raise FindError('Content is still on the page after scrolling')
        scroll(scroll_height)

        after_scroll_content_exists = exists(scroll_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, after_scroll_content_exists,
                    'Scroll up and down using mouse wheel is successful after use smooth scrolling is enabled')

        # Scroll up and down using arrow keys
        before_scroll_content_exists = exists(scroll_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, before_scroll_content_exists,
                    'Content before scrolling using arrow keys is on the page after use smooth scrolling is enabled')

        repeat_key_down(20)
        try:
            wait_vanish(scroll_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        except FindError:
            raise FindError('Content is still on the page after scrolling')
        repeat_key_up(20)

        after_scroll_content_exists = exists(scroll_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, after_scroll_content_exists,
                    'Scroll up and down using arrow keys is successful after use smooth scrolling is enabled')

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Scrolling works properly while Reader View is enabled.'
        self.test_case_id = '4655'
        self.test_suite_id = '102'
        self.locales = ['en-US']

    def run(self):
        reader_view_button_pattern = Pattern('reader_view_button.png')
        reader_view_content_pattern = Pattern('reader_view_content.png')

        if Settings.is_windows():
            scroll_height = 1600
        if Settings.is_linux() or Settings.is_mac():
            scroll_height = 100

        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)
        web_page_loaded_exists = exists(LocalWeb.SOAP_WIKI_SOAP_LABEL, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, web_page_loaded_exists, 'The website is properly loaded.')

        click(reader_view_button_pattern, DEFAULT_FX_DELAY)

        reader_view_button_exists = exists(reader_view_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, reader_view_button_exists, 'The website is properly loaded in Reader View.')

        # Scroll up and down using mouse wheel
        before_scroll_content_exists = exists(reader_view_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, before_scroll_content_exists, 'Content before scrolling is on the page')

        click(reader_view_content_pattern)
        scroll(-scroll_height)
        try:
            wait_vanish(reader_view_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        except FindError:
            raise FindError('After scrolling content is still on the page')
        scroll(scroll_height)

        after_scroll_content_exists = exists(reader_view_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, after_scroll_content_exists, 'Scroll up and down using mouse wheel is successful.')

        # Scroll up and down using arrow keys
        before_scroll_content_exists = exists(reader_view_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, before_scroll_content_exists, 'Content before scrolling is on the page')

        repeat_key_down(10)
        try:
            wait_vanish(reader_view_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        except FindError:
            raise FindError('After scrolling content is still on the page')
        repeat_key_up(10)

        after_scroll_content_exists = exists(reader_view_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, after_scroll_content_exists, 'Scroll up and down using arrow keys is successful.')

        # Scroll up and down using page up/down keys
        before_scroll_content_exists = exists(reader_view_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, before_scroll_content_exists, 'Content before scrolling is on the page')

        [type(Key.PAGE_DOWN) for _ in range(4)]
        try:
            wait_vanish(reader_view_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        except FindError:
            raise FindError('After scrolling content is still on the page')
        [type(Key.PAGE_UP) for _ in range(4)]

        after_scroll_content_exists = exists(reader_view_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, after_scroll_content_exists, 'Scroll up and down using page up/down keys is successful.')

        # Scroll up and down using ctrl + up/down keys
        before_scroll_content_exists = exists(reader_view_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, before_scroll_content_exists, 'Content before scrolling is on the page')

        type(Key.DOWN, modifier=KeyModifier.CTRL)
        try:
            wait_vanish(reader_view_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        except FindError:
            raise FindError('After scrolling content is still on the page')
        type(Key.UP, modifier=KeyModifier.CTRL)

        after_scroll_content_exists = exists(reader_view_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, after_scroll_content_exists, 'Scroll up and down using ctrl + up/down keys is successful.')

        # Scroll up and down using space bar
        before_scroll_content_exists = exists(reader_view_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, before_scroll_content_exists, 'Content before scrolling is on the page')

        try:
            type(Key.SPACE)
            after_scroll_content_disappeared = wait_vanish(reader_view_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
            assert_true(self, after_scroll_content_disappeared, 'Scroll up and down using space bar is successful.')
        except FindError:
            raise FindError('Content before scrolling is still on the page')

        close_window()

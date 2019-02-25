# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = '[Win & Linux] Scrolling works properly while print-preview is enabled'
        self.test_case_id = '4654'
        self.test_suite_id = '102'
        self.locales = ['en-US']
        self.exclude = Platform.MAC

    def run(self):
        scroll_content_pattern = Pattern('soap_wiki_print_mode.png')
        print_preview_mode_enabled_pattern = Pattern('print_preview_mode.png')

        # Scroll bar arrows pattern for Windows
        if Settings.is_windows():
            scroll_height = 1600
        if Settings.is_linux():
            scroll_height = 100

        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)
        web_page_loaded_exists = exists(LocalWeb.SOAP_WIKI_SOAP_LABEL, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, web_page_loaded_exists, 'The website is properly loaded.')
        click_hamburger_menu_option('Print...')

        print_preview_mode_exists = exists(print_preview_mode_enabled_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, print_preview_mode_exists, 'Print-preview mode is successfully enabled.')

        # Scroll up and down using mouse wheel
        before_scroll_content_exists = exists(scroll_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, before_scroll_content_exists, 'Content before scrolling using mouse wheel is on the page')

        [scroll(-scroll_height) for _ in range(3)]
        after_scroll_down_content_not_exists = exists(scroll_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_false(self, after_scroll_down_content_not_exists,
                     'Content is gone after scrolling down using mouse wheel in preview mode')
        [scroll(scroll_height) for _ in range(3)]

        after_scroll_content_exists = exists(scroll_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, after_scroll_content_exists, 'Scroll up and down using mouse wheel is successful.')

        # Scroll up and down using arrow keys
        before_scroll_content_exists = exists(scroll_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, before_scroll_content_exists, 'Content before scrolling using arrow keys is on the page')

        repeat_key_down(10)
        after_scroll_down_content_not_exists = exists(scroll_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_false(self, after_scroll_down_content_not_exists,
                     'Content is gone after scrolling down using arrow keys in preview mode')
        repeat_key_up(10)

        after_scroll_content_exists = exists(scroll_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, after_scroll_content_exists, 'Scroll up and down using arrow keys is successful.')

        # Scroll up and down using page up/down keys
        before_scroll_content_exists = exists(scroll_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, before_scroll_content_exists, 'Content before scrolling using page up/down is on the page')

        [type(Key.PAGE_DOWN) for _ in range(4)]
        after_scroll_down_content_not_exists = exists(scroll_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_false(self, after_scroll_down_content_not_exists,
                     'Content is gone after scrolling down using page up/down in preview mode')
        [type(Key.PAGE_UP) for _ in range(4)]

        after_scroll_content_exists = exists(scroll_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, after_scroll_content_exists, 'Scroll up and down using page up/down keys is successful.')

        # Scroll up and down using ctrl + up/down keys
        before_scroll_content_exists = exists(scroll_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, before_scroll_content_exists, 'Content before scrolling using ctrl + up/down is on the page')

        type(Key.DOWN, modifier=KeyModifier.CTRL)
        after_scroll_down_content_not_exists = exists(scroll_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_false(self, after_scroll_down_content_not_exists,
                     'Content is gone after scrolling down using ctrl + up/down keys in preview mode')
        type(Key.UP, modifier=KeyModifier.CTRL)

        after_scroll_content_exists = exists(scroll_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, after_scroll_content_exists, 'Scroll up and down using ctrl + up/down keys is successful.')

        # Scroll up and down using space bar
        before_scroll_content_exists = exists(scroll_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, before_scroll_content_exists, 'Content before scrolling using space bar is on the page')

        [type(Key.SPACE) for _ in range(3)]

        time.sleep(1)
        after_scroll_down_content_not_exists = exists(scroll_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_false(self, after_scroll_down_content_not_exists,
                     'Content is gone after scrolling down using space bar in preview mode')

        close_window()

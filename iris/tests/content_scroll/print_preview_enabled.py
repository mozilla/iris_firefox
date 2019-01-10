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
        print_preview_content_loaded_pattern = Pattern('print_preview_content_loaded.png')
        scroll_content_pattern = Pattern('soap_wiki_print_mode.png')
        scroll_bar_button_up_pattern = Pattern('scroll_bar_button_up.png')
        scroll_bar_button_down_pattern = Pattern('scroll_bar_button_down.png')

        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)
        web_page_loaded_exists = exists(LocalWeb.SOAP_WIKI_SOAP_LABEL, 20)
        assert_true(self, web_page_loaded_exists, 'The website is properly loaded.')

        click_hamburger_menu_option("Print...")
        print_preview_content_loaded_exists = exists(print_preview_content_loaded_pattern, 20)
        assert_true(self, print_preview_content_loaded_exists, 'Print-preview mode is successfully enabled.')

        # Scroll up and down using mouse wheel
        before_scroll_content_exists = exists(scroll_content_pattern, 10)
        try:
            scroll(-1600)
            wait_vanish(scroll_content_pattern, 10)
        except FindError:
            raise FindError('Content before scrolling is still on the page')
        scroll(1600)
        after_scroll_content_pattern = exists(scroll_content_pattern, 10)
        assert_true(self, before_scroll_content_exists and after_scroll_content_pattern, 'Scroll up and down using mouse wheel is successful.')

        # Scroll up and down using scroll bar
        before_scroll_content_exists = exists(scroll_content_pattern, 10)
        try:
            [click(scroll_bar_button_down_pattern, DEFAULT_FX_DELAY) for _ in range(4)]
            wait_vanish(scroll_content_pattern, 10)
        except FindError:
            raise FindError('Content before scrolling is still on the page')
        [click(scroll_bar_button_up_pattern, DEFAULT_FX_DELAY) for _ in range(10)]
        after_scroll_content_pattern = exists(scroll_content_pattern, 10)
        assert_true(self, before_scroll_content_exists and after_scroll_content_pattern, 'Scroll up and down using scroll bar is successful.')

        # Scroll up and down using arrow keys
        before_scroll_content_exists = exists(scroll_content_pattern, 10)
        try:
            repeat_key_down(10)
            wait_vanish(scroll_content_pattern, 10)
        except FindError:
            raise FindError('Content before scrolling is still on the page')
        repeat_key_up(10)
        after_scroll_content_pattern = exists(scroll_content_pattern, 10)
        assert_true(self, before_scroll_content_exists and after_scroll_content_pattern, 'Scroll up and down using arrow keys is successful.')

        # Scroll up and down using page up/down keys
        before_scroll_content_exists = exists(scroll_content_pattern, 10)
        try:
            [type(Key.PAGE_DOWN) for _ in range(4)]
            wait_vanish(scroll_content_pattern, 10)
        except FindError:
            raise FindError('Content before scrolling is still on the page')
        [type(Key.PAGE_UP) for _ in range(4)]
        after_scroll_content_pattern = exists(scroll_content_pattern, 10)
        assert_true(self, before_scroll_content_exists and after_scroll_content_pattern, 'Scroll up and down using page up/down keys is successful.')

        # Scroll up and down using space bar
        before_scroll_content_exists = exists(scroll_content_pattern, 10)
        try:
            type(Key.SPACE)
            after_scroll_content_disappeared = wait_vanish(scroll_content_pattern, 10)
            assert_true(self, before_scroll_content_exists and after_scroll_content_disappeared,
                        'Scroll up and down using space bar is successful.')
        except FindError:
            raise FindError('Content before scrolling is still on the page')

        close_window()
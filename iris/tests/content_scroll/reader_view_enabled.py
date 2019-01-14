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
            scroll_bar_button_up_pattern = Pattern('scroll_bar_button_up.png').similar(0.6)
            scroll_bar_button_down_pattern = Pattern('scroll_bar_button_down.png').similar(0.6)

        if Settings.is_windows():
            scroll_height = 1600
        if Settings.is_linux() or Settings.is_mac():
            scroll_height = 10

        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)
        web_page_loaded_exists = exists(LocalWeb.SOAP_WIKI_SOAP_LABEL, 20)
        assert_true(self, web_page_loaded_exists, 'The website is properly loaded.')

        try:
            wait(reader_view_button_pattern, 10)
            click(reader_view_button_pattern, DEFAULT_FX_DELAY)
        except FindError:
            raise FindError('Cannot find Reader View button')

        reader_view_button_exists = exists(reader_view_content_pattern, 10)
        assert_true(self, reader_view_button_exists, 'The website is properly loaded in Reader View.')

        # Scroll up and down using mouse wheel
        before_scroll_content_exists = exists(reader_view_content_pattern, 10)
        activate_scroll = Location(500, 500)
        try:
            click(activate_scroll)
            scroll(-scroll_height)
            wait_vanish(reader_view_content_pattern, 10)
        except FindError:
            raise FindError('Content before scrolling is still on the page')
        scroll(scroll_height)

        after_scroll_content_exists = exists(reader_view_content_pattern, 10)
        assert_true(self, before_scroll_content_exists and after_scroll_content_exists,
                    'Scroll up and down using mouse wheel is successful.')

        # Scroll up and down using scroll bar
        before_scroll_content_exists = exists(reader_view_content_pattern, 10)
        scroll_bar_location_down = Location(SCREEN_WIDTH - 1, SCREEN_HEIGHT / 1.2)
        scroll_bar_location_up = Location(SCREEN_WIDTH - 1, SCREEN_HEIGHT / 10)
        scroll_bar_region = Region(x=SCREEN_WIDTH / 2, y=0, width=SCREEN_WIDTH / 2, height=SCREEN_HEIGHT)
        try:
            if Settings.is_linux() or Settings.is_mac():
                click(scroll_bar_location_down, DEFAULT_FX_DELAY)
            if Settings.is_windows():
                [click(scroll_bar_button_down_pattern, DEFAULT_FX_DELAY, in_region=scroll_bar_region) for _ in
                 range(10)]
            wait_vanish(reader_view_content_pattern, 10)
        except FindError:
            raise FindError('Content before scrolling is still on the page')

        if Settings.is_linux() or Settings.is_mac():
            click(scroll_bar_location_up, DEFAULT_FX_DELAY)
        if Settings.is_windows():
            [click(scroll_bar_button_up_pattern, DEFAULT_FX_DELAY) for _ in range(10)]

        after_scroll_content_exists = exists(reader_view_content_pattern, 10)
        assert_true(self, before_scroll_content_exists and after_scroll_content_exists,
                    'Scroll up and down using scroll bar is successful.')

        # Scroll up and down using arrow keys
        before_scroll_content_exists = exists(reader_view_content_pattern, 10)
        try:
            repeat_key_down(10)
            wait_vanish(reader_view_content_pattern, 10)
        except FindError:
            raise FindError('Content before scrolling is still on the page')
        repeat_key_up(10)
        after_scroll_content_exists = exists(reader_view_content_pattern, 10)
        assert_true(self, before_scroll_content_exists and after_scroll_content_exists,
                    'Scroll up and down using arrow keys is successful.')

        # Scroll up and down using page up/down keys
        before_scroll_content_exists = exists(reader_view_content_pattern, 10)
        try:
            [type(Key.PAGE_DOWN) for _ in range(4)]
            wait_vanish(reader_view_content_pattern, 10)
        except FindError:
            raise FindError('Content before scrolling is still on the page')
        [type(Key.PAGE_UP) for _ in range(4)]
        after_scroll_content_exists = exists(reader_view_content_pattern, 10)
        assert_true(self, before_scroll_content_exists and after_scroll_content_exists,
                    'Scroll up and down using page up/down keys is successful.')

        # Scroll up and down using space bar
        before_scroll_content_exists = exists(reader_view_content_pattern, 10)
        try:
            type(Key.SPACE)
            after_scroll_content_disappeared = wait_vanish(reader_view_content_pattern, 10)
            assert_true(self, before_scroll_content_exists and after_scroll_content_disappeared,
                        'Scroll up and down using space bar is successful.')
        except FindError:
            raise FindError('Content before scrolling is still on the page')

    close_window()

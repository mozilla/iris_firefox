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
        scroll_bar_pattern = Pattern('scroll_bar_button.png')

        if Settings.is_windows():
            scroll_height = 1600
        if Settings.is_linux() or Settings.is_mac():
            scroll_height = 10

        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)
        web_page_loaded_exists = exists(LocalWeb.SOAP_WIKI_SOAP_LABEL, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, web_page_loaded_exists, 'The website is properly loaded.')

        click(reader_view_button_pattern, DEFAULT_FX_DELAY)

        reader_view_button_exists = exists(reader_view_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, reader_view_button_exists, 'The website is properly loaded in Reader View.')

        # Scroll up and down using mouse wheel
        before_scroll_content_exists = exists(reader_view_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        loc_control = Location(500, 500)

        click(loc_control)
        scroll(-scroll_height)
        scroll(scroll_height)

        after_scroll_content_exists = exists(reader_view_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, before_scroll_content_exists and after_scroll_content_exists,
                    'Scroll up and down using mouse wheel is successful.')

        # Scroll up and down using scroll bar
        before_scroll_content_exists = exists(reader_view_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        before_scroll_button_location = find(scroll_bar_pattern)
        after_scroll_button_position = before_scroll_button_location.offset(0, 500)

        drag_drop(scroll_bar_pattern, after_scroll_button_position)

        after_scroll_button_position.x += 10
        after_scroll_button_position.y += 10
        initial_position = before_scroll_button_location.offset(0, -500)
        drag_drop(after_scroll_button_position, initial_position)

        after_scroll_content_exists = exists(reader_view_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, before_scroll_content_exists and after_scroll_content_exists,
                    'Scroll up and down using scroll bar is successful.')

        # Scroll up and down using arrow keys
        before_scroll_content_exists = exists(reader_view_content_pattern, DEFAULT_FIREFOX_TIMEOUT)

        repeat_key_down(10)
        repeat_key_up(10)

        after_scroll_content_exists = exists(reader_view_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, before_scroll_content_exists and after_scroll_content_exists,
                    'Scroll up and down using arrow keys is successful.')

        # Scroll up and down using page up/down keys
        before_scroll_content_exists = exists(reader_view_content_pattern, DEFAULT_FIREFOX_TIMEOUT)

        [type(Key.PAGE_DOWN) for _ in range(4)]
        [type(Key.PAGE_UP) for _ in range(4)]

        after_scroll_content_exists = exists(reader_view_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, before_scroll_content_exists and after_scroll_content_exists,
                    'Scroll up and down using page up/down keys is successful.')

        # Scroll up and down using ctrl + up/down keys
        before_scroll_content_exists = exists(reader_view_content_pattern, DEFAULT_FIREFOX_TIMEOUT)

        if Settings.is_mac():
            type(Key.DOWN, modifier=KeyModifier.CMD)
        else:
            type(Key.DOWN, modifier=KeyModifier.CTRL)

        if Settings.is_mac():
            type(Key.UP, modifier=KeyModifier.CMD)
        else:
            type(Key.UP, modifier=KeyModifier.CTRL)

        after_scroll_content_exists = exists(reader_view_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, before_scroll_content_exists and after_scroll_content_exists,
                    'Scroll up and down using ctrl + up/down keys is successful.')

        # Scroll up and down using space bar
        before_scroll_content_exists = exists(reader_view_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        try:
            type(Key.SPACE)
            after_scroll_content_disappeared = wait_vanish(reader_view_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
            assert_true(self, before_scroll_content_exists and after_scroll_content_disappeared,
                        'Scroll up and down using space bar is successful.')
        except FindError:
            raise FindError('Content before scrolling is still on the page')

    close_window()

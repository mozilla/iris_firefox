from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Scrolling works properly after resizing the browser window.'
        self.test_case_id = '4656'
        self.test_suite_id = '102'
        self.locales = ['en-US']

    def run(self):
        resizing_confirmed_pattern = Pattern('resizing_confirmed.png')
        browser_console_opened_pattern = Pattern('browser_console_opened.png')
        scroll_content_pattern = Pattern('soap_wiki_content.png')
        if Settings.is_windows():
            scroll_bar_button_up_pattern = Pattern('scroll_bar_button_up.png').similar(0.6)
            scroll_bar_button_down_pattern = Pattern('scroll_bar_button_down.png').similar(0.6)
        else:
            scroll_bar_button_pattern = Pattern('scroll_bar_button.png')

        if Settings.is_windows():
            scroll_height = 1600
        if Settings.is_linux() or Settings.is_mac():
            scroll_height = 10

        change_preference("devtools.chrome.enabled", True)

        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)
        web_page_loaded_exists = exists(LocalWeb.SOAP_WIKI_SOAP_LABEL, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, web_page_loaded_exists, 'The website is properly loaded.')

        open_browser_console()
        click(browser_console_opened_pattern)
        paste('window.resizeTo(500, 400)')
        type(Key.ENTER)

        try:
            wait(browser_console_opened_pattern, DEFAULT_FIREFOX_TIMEOUT)
            click(browser_console_opened_pattern, DEFAULT_FX_DELAY)
            close_tab()
        except FindError:
            raise FindError('Cannot find browser console window')

        resizing_confirmed_exists = exists(resizing_confirmed_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, resizing_confirmed_exists, 'The browser window is successfully resized.')


        # Scroll up and down using mouse wheel
        before_scroll_content_exists = exists(scroll_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        try:
            click(scroll_content_pattern)
            scroll(-scroll_height)
            wait_vanish(scroll_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        except FindError:
            raise FindError('Content before scrolling is still on the page')
        scroll(scroll_height)

        after_scroll_content_exists = exists(scroll_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, before_scroll_content_exists and after_scroll_content_exists,
                    'Scroll up and down using mouse wheel is successful.')

        # Scroll up and down using scroll bar
        before_scroll_content_exists = exists(scroll_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        scroll_bar_location = find(scroll_bar_button_pattern)
        scroll_bar_location.x = scroll_bar_location.x + 5
        scroll_bar_location.y = scroll_bar_location.y + 10

        a_s_l = find(scroll_bar_button_pattern)
        drop_to_x = a_s_l.x
        drop_to_y = a_s_l.y + 400
        location_x_y = Location(drop_to_x, drop_to_y)

        scroll_bar_region = Region(x=0, y=0, width=SCREEN_WIDTH / 2, height=SCREEN_HEIGHT)
        try:
            if Settings.is_linux():
                drag_drop(scroll_bar_location, location_x_y)
            if Settings.is_windows():
                [click(scroll_bar_button_down_pattern, DEFAULT_FX_DELAY, in_region=scroll_bar_region) for _ in
                 range(10)]
            wait_vanish(scroll_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        except FindError:
            raise FindError('Content before scrolling is still on the page')

        if Settings.is_windows():
            [click(scroll_bar_button_up_pattern, DEFAULT_FX_DELAY) for _ in range(10)]

        after_scroll_content_exists = exists(scroll_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, before_scroll_content_exists and after_scroll_content_exists,
                    'Scroll up and down using scroll bar is successful.')

        # Scroll up and down using arrow keys
        before_scroll_content_exists = exists(scroll_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        try:
            repeat_key_down(10)
            wait_vanish(scroll_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        except FindError:
            raise FindError('Content before scrolling is still on the page')
        repeat_key_up(10)
        after_scroll_content_exists = exists(scroll_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, before_scroll_content_exists and after_scroll_content_exists,
                    'Scroll up and down using arrow keys is successful.')

        # Scroll up and down using page up/down keys
        before_scroll_content_exists = exists(scroll_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        try:
            [type(Key.PAGE_DOWN) for _ in range(4)]
            wait_vanish(scroll_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        except FindError:
            raise FindError('Content before scrolling is still on the page')
        [type(Key.PAGE_UP) for _ in range(4)]
        after_scroll_content_exists = exists(scroll_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, before_scroll_content_exists and after_scroll_content_exists,
                    'Scroll up and down using page up/down keys is successful.')

        # Scroll up and down using ctrl + up/down keys
        before_scroll_content_exists = exists(scroll_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        try:
            if Settings.is_mac():
                type(Key.DOWN, modifier=KeyModifier.CMD)
            else:
                type(Key.DOWN, modifier=KeyModifier.CTRL)
            wait_vanish(scroll_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        except FindError:
            raise FindError('Content before scrolling is still on the page')

        if Settings.is_mac():
            type(Key.UP, modifier=KeyModifier.CMD)
        else:
            type(Key.UP, modifier=KeyModifier.CTRL)

        after_scroll_content_exists = exists(scroll_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, before_scroll_content_exists and after_scroll_content_exists,
                    'Scroll up and down using ctrl + up/down keys is successful.')

        # Scroll up and down using space bar
        before_scroll_content_exists = exists(scroll_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        try:
            type(Key.SPACE)
            after_scroll_content_disappeared = wait_vanish(scroll_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
            assert_true(self, before_scroll_content_exists and after_scroll_content_disappeared,
                        'Scroll up and down using space bar is successful.')
        except FindError:
            raise FindError('Content before scrolling is still on the page')

    close_window()

from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Scrolling works properly after resizing the browser window.'
        self.test_case_id = '4656'
        self.test_suite_id = '102'
        self.locales = ['en-US']

    def setup(self):
        BaseTest.setup(self)
        self.set_profile_pref({'devtools.chrome.enabled': True})

    def run(self):
        resizing_confirmed_pattern = Pattern('resizing_confirmed.png')
        browser_console_opened_pattern = Pattern('browser_console_opened.png')
        scroll_content_pattern = Pattern('soap_wiki_content.png')

        if Settings.is_windows():
            scroll_height = 1600
        if Settings.is_linux() or Settings.is_mac():
            scroll_height = 200

        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)
        web_page_loaded_exists = exists(LocalWeb.SOAP_WIKI_SOAP_LABEL, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, web_page_loaded_exists, 'The website is properly loaded.')

        open_browser_console()
        click(browser_console_opened_pattern)
        paste('window.resizeTo(550, 600)')
        type(Key.ENTER)

        resizing_confirmed_exists = exists(resizing_confirmed_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, resizing_confirmed_exists, 'The browser window is successfully resized.')

        # Scroll up and down using mouse wheel
        before_scroll_content_exists = exists(scroll_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, before_scroll_content_exists, 'Content before scrolling using mouse wheel is on the page')
        click(scroll_content_pattern)

        scroll(-scroll_height)
        time.sleep(DEFAULT_UI_DELAY)
        content_exists = exists(scroll_content_pattern)
        assert_false(self, content_exists, 'Content is still on the page after scrolling')

        scroll(scroll_height)

        after_scroll_content_exists = exists(scroll_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, after_scroll_content_exists, 'Scroll up and down using mouse wheel is successful.')

        # Scroll up and down using arrow keys
        before_scroll_content_exists = exists(scroll_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, before_scroll_content_exists, 'Content before scrolling using arrow keys is on the page')

        repeat_key_down(10)
        time.sleep(DEFAULT_UI_DELAY)
        content_exists = exists(scroll_content_pattern)
        assert_false(self, content_exists, 'Content is still on the page after scrolling')

        repeat_key_up(10)

        after_scroll_content_exists = exists(scroll_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, after_scroll_content_exists, 'Scroll up and down using arrow keys is successful.')

        # Scroll up and down using page up/down keys
        before_scroll_content_exists = exists(scroll_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, before_scroll_content_exists, 'Content before scrolling using page up/down is on the page')

        [type(Key.PAGE_DOWN) for _ in range(4)]
        time.sleep(DEFAULT_UI_DELAY)
        content_exists = exists(scroll_content_pattern)
        assert_false(self, content_exists, 'Content is still on the page after scrolling')

        [type(Key.PAGE_UP) for _ in range(4)]

        after_scroll_content_exists = exists(scroll_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, after_scroll_content_exists, 'Scroll up and down using page up/down keys is successful.')

        # Scroll up and down using ctrl + up/down keys
        before_scroll_content_exists = exists(scroll_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, before_scroll_content_exists, 'Content before scrolling using ctrl + up/down is on the page')

        if Settings.is_mac():
            type(Key.DOWN, modifier=KeyModifier.CMD)
        else:
            type(Key.DOWN, modifier=KeyModifier.CTRL)

        time.sleep(DEFAULT_UI_DELAY)
        content_exists = exists(scroll_content_pattern)
        assert_false(self, content_exists, 'Content is still on the page after scrolling')

        if Settings.is_mac():
            type(Key.UP, modifier=KeyModifier.CMD)
        else:
            type(Key.UP, modifier=KeyModifier.CTRL)

        after_scroll_content_exists = exists(scroll_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, after_scroll_content_exists, 'Scroll up and down using ctrl + up/down keys is successful.')

        # Scroll up and down using space bar
        before_scroll_content_exists = exists(scroll_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, before_scroll_content_exists, 'Content before scrolling using space bar is on the page.')

        type(Key.SPACE)
        type(Key.SPACE)
        time.sleep(DEFAULT_UI_DELAY)
        content_exists = exists(scroll_content_pattern)
        assert_false(self, content_exists, 'Content is still on the page after scrolling')

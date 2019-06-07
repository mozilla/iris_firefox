# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Scrolling works properly after resizing the browser window.',
        test_case_id='4656',
        test_suite_id='102',
        locales=['en-US'],
        preferences={'devtools.chrome.enabled': True}
    )
    def run(self, firefox):
        resizing_confirmed_pattern = Pattern('resizing_confirmed.png')
        browser_console_opened_pattern = Pattern('browser_console_opened.png')
        scroll_content_pattern = Pattern('soap_wiki_content.png')

        if OSHelper.is_windows():
            scroll_height = 1600
        if OSHelper.is_linux() or OSHelper.is_mac():
            scroll_height = 200

        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)

        web_page_loaded_exists = exists(LocalWeb.SOAP_WIKI_SOAP_LABEL, FirefoxSettings.FIREFOX_TIMEOUT)
        assert web_page_loaded_exists is True, 'The website is properly loaded.'

        open_browser_console()

        click(browser_console_opened_pattern)

        paste('window.resizeTo(400, 500)')
        type(Key.ENTER)

        resizing_confirmed_exists = exists(resizing_confirmed_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert resizing_confirmed_exists is True, 'The browser window is successfully resized.'

        click(browser_console_opened_pattern)
        close_tab()

        # Scroll up and down using mouse wheel
        before_scroll_content_exists = exists(scroll_content_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert before_scroll_content_exists is True, 'Content before scrolling using mouse wheel is on the page'

        click(scroll_content_pattern)

        Mouse().scroll(0, -scroll_height)

        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)

        content_exists = exists(scroll_content_pattern)
        assert content_exists is False, 'Content is still on the page after scrolling'

        Mouse().scroll(0, scroll_height)

        after_scroll_content_exists = exists(scroll_content_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert after_scroll_content_exists is True, 'Scroll up and down using mouse wheel is successful.'

        # Scroll up and down using arrow keys
        before_scroll_content_exists = exists(scroll_content_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert before_scroll_content_exists is True, 'Content before scrolling using arrow keys is on the page'

        repeat_key_down(10)

        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)

        content_exists = exists(scroll_content_pattern)
        assert content_exists is False, 'Content is still on the page after scrolling'

        repeat_key_up(10)

        after_scroll_content_exists = exists(scroll_content_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert after_scroll_content_exists is True, 'Scroll up and down using arrow keys is successful.'

        # Scroll up and down using page up/down keys
        before_scroll_content_exists = exists(scroll_content_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert before_scroll_content_exists is True, 'Content before scrolling using page up/down is on the page'

        [type(Key.PAGE_DOWN) for _ in range(4)]

        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)

        content_exists = exists(scroll_content_pattern)
        assert content_exists is False, 'Content is still on the page after scrolling'

        [type(Key.PAGE_UP) for _ in range(4)]

        after_scroll_content_exists = exists(scroll_content_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert after_scroll_content_exists is True, 'Scroll up and down using page up/down keys is successful.'

        # Scroll up and down using ctrl + up/down keys
        before_scroll_content_exists = exists(scroll_content_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert before_scroll_content_exists is True, 'Content before scrolling using ctrl + up/down is on the page'

        if OSHelper.is_mac():
            type(Key.DOWN, modifier=KeyModifier.CMD)
        else:
            type(Key.DOWN, modifier=KeyModifier.CTRL)

        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)

        content_exists = exists(scroll_content_pattern)
        assert content_exists is False, 'Content is still on the page after scrolling'

        if OSHelper.is_mac():
            type(Key.UP, modifier=KeyModifier.CMD)
        else:
            type(Key.UP, modifier=KeyModifier.CTRL)

        after_scroll_content_exists = exists(scroll_content_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert after_scroll_content_exists is True, 'Scroll up and down using ctrl + up/down keys is successful.'

        # Scroll up and down using space bar
        before_scroll_content_exists = exists(scroll_content_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert before_scroll_content_exists is True, 'Content before scrolling using space bar is on the page.'

        type(Key.SPACE)
        type(Key.SPACE)

        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)

        content_exists = exists(scroll_content_pattern)
        assert content_exists is False, 'Content is still on the page after scrolling'

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='[Win & Linux] Scrolling works properly while print-preview is enabled',
        test_case_id='4654',
        test_suite_id='102',
        locale=['en-US'],
        exclude=OSPlatform.MAC
    )
    def run(self, firefox):
        scroll_content_pattern = Pattern('soap_wiki_print_mode.png')
        print_preview_mode_enabled_pattern = Pattern('print_preview_mode.png')

        # Scroll bar arrows pattern for Windows
        if OSHelper.is_windows():
            scroll_height = 1600
        else:
            scroll_height = 100

        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)

        web_page_loaded_exists = exists(LocalWeb.SOAP_WIKI_SOAP_LABEL, Settings.FIREFOX_TIMEOUT)
        assert web_page_loaded_exists is True, 'The website is properly loaded.'

        click_hamburger_menu_option('Print...')

        print_preview_mode_exists = exists(print_preview_mode_enabled_pattern, Settings.FIREFOX_TIMEOUT)
        assert print_preview_mode_exists is True, 'Print-preview mode is successfully enabled.'

        # Scroll up and down using mouse wheel
        before_scroll_content_exists = exists(scroll_content_pattern, Settings.FIREFOX_TIMEOUT)
        assert before_scroll_content_exists is True, 'Content before scrolling using mouse wheel is on the page'

        [Mouse().scroll(0, -scroll_height) for _ in range(3)]
        after_scroll_down_content_not_exists = exists(scroll_content_pattern, Settings.FIREFOX_TIMEOUT)
        assert after_scroll_down_content_not_exists is False, 'Content is gone after scrolling down ' \
                                                              'using mouse wheel in preview mode'
        [Mouse().scroll(0, scroll_height) for _ in range(3)]

        after_scroll_content_exists = exists(scroll_content_pattern, Settings.FIREFOX_TIMEOUT)
        assert after_scroll_content_exists is True, 'Scroll up and down using mouse wheel is successful.'

        # Scroll up and down using arrow keys
        before_scroll_content_exists = exists(scroll_content_pattern, Settings.FIREFOX_TIMEOUT)
        assert before_scroll_content_exists is True, 'Content before scrolling using arrow keys is on the page'

        repeat_key_down(10)
        after_scroll_down_content_not_exists = exists(scroll_content_pattern, Settings.FIREFOX_TIMEOUT)
        assert after_scroll_down_content_not_exists is False, 'Content is gone after scrolling down' \
                                                              ' using arrow keys in preview mode'
        repeat_key_up(10)

        after_scroll_content_exists = exists(scroll_content_pattern, Settings.FIREFOX_TIMEOUT)
        assert after_scroll_content_exists is True, 'Scroll up and down using arrow keys is successful.'

        # Scroll up and down using page up/down keys
        before_scroll_content_exists = exists(scroll_content_pattern, Settings.FIREFOX_TIMEOUT)
        assert before_scroll_content_exists is True, 'Content before scrolling using page up/down is on the page'

        [type(Key.PAGE_DOWN) for _ in range(4)]
        after_scroll_down_content_not_exists = exists(scroll_content_pattern, Settings.FIREFOX_TIMEOUT)
        assert after_scroll_down_content_not_exists is False, 'Content is gone after scrolling down' \
                                                              ' using page up/down in preview mode'
        [type(Key.PAGE_UP) for _ in range(4)]

        after_scroll_content_exists = exists(scroll_content_pattern, Settings.FIREFOX_TIMEOUT)
        assert after_scroll_content_exists is True, 'Scroll up and down using page up/down keys is successful.'

        # Scroll up and down using ctrl + up/down keys
        before_scroll_content_exists = exists(scroll_content_pattern, Settings.FIREFOX_TIMEOUT)
        assert before_scroll_content_exists is True, 'Content before scrolling using ctrl + up/down is on the page'

        type(Key.DOWN, modifier=KeyModifier.CTRL)
        after_scroll_down_content_not_exists = exists(scroll_content_pattern, Settings.FIREFOX_TIMEOUT)
        assert after_scroll_down_content_not_exists is False, 'Content is gone after scrolling down' \
                                                              ' using ctrl + up/down keys in preview mode'
        type(Key.UP, modifier=KeyModifier.CTRL)

        after_scroll_content_exists = exists(scroll_content_pattern, Settings.FIREFOX_TIMEOUT)
        assert after_scroll_content_exists is True, 'Scroll up and down using' \
                                                    ' ctrl + up/down keys is successful.'

        # Scroll up and down using space bar
        before_scroll_content_exists = exists(scroll_content_pattern, Settings.FIREFOX_TIMEOUT)
        assert before_scroll_content_exists is True, 'Content before scrolling using space bar is on the page'

        [type(Key.SPACE) for _ in range(3)]

        time.sleep(1)

        after_scroll_down_content_not_exists = exists(scroll_content_pattern, Settings.FIREFOX_TIMEOUT)
        assert after_scroll_down_content_not_exists is False, 'Content is gone after scrolling down' \
                                                              ' using space bar in preview mode'

        close_window()

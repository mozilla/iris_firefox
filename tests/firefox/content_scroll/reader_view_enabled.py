# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Scrolling works properly while Reader View is enabled.',
        test_case_id='4655',
        test_suite_id='102',
        locales=['en-US']
    )
    def run(self, firefox):
        reader_view_button_pattern = Pattern('reader_view_button.png')
        reader_view_content_pattern = Pattern('reader_view_content.png')

        if OSHelper.is_windows():
            scroll_height = 1600
        if OSHelper.is_linux() or OSHelper.is_mac():
            scroll_height = 200

        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)

        web_page_loaded_exists = exists(LocalWeb.SOAP_WIKI_SOAP_LABEL, FirefoxSettings.FIREFOX_TIMEOUT)
        assert web_page_loaded_exists is True, 'The website is properly loaded.'

        click(reader_view_button_pattern)

        reader_view_button_exists = exists(reader_view_content_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert reader_view_button_exists is True, 'The website is properly loaded in Reader View.'

        # Scroll up and down using mouse wheel
        before_scroll_content_exists = exists(reader_view_content_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert before_scroll_content_exists is True, 'Content before scrolling using mouse wheel is on the page'

        click(reader_view_content_pattern)

        Mouse().scroll(0, -scroll_height)
        try:
            wait_vanish(reader_view_content_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        except FindError:
            raise FindError('Content is still on the page after scrolling')
        Mouse().scroll(0, scroll_height)

        after_scroll_content_exists = exists(reader_view_content_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert after_scroll_content_exists is True, 'Scroll up and down using mouse wheel is successful.'

        # Scroll up and down using arrow keys
        before_scroll_content_exists = exists(reader_view_content_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert before_scroll_content_exists is True, 'Content before scrolling using arrow keys is on the page'

        repeat_key_down(10)
        try:
            wait_vanish(reader_view_content_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        except FindError:
            raise FindError('Content is still on the page after scrolling')
        repeat_key_up(10)

        after_scroll_content_exists = exists(reader_view_content_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert after_scroll_content_exists is True, 'Scroll up and down using arrow keys is successful.'

        # Scroll up and down using page up/down keys
        before_scroll_content_exists = exists(reader_view_content_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert before_scroll_content_exists is True, 'Content before scrolling using page up/down is on the page'

        [type(Key.PAGE_DOWN) for _ in range(4)]
        try:
            wait_vanish(reader_view_content_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        except FindError:
            raise FindError('Content is still on the page after scrolling')
        [type(Key.PAGE_UP) for _ in range(4)]

        after_scroll_content_exists = exists(reader_view_content_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert after_scroll_content_exists is True, 'Scroll up and down using page up/down keys is successful.'

        # Scroll up and down using ctrl + up/down keys
        before_scroll_content_exists = exists(reader_view_content_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert before_scroll_content_exists is True, 'Content before scrolling using ctrl + up/down is on the page'

        if OSHelper.is_mac():
            type(Key.DOWN, modifier=KeyModifier.CMD)
        else:
            type(Key.DOWN, modifier=KeyModifier.CTRL)

        try:
            wait_vanish(reader_view_content_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        except FindError:
            raise FindError('Content is still on the page after scrolling')

        if OSHelper.is_mac():
            type(Key.UP, modifier=KeyModifier.CMD)
        else:
            type(Key.UP, modifier=KeyModifier.CTRL)

        after_scroll_content_exists = exists(reader_view_content_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert after_scroll_content_exists is True, 'Scroll up and down using ctrl + up/down keys is successful.'

        # Scroll up and down using space bar
        before_scroll_content_exists = exists(reader_view_content_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert before_scroll_content_exists is True, 'Content before scrolling using space bar is on the page'

        try:
            type(Key.SPACE)
            after_scroll_content_disappeared = wait_vanish(reader_view_content_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
            assert after_scroll_content_disappeared is True, 'Scroll up and down using space bar is successful.'
        except FindError:
            raise FindError('Content is still on the page after scrolling')

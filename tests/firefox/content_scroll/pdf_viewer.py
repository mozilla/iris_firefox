# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Scrolling works properly while in PDF Viewer.',
        test_case_id='4663',
        test_suite_id='102',
        locale=['en-US']
    )
    def run(self, firefox):

        content_scroll_pattern = Pattern('pdf_content.png')
        after_scroll_content_pattern = Pattern('pdf_content_normal_mode.png')
        pdf_logo_pattern = Pattern('pdf_logo.png')
        presentation_mode_icon_pattern = Pattern('presentation_mode_icon.png')
        presentation_mode_content_pattern = Pattern('presentation_mode_content.png').similar(0.6)
        presentation_mode_enabled_pattern = Pattern('presentation_mode_enabled.png')
        after_scroll_content_presentation_mode_pattern = Pattern('pdf_content_presentation_mode.png').similar(0.6)

        if OSHelper.is_windows():
            screen_height = Screen.SCREEN_HEIGHT
        elif OSHelper.is_mac():
            screen_height = 100
        else:
            screen_height = 10

        pdf_file = self.get_asset_path('pdf.pdf')

        navigate(pdf_file)

        # Normal mode scrolling
        pdf_logo_exists = exists(pdf_logo_pattern, Settings.FIREFOX_TIMEOUT)
        assert pdf_logo_exists is True, 'PDF url loaded successfully'

        click(pdf_logo_pattern)

        after_scroll_content_exists = \
            scroll_until_pattern_found(after_scroll_content_pattern, Mouse().scroll,
                                       (None, -screen_height), 100, FirefoxSettings.TINY_FIREFOX_TIMEOUT/2)
        assert after_scroll_content_exists is True, 'Scroll Down using mouse wheel is successful'

        before_scroll_content_exists = \
            scroll_until_pattern_found(content_scroll_pattern, Mouse().scroll, (None, screen_height), 100,
                                       FirefoxSettings.TINY_FIREFOX_TIMEOUT/2)
        assert before_scroll_content_exists is True, 'Scroll Up using mouse wheel is successful'

        # Presentation mode scrolling
        presentation_mode_icon_exists = exists(presentation_mode_icon_pattern)
        assert presentation_mode_icon_exists is True, 'Presentation mode is available'

        click(presentation_mode_icon_pattern)

        presentation_mode_enabled_exists = exists(presentation_mode_enabled_pattern)
        assert presentation_mode_enabled_exists is True, 'Presentation Mode is successfully enabled'

        if OSHelper.is_linux():
            value = FirefoxSettings.TINY_FIREFOX_TIMEOUT
            screen_height = 1
        else:
            value = FirefoxSettings.TINY_FIREFOX_TIMEOUT

        after_scroll_content_exists = \
            scroll_until_pattern_found(after_scroll_content_presentation_mode_pattern, Mouse().scroll,
                                       (0, -screen_height), 100, value)
        assert after_scroll_content_exists, 'Scroll Down using mouse wheel is successful'

        before_scroll_content_exists = \
            scroll_until_pattern_found(presentation_mode_content_pattern, Mouse().scroll, (0, screen_height), 100,
                                       value)
        assert before_scroll_content_exists, 'Scroll Up using mouse wheel is successful'

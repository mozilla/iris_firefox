# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Scrolling works properly while in PDF Viewer.'
        self.test_case_id = '4663'
        self.test_suite_id = '102'
        self.locales = ['en-US']

    def run(self):

        content_scroll_pattern = Pattern('pdf_content.png')
        after_scroll_content_pattern = Pattern('pdf_content_normal_mode.png')
        pdf_logo_pattern = Pattern('pdf_logo.png')
        presentation_mode_icon_pattern = Pattern('presentation_mode_icon.png')
        presentation_mode_content_pattern = Pattern('presentation_mode_content.png').similar(0.6)
        presentation_mode_enabled_pattern = Pattern('presentation_mode_enabled.png')
        after_scroll_content_presentation_mode_pattern = Pattern('pdf_content_presentation_mode.png').similar(0.6)

        if Settings.is_windows():
            screen_height = SCREEN_HEIGHT
        else:
            screen_height = 10

        pdf_file = self.get_asset_path('pdf.pdf')
        navigate(pdf_file)

        # Normal mode scrolling
        pdf_logo_exists = exists(pdf_logo_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, pdf_logo_exists, 'PDF url loaded successfully')
        click(pdf_logo_pattern)

        after_scroll_content_exists = \
            scroll_until_pattern_found(after_scroll_content_pattern, scroll,
                                       (-screen_height, None), 100, DEFAULT_UI_DELAY)
        assert_true(self, after_scroll_content_exists, 'Scroll Down using mouse wheel is successful')

        before_scroll_content_exists = \
            scroll_until_pattern_found(content_scroll_pattern, scroll, (screen_height, None), 100, DEFAULT_UI_DELAY)
        assert_true(self, before_scroll_content_exists,
                    'Scroll Up using mouse wheel is successful')

        # Presentation mode scrolling
        presentation_mode_icon_exists = exists(presentation_mode_icon_pattern, DEFAULT_UI_DELAY)
        assert_true(self, presentation_mode_icon_exists, 'Presentation mode is available')
        click(presentation_mode_icon_pattern)

        presentation_mode_enabled_exists = exists(presentation_mode_enabled_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, presentation_mode_enabled_exists, 'Presentation Mode is successfully enabled')

        if Settings.is_linux():
            value = DEFAULT_UI_DELAY_LONG
            screen_height = 1
        else:
            value = DEFAULT_UI_DELAY

        after_scroll_content_exists = \
            scroll_until_pattern_found(after_scroll_content_presentation_mode_pattern, scroll,
                                       (-screen_height, None), 100, value)
        assert_true(self, after_scroll_content_exists, 'Scroll Down using mouse wheel is successful')

        before_scroll_content_exists = \
            scroll_until_pattern_found(presentation_mode_content_pattern, scroll, (screen_height, None), 100, value)
        assert_true(self, before_scroll_content_exists, 'Scroll Up using mouse wheel is successful')

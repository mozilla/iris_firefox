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
        pdf_logo_pattern = Pattern('pdf_logo.png')
        presentation_mode_icon_pattern = Pattern('presentation_mode_icon.png')
        presentation_mode_content = Pattern('presentation_mode_content.png')

        scroll_height = SCREEN_HEIGHT

        pdf_file = self.get_asset_path('pdf.pdf')
        navigate(pdf_file)

        pdf_logo_exists = exists(pdf_logo_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, pdf_logo_exists, 'PDF url loaded successfully.')

        # Scroll up and down using mouse wheel
        before_scroll_content_exists = exists(content_scroll_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, before_scroll_content_exists, 'Content before scrolling using mouse wheel is on the page')

        click(pdf_logo_pattern)
        [scroll(-scroll_height) for _ in range(3)]
        try:
            wait_vanish(content_scroll_pattern, DEFAULT_FIREFOX_TIMEOUT)
        except FindError:
            raise FindError('Content is still on the page after scrolling')
        [scroll(scroll_height) for _ in range(3)]

        after_scroll_content_exists = exists(content_scroll_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, after_scroll_content_exists, 'Scroll up and down using mouse wheel is successful.')

        # Scrolling using presentation mode
        presentation_mode_icon_exists = exists(presentation_mode_icon_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, presentation_mode_icon_exists, 'Presentation Mode icon is on the page')
        click(presentation_mode_icon_pattern)

        try:
            presentation_mode_enabled = wait_vanish(presentation_mode_icon_pattern)
            assert_true(self, presentation_mode_enabled, 'Presentation Mode is successfully enabled')
        except FindError:
            raise FindError('Presentation Mode icon is still on the page')

        before_scroll_content_exists = exists(presentation_mode_content, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, before_scroll_content_exists,
                    'Content before scrolling in Presentation Mode is on the page')

        [scroll(-scroll_height) for _ in range(3)]
        try:
            wait_vanish(presentation_mode_content, DEFAULT_FIREFOX_TIMEOUT)
        except FindError:
            raise FindError('Content is still on the page after scrolling in Presentation Mode')
        [scroll(scroll_height) for _ in range(3)]

        after_scroll_content_exists = exists(presentation_mode_content, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, after_scroll_content_exists,
                    'Scroll up and down using mouse wheel is successful in Presentation Mode.')

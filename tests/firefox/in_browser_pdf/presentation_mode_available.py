# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Presentation mode is available for any eligible PDF file via pdf.js',
        test_case_id='3930',
        test_suite_id='65',
        locales=Locales.ENGLISH
    )
    def test_run(self, firefox):
        rotate_counterclockwise_option_pattern = Pattern('rotate_counterclockwise_option.png')
        last_page_contents_rotated_pattern = Pattern('last_page_contents_rotated.png')
        exit_fullscreen_button_pattern = Pattern('exit_fullscreen_popup_button.png')
        view_background_image_option_pattern = Pattern('view_background_image.png')
        first_page_document_contents_pattern = Pattern('first_page_contents.png')
        go_to_first_page_option_pattern = Pattern('go_to_first_page_option.png')
        exit_full_screen_option_pattern = Pattern('exit_full_screen_option.png')
        rotate_clockwise_option_pattern = Pattern('rotate_clockwise_option.png')
        take_screenshot_option_pattern = Pattern('take_screenshot_option.png')
        go_to_last_page_option_pattern = Pattern('go_to_last_page_option.png')
        inspect_element_option_pattern = Pattern('inspect_element_option.png')
        presentation_button_pattern = Pattern('presentation_mode_button.png')
        save_page_as_option_pattern = Pattern('save_page_as_option.png')
        last_page_document_contents = Pattern('last_page_contents.png')
        view_page_info_pattern = Pattern('view_page_info_option.png')
        select_all_option_pattern = Pattern('select_all_option.png')

        change_preference('pdfjs.defaultZoomValue', '100')

        pdf_file_path = self.get_asset_path('pdf.pdf')
        navigate(pdf_file_path)

        document_opened = exists(first_page_document_contents_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert document_opened, 'Document successfully opened in pdf viewer'

        presentation_mode_button_available = exists(presentation_button_pattern)
        assert presentation_mode_button_available, '\'Presentation mode\' button available'

        click(presentation_button_pattern)

        full_screen_popup_displayed = exists(exit_fullscreen_button_pattern)
        navigation_buttons_disappeared = not exists(presentation_button_pattern)
        assert full_screen_popup_displayed and navigation_buttons_disappeared,\
            'Presentation mode can be successfully enabled'

        try:
            full_screen_popup_vanished = wait_vanish(exit_fullscreen_button_pattern,
                                                     FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
            assert full_screen_popup_vanished, '\'Full screen\' popup successfully vanished'
        except FindError:
            raise FindError('\'Full screen\' popup did not vanish')

        right_click(Location(Screen.SCREEN_WIDTH // 2, Screen.SCREEN_HEIGHT // 2))

        go_to_last_page_option_available = exists(go_to_first_page_option_pattern)
        assert go_to_last_page_option_available, \
            '\'Go to last page\' option available in context menu after right-click at the document area'

        click(go_to_last_page_option_pattern)

        last_page_opened = exists(last_page_document_contents)
        assert last_page_opened, '\'Go to last page\' option works correctly'

        right_click(Location(Screen.SCREEN_WIDTH // 2, Screen.SCREEN_HEIGHT // 2))

        rotate_clockwise_option_available = exists(rotate_clockwise_option_pattern)
        assert rotate_clockwise_option_available, \
            '\'Rotate clockwise\' option available in context menu after right-click at the document area'

        click(rotate_clockwise_option_pattern)

        page_contents_rotated = exists(last_page_contents_rotated_pattern)
        assert page_contents_rotated, '\'Rotate clockwise\' option works correctly'

        right_click(Location(Screen.SCREEN_WIDTH // 2, Screen.SCREEN_HEIGHT // 2))

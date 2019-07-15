# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description='Test case: Image-rich PDF files can be properly opened and navigated through by pdf.js.',
        locale=[Locales.ENGLISH],
        test_case_id='3933',
        test_suite_id='65',
    )
    def test_run(self, firefox):
        zoom_in_button_pattern = Pattern('zoom_in_button.png')
        zoom_out_button_pattern = Pattern('zoom_out_button.png')
        next_page_button_pattern = Pattern('next_page_button.png')
        previous_page_button_pattern = Pattern('previous_page_button.png')
        image_rich_pdf_zoomed_in_pattern = Pattern('image_rich_pdf_zoomed_in.png')
        jump_to_page_field_pattern = Pattern('jump_to_page_filed_image_rich_pdf.png')
        image_rich_pdf_last_page_contents_pattern = Pattern('image_rich_pdf_last_page_contents.png')
        image_rich_pdf_first_page_contents_pattern = Pattern('image_rich_pdf_first_page_contents.png')
        image_rich_pdf_third_page_contents_pattern = Pattern('image_rich_pdf_third_page_contents.png')

        change_preference('pdfjs.defaultZoomValue', '100')

        if OSHelper.is_linux():
            scroll_height = -10
        else:
            scroll_height = -50

        pdf_file_path = self.get_asset_path('img_rich_pdf.pdf')
        navigate(pdf_file_path)

        assert exists(image_rich_pdf_first_page_contents_pattern, FirefoxSettings.HEAVY_SITE_LOAD_TIMEOUT), \
            'The document is loaded and displayed properly using Firefox\'s pdf.js'

        click(image_rich_pdf_first_page_contents_pattern)  # To make mouse scroll possible

        scrolling_down_works = scroll_until_pattern_found(image_rich_pdf_third_page_contents_pattern, scroll,
                                                          (scroll_height,), num_of_scroll_iterations=50)
        assert scrolling_down_works, 'Scrolling down via mouse wheel works properly'

        scrolling_up_works = scroll_until_pattern_found(image_rich_pdf_first_page_contents_pattern, scroll,
                                                        (50,), num_of_scroll_iterations=50)
        assert scrolling_up_works, 'Scrolling up via mouse wheel works properly'

        arrow_down_navigation_works = scroll_until_pattern_found(image_rich_pdf_third_page_contents_pattern,
                                                                 type, (Key.DOWN,), num_of_scroll_iterations=50)
        assert arrow_down_navigation_works, 'Navigation via \'Arrow down\' key works properly'

        arrow_up_navigation_works = scroll_until_pattern_found(image_rich_pdf_first_page_contents_pattern,
                                                               type, (Key.UP,), num_of_scroll_iterations=50)
        assert arrow_up_navigation_works, 'Navigation via \'Arrow up\' key works properly'

        [type(Key.RIGHT) for _ in range(2)]

        assert exists(image_rich_pdf_third_page_contents_pattern), 'Navigation via \'Arrow right\' key works properly'

        [type(Key.LEFT) for _ in range(2)]

        assert exists(image_rich_pdf_first_page_contents_pattern), 'Navigation via \'Arrow left\' key works properly'

        assert scroll_until_pattern_found(image_rich_pdf_third_page_contents_pattern, type, (Key.PAGE_DOWN,)), \
            'Navigation via \'Page Down\' key works properly'

        assert scroll_until_pattern_found(image_rich_pdf_first_page_contents_pattern, type, (Key.PAGE_UP,)), \
            'Navigation via \'Page Up\' key works properly'

        type(Key.END)

        assert image_rich_pdf_last_page_contents_pattern, 'Navigation via \'End\' key works properly'

        type(Key.HOME)

        assert image_rich_pdf_first_page_contents_pattern, 'Navigation via \'Home\' key works properly'

        assert exists(next_page_button_pattern), '\'Next page\' button available'

        [click(next_page_button_pattern) for _ in range(2)]

        assert exists(image_rich_pdf_third_page_contents_pattern), \
            'By clicking the \'Next page\' button, the current view moves to the previous page'

        assert exists(previous_page_button_pattern), '\'Previous page\' button available'

        [click(previous_page_button_pattern) for _ in range(2)]

        assert exists(image_rich_pdf_first_page_contents_pattern), \
            'By clicking the \'Previous page\' button, the current view moves to the previous page'

        assert exists(jump_to_page_field_pattern), '\'Jump to page\' field available'

        click(jump_to_page_field_pattern)

        paste("3")

        type(Key.ENTER)

        assert exists(image_rich_pdf_third_page_contents_pattern), '\'Jump to page\' field works as expected'

        assert exists(zoom_in_button_pattern), '\'Zoom in\' button available'

        [click(zoom_in_button_pattern) for _ in range(3)]

        assert exists(image_rich_pdf_zoomed_in_pattern), '\'Zoom in\' button works as expected'

        assert exists(zoom_out_button_pattern), '\'Zoom out\' button available'

        [click(zoom_out_button_pattern) for _ in range(3)]

        assert exists(image_rich_pdf_third_page_contents_pattern), '\'Zoom out\' button works as expected'

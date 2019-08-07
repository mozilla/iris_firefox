# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    
    @pytest.mark.details(
        description='Zooming in and out of a PDF file works properly using pdf.js',
        locale=[Locales.ENGLISH],
        test_case_id='3928',
        test_suite_id='65'
    )
    def test_run(self, firefox):
        pdf_file_page_contents_zoomed_in_pattern = Pattern('pdf_file_page_contents_zoomed_in.png')
        pdf_file_page_contents_pattern = Pattern('pdf_file_page_contents.png')
        zoom_out_button_pattern = Pattern('zoom_out_button.png')
        zoom_in_button_pattern = Pattern('zoom_in_button.png')

        change_preference('pdfjs.defaultZoomValue', '100')

        if OSHelper.is_mac():
            key_used_in_scroll_zoom = Key.CMD
        else:
            key_used_in_scroll_zoom = Key.CTRL

        pdf_file_path = self.get_asset_path('pdf.pdf')

        navigate(pdf_file_path)

        pdf_document_opened = exists(pdf_file_page_contents_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert pdf_document_opened, 'The PDF file successfully opened in In-browser PDF viewer'

        zoom_in_button_available = exists(zoom_in_button_pattern)
        assert zoom_in_button_available, '\'Zoom in (+)\' button available in In-browser PDF viewer'

        [click(zoom_in_button_pattern) for _ in range(3)]

        pdf_document_zoomed_in = exists(pdf_file_page_contents_zoomed_in_pattern)
        assert pdf_document_zoomed_in, 'The PDF file is successfully zoomed in via \'+\' button'

        zoom_out_button_available = exists(zoom_out_button_pattern)
        assert zoom_out_button_available, '\'Zoom out (-)\' button available in In-browser PDF viewer'

        [click(zoom_out_button_pattern) for _ in range(3)]

        pdf_document_zoomed_out = exists(pdf_file_page_contents_pattern)
        assert pdf_document_zoomed_out, 'The PDF file is successfully zoomed out via \'-\' button'

        [type('+', modifier=KeyModifier.CTRL) for _ in range(3)]

        pdf_document_zoomed_in = exists(pdf_file_page_contents_zoomed_in_pattern)
        assert pdf_document_zoomed_in, 'The PDF file is successfully zoomed in via shortcut (\'Ctrl/Control\' + \'+\')'

        [type('-', modifier=KeyModifier.CTRL) for _ in range(3)]

        pdf_document_zoomed_out = exists(pdf_file_page_contents_pattern)
        assert pdf_document_zoomed_out, \
            'The PDF file is successfully zoomed out via shortcut (\'Ctrl/Control\' + \'-\')'

        key_down(key_used_in_scroll_zoom)
        pdf_document_zoomed_in = scroll_until_pattern_found(pdf_file_page_contents_zoomed_in_pattern,
                                                            Mouse().scroll, (0, 1,))
        key_up(key_used_in_scroll_zoom)

        assert pdf_document_zoomed_in, 'The PDF file is successfully zoomed in via Ctrl/Command + mouse scroll'

        key_down(key_used_in_scroll_zoom)
        pdf_document_zoomed_out = scroll_until_pattern_found(pdf_file_page_contents_zoomed_in_pattern,
                                                             Mouse().scroll, (0, -1,))
        key_up(key_used_in_scroll_zoom)

        assert pdf_document_zoomed_out, 'The PDF file is successfully zoomed out via Ctrl/Command + mouse scroll'

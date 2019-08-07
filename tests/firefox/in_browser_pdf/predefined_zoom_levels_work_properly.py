# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Predefined zoom levels are being applied properly to PDF files via pdf.js',
        test_case_id='3929',
        test_suite_id='65',
        locales=Locales.ENGLISH
    )
    def test_run(self, firefox):
        actual_size_zoom_level_option_pattern = Pattern('actual_size_zoom_level_option.png')
        page_width_zoom_level_option_pattern = Pattern('page_width_zoom_level_option.png')
        automatic_zoom_level_option_pattern = Pattern('automatic_zoom_level_option.png')
        page_fit_zoom_level_option_pattern = Pattern('page_fit_zoom_level_option.png')
        pdf_file_first_page_contents_pattern = Pattern('pdf_file_page_contents.png')
        zoom_levels_dropdown_pattern = Pattern('zoom_levels_dropdown.png')
        actual_size_zoom_selected_pattern = Pattern('actual_size_dropdown.png')
        automatic_zoom_selected_pattern = Pattern('automatic_zoom_dropdown.png')
        page_fit_zoom_selected_pattern = Pattern('page_fit_dropdown.png')
        page_width_zoom_selected_pattern = Pattern('page_width_dropdown.png')
        page_width_document_contents_pattern = Pattern('page_width_document_contents.png')
        page_fit_document_contents_pattern = Pattern('page_fit_document_contents.png')
        automatic_zoom_document_contents_pattern = Pattern('auto_zoom_document_contents.png')
        actual_size_document_contents_pattern = Pattern('first_page_contents.png')

        change_preference('pdfjs.defaultZoomValue', '100')

        pdf_file_path = self.get_asset_path('pdf.pdf')
        navigate(pdf_file_path)

        pdf_file_opened = exists(pdf_file_first_page_contents_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert pdf_file_opened, 'PDF document successfully opened in pdf.js'

        zoom_levels_dropdown_available = exists(zoom_levels_dropdown_pattern)
        assert zoom_levels_dropdown_available, '\'Zoom\' dropdown available'

        click(zoom_levels_dropdown_pattern)

        page_width_zoom_option_available = exists(page_width_zoom_level_option_pattern)
        assert page_width_zoom_option_available, '\'Page Width\' zoom option available in \'Zoom\' dropdown'

        click(page_width_zoom_level_option_pattern)

        page_width_zoom_level_applied = exists(page_width_document_contents_pattern)
        assert page_width_zoom_level_applied, '\'Page Width\' zoom level successfully applied'

        page_width_zoom_selected_on_dropdown = exists(page_width_zoom_selected_pattern)
        assert page_width_zoom_selected_on_dropdown, \
            '\'Page width\' displayed as current zoom level on \'Zoom\' dropdown after applying'

        click(page_width_zoom_selected_pattern)

        page_fit_zoom_option_available = exists(page_fit_zoom_level_option_pattern)
        assert page_fit_zoom_option_available, '\'Page Fit\' zoom option available in \'Zoom\' dropdown'

        click(page_fit_zoom_level_option_pattern)

        page_fit_zoom_level_applied = exists(page_fit_document_contents_pattern)
        assert page_fit_zoom_level_applied, '\'Page Fit\' zoom level successfully applied'

        page_fit_zoom_selected_on_dropdown = exists(page_fit_zoom_selected_pattern)
        assert page_fit_zoom_selected_on_dropdown, \
            '\'Page fit\' displayed as current zoom level on \'Zoom\' dropdown after applying'

        click(page_fit_zoom_selected_pattern)

        actual_size_zoom_option_available = exists(actual_size_zoom_level_option_pattern)
        assert actual_size_zoom_option_available, '\'Actual Size\' zoom option available in \'Zoom\' dropdown'

        click(actual_size_zoom_level_option_pattern)

        actual_size_zoom_level_applied = exists(actual_size_document_contents_pattern)
        assert actual_size_zoom_level_applied, '\'Actual Size\' zoom level successfully applied'

        page_width_zoom_selected_on_dropdown = exists(actual_size_zoom_selected_pattern)
        assert page_width_zoom_selected_on_dropdown, \
            '\'Actual Size\' displayed as current zoom level on \'Zoom\' dropdown after applying'

        click(actual_size_zoom_selected_pattern)

        automatic_zoom_option_available = exists(automatic_zoom_level_option_pattern)
        assert automatic_zoom_option_available, '\'Automatic zoom\' option available in \'Zoom\' dropdown'

        click(automatic_zoom_level_option_pattern)

        automatic_zoom_level_applied = exists(automatic_zoom_document_contents_pattern)
        assert automatic_zoom_level_applied, '\'Automatic zoom\' zoom level successfully applied'

        automatic_zoom_selected_on_dropdown = exists(automatic_zoom_selected_pattern)
        assert automatic_zoom_selected_on_dropdown, \
            '\'Automatic zoom\' displayed as current zoom level on \'Zoom\' dropdown after applying'

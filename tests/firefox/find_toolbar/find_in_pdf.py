# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description='Search on a PDF page',
        locale=['en-US'],
        test_case_id='127271',
        test_suite_id='2085',
    )
    def run(self, firefox):
        pdf_logo_pattern = Pattern('pdf_page_logo.png').similar(0.6)
        first_occurrence_highlighted_pattern = Pattern('first_printer_highlight.png')
        second_occurrence_highlighted_pattern = Pattern('second_printer_highlight.png')
        second_occurrence_unhighlighted_pattern = Pattern('second_printer_white.png')

        # Open Firefox and open a [PDF page]
        test_page_local = self.get_asset_path('pdf.pdf')
        navigate(test_page_local)

        navigated_to_pdf_url = exists(pdf_logo_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert navigated_to_pdf_url, 'PDF URL loaded successfully.'

        # Open the Find Toolbar
        open_find()
        edit_select_all()
        edit_delete()

        find_toolbar_is_opened = exists(FindToolbar.FINDBAR_TEXTBOX, FirefoxSettings.FIREFOX_TIMEOUT)
        assert find_toolbar_is_opened, 'The Find Toolbar is successfully displayed'

        # Search for a term that appears on the page
        type('printer')
        type(Key.ENTER)

        first_occurrence_highlighted = exists(first_occurrence_highlighted_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert first_occurrence_highlighted, 'The first occurrence is highlighted'

        second_occurrence_unhighlighted = exists(second_occurrence_unhighlighted_pattern,
                                                 FirefoxSettings.FIREFOX_TIMEOUT)
        assert second_occurrence_unhighlighted, 'The second occurrence is not highlighted'

        # Navigate through found items
        find_next()

        second_occurrence_highlighted = exists(second_occurrence_highlighted_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert second_occurrence_highlighted, 'The second occurrence is highlighted'

        # Scroll the page up and down
        find_previous()
        first_occurrence_before_scrolling_highlighted = exists(first_occurrence_highlighted_pattern,
                                                               FirefoxSettings.FIREFOX_TIMEOUT)
        assert first_occurrence_before_scrolling_highlighted, 'The first occurrence is highlighted before scrolling'

        repeat_key_down(4)
        repeat_key_up(4)

        first_occurrence_after_scrolling_highlighted = exists(first_occurrence_highlighted_pattern,
                                                              FirefoxSettings.FIREFOX_TIMEOUT)
        assert first_occurrence_after_scrolling_highlighted, 'The first occurrence is highlighted after scrolling'

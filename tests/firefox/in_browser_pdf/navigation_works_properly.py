# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Navigating through a PDF file works properly via pdf.js',
        test_case_id='3927',
        test_suite_id='65',
        locales=Locales.ENGLISH
    )
    def test_run(self, firefox):
        pdf_file_last_page_contents_rotated_pattern = Pattern('last_page_contents_rotated.png')
        rotate_counterclockwise_button_pattern = Pattern('rotate_counterclockwise_button.png')
        doc_properties_close_button_pattern = Pattern('document_properties_close_button.png')
        document_properties_filename_pattern = Pattern('document_properties_info.png')
        document_properties_button_pattern = Pattern('document_properties_button.png')
        introduction_chapter_pattern = Pattern('introduction_chapter_headline.png')
        last_page_text_contents_pattern = Pattern('last_page_text_contents.png')
        go_to_first_page_button_pattern = Pattern('go_to_first_page_button.png')
        rotate_clockwise_button_pattern = Pattern('rotate_clockwise_button.png')
        pdf_file_last_page_contents_pattern = Pattern('last_page_contents.png')
        go_to_last_page_button_pattern = Pattern('go_to_last_page_button.png')
        pdf_file_page_contents_pattern = Pattern('first_page_contents.png')
        previous_page_button_pattern = Pattern('previous_page_button.png')
        history_chapter_pattern = Pattern('history_chapter_headline.png')
        text_selection_tool_button = Pattern('text_selection_tool.png')
        jump_to_page_field_pattern = Pattern('jump_to_page_field.png')
        next_page_button_pattern = Pattern('next_page_button.png')
        text_selected_pattern = Pattern('text_selected.png')
        hand_tool_button_pattern = Pattern('hand_tool.png')
        tools_button_pattern = Pattern('tools_button.png')

        change_preference('pdfjs.defaultZoomValue', '100')

        pdf_file_path = self.get_asset_path('pdf.pdf')
        navigate(pdf_file_path)

        pdf_document_opened = exists(pdf_file_page_contents_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert pdf_document_opened, 'The PDF file successfully opened in In-browser PDF viewer'

        arrow_down_navigation_works = scroll_until_pattern_found(introduction_chapter_pattern, type, (Key.DOWN,),
                                                                 num_of_scroll_iterations=20)
        assert arrow_down_navigation_works, 'Navigation via \'Arrow down\' key works properly'

        arrow_up_navigation_works = scroll_until_pattern_found(pdf_file_page_contents_pattern, type, (Key.UP,),
                                                               num_of_scroll_iterations=20)
        assert arrow_up_navigation_works, 'Navigation via \'Arrow up\' key works properly'

        [type(Key.RIGHT) for _ in range(2)]
        type(Key.DOWN)

        arrow_right_navigation_works = exists(history_chapter_pattern)
        assert arrow_right_navigation_works, 'Navigation via \'Arrow right\' key works properly'

        type(Key.LEFT)

        arrow_left_navigation_works = exists(introduction_chapter_pattern)
        assert arrow_left_navigation_works, 'Navigation via \'Arrow left\' key works properly'

        page_up_navigation_works = scroll_until_pattern_found(pdf_file_page_contents_pattern, type, (Key.PAGE_UP,))
        assert page_up_navigation_works, 'Navigation via \'Page Up\' key works properly'

        page_down_navigation_works = scroll_until_pattern_found(introduction_chapter_pattern, type, (Key.PAGE_DOWN,))
        assert page_down_navigation_works, 'Navigation via \'Page Down\' key works properly'

        type(Key.HOME)

        home_button_navigation_works = exists(pdf_file_page_contents_pattern)
        assert home_button_navigation_works, 'Navigation via \'Home\' key works properly'

        type(Key.END)

        end_button_navigation_works = exists(pdf_file_last_page_contents_pattern)
        assert end_button_navigation_works, 'Navigation via \'End\' key works properly'

        previous_page_button_available = exists(previous_page_button_pattern)
        assert previous_page_button_available, '\'Previous page\' button available'

        [click(previous_page_button_pattern) for _ in range(2)]
        type(Key.DOWN)

        navigation_via_previous_page_button_works = exists(history_chapter_pattern)
        assert navigation_via_previous_page_button_works, \
            'By clicking the \'Previous page\' button, the current view moves to the previous page'

        next_page_button_available = exists(next_page_button_pattern)
        assert next_page_button_available, '\'Next page\' button available'

        [click(next_page_button_pattern) for _ in range(2)]

        navigation_via_next_page_button_works = exists(pdf_file_last_page_contents_pattern)
        assert navigation_via_next_page_button_works, \
            'By clicking the \'Previous page\' button, the current view moves to the previous page'

        tools_button_available = exists(tools_button_pattern)
        assert tools_button_available, '\'Tools\' button available in In-browser PDF viewer'

        click(tools_button_pattern)

        go_to_first_page_button_available = exists(go_to_first_page_button_pattern)
        assert go_to_first_page_button_available, '\'Go to first page\' button available in \'Tools\' menu'

        click(go_to_first_page_button_pattern)

        navigation_via_go_to_first_page_button_works = exists(pdf_file_page_contents_pattern)
        assert navigation_via_go_to_first_page_button_works, \
            'Navigation via \'Go to first page\' button from \'Tools\' menu works properly'

        tools_button_available = exists(tools_button_pattern)
        assert tools_button_available, '\'Tools\' button available in In-browser PDF viewer'

        click(tools_button_pattern)

        go_to_last_page_button_available = exists(go_to_last_page_button_pattern)
        assert go_to_last_page_button_available, '\'Go to last page\' button available in \'Tools\' menu'

        click(go_to_last_page_button_pattern)

        navigation_via_go_to_last_page_button_works = exists(pdf_file_last_page_contents_pattern)
        assert navigation_via_go_to_last_page_button_works, \
            'Navigation via \'Go to last page\' button from \'Tools\' menu works properly'

        tools_button_available = exists(tools_button_pattern)
        assert tools_button_available, '\'Tools\' button available in In-browser PDF viewer'

        click(tools_button_pattern)

        rotate_clockwise_button_available = exists(rotate_clockwise_button_pattern)
        assert rotate_clockwise_button_available, '\'Rotate clockwise\' button available in \'Tools\' menu'

        click(rotate_clockwise_button_pattern)

        page_contents_rotated = exists(pdf_file_last_page_contents_rotated_pattern)
        assert page_contents_rotated, 'Page contents rotated via \'Rotate clockwise\' button'

        rotate_counterclockwise_button_available = exists(rotate_counterclockwise_button_pattern)
        assert rotate_counterclockwise_button_available, \
            '\'Tools\' menu didn\'t close after rotating page clockwise and contains \'Rotate counterclockwise\' button'

        click(rotate_counterclockwise_button_pattern)

        page_rotated_back = exists(pdf_file_last_page_contents_pattern)
        assert page_rotated_back, 'Page contents rotated via \'Rotate counterclockwise\' button'

        type(Key.ESC)

        tools_button_available = exists(tools_button_pattern)
        assert tools_button_available, '\'Tools\' button available in In-browser PDF viewer'

        click(tools_button_pattern)

        hand_tool_available = exists(hand_tool_button_pattern)
        assert hand_tool_available, '\'Hand tool\' button available in \'Tools\' menu'

        click(hand_tool_button_pattern)

        drag_drop(pdf_file_last_page_contents_pattern, Location(Screen.SCREEN_WIDTH // 2, Screen.SCREEN_HEIGHT))

        try:
            content_scrolled_via_hand_tool = wait_vanish(pdf_file_last_page_contents_pattern)
        except FindError:
            raise FindError('Page contents didn\'t scroll using \'Hand tool\'')

        assert content_scrolled_via_hand_tool, 'Scrolling via \'Hand tool\' works properly'

        tools_button_available = exists(tools_button_pattern)
        assert tools_button_available, '\'Tools\' button available in In-browser PDF viewer'

        click(tools_button_pattern)

        text_selection_tool_available = exists(text_selection_tool_button)
        assert text_selection_tool_available, '\'Text selection tool\' button available in \'Tools\' menu'

        click(text_selection_tool_button)

        text_to_select_present_on_page = exists(last_page_text_contents_pattern)
        assert text_to_select_present_on_page, 'Text to select is available on the page'

        double_click(last_page_text_contents_pattern)

        text_selection_tool_works = exists(text_selected_pattern)
        assert text_selection_tool_works, '\'Text selection tool\' works'

        tools_button_available = exists(tools_button_pattern)
        assert tools_button_available, '\'Tools\' button available in In-browser PDF viewer'

        click(tools_button_pattern)

        document_properties_button_available = exists(document_properties_button_pattern)
        assert document_properties_button_available, '\'Document properties\' button available in \'Tools\' menu'

        click(document_properties_button_pattern)

        document_properties_opened = exists(document_properties_filename_pattern)
        assert document_properties_opened, '\'Document properties\' popup successfully opened'

        close_button_available = exists(doc_properties_close_button_pattern)
        assert close_button_available, '\'Close\' button available in \'Document properties\' popup'

        click(doc_properties_close_button_pattern)
        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)  # To prevent matching popup being opened while it closes

        document_properties_opened = exists(document_properties_filename_pattern)
        assert document_properties_opened is not True, '\'Document properties\' popup successfully closed'

        jump_to_page_field_available = exists(jump_to_page_field_pattern)
        assert jump_to_page_field_available, '\'Jump to page\' field available'

        click(jump_to_page_field_pattern)

        paste("1")

        type(Key.ENTER)

        first_page_opened = exists(pdf_file_page_contents_pattern)
        assert first_page_opened, 'The requested page number is shown using \'Jump to page\' field'

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.nightly.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description="Navigating through a PDF file in pdf.js",
        test_case_id="3927",
        test_suite_id="65",
        locales=Locales.ENGLISH,
        preferences={"pdfjs.defaultZoomValue": "100"},
        blocked_by={"id": "issue_4118", "platform": OSPlatform.LINUX},
    )
    def test_run(self, firefox):
        pdf_file_last_page_contents_rotated_pattern = Pattern(
            "last_page_contents_rotated.png"
        )
        rotate_counterclockwise_button_pattern = Pattern(
            "rotate_counterclockwise_button.png"
        ).similar(0.6)
        doc_properties_close_button_pattern = Pattern(
            "document_properties_close_button.png"
        ).similar(0.5)
        document_properties_filename_pattern = Pattern(
            "document_properties_info.png"
        ).similar(0.6)
        document_properties_button_pattern = Pattern(
            "document_properties_button.png"
        ).similar(0.6)
        introduction_chapter_pattern = Pattern("introduction_chapter_headline.png")
        last_page_text_contents_pattern = Pattern("last_page_text_contents.png")
        go_to_first_page_button_pattern = Pattern(
            "go_to_first_page_button.png"
        ).similar(0.6)
        rotate_clockwise_button_pattern = Pattern(
            "rotate_clockwise_button.png"
        ).similar(0.6)
        pdf_file_last_page_contents_pattern = Pattern("last_page_contents.png")
        go_to_last_page_button_pattern = Pattern("go_to_last_page_button.png").similar(
            0.6
        )
        pdf_file_page_contents_pattern = Pattern("first_page_contents.png")
        previous_page_button_pattern = Pattern("previous_page_button.png")
        history_chapter_pattern = Pattern("history_chapter_headline.png")
        text_selection_tool_button = Pattern("text_selection_tool.png").similar(0.6)
        jump_to_page_field_pattern = Pattern("jump_to_page_field.png").similar(0.6)
        next_page_button_pattern = Pattern("next_page_button.png")
        text_selected_pattern = Pattern("text_selected.png")
        hand_tool_button_pattern = Pattern("hand_tool.png").similar(0.6)
        tools_button_pattern = Pattern("tools_button.png").similar(0.6)

        region_top = Screen.TOP_THIRD
        region_right = Screen.RIGHT_HALF
        region_bottom = Screen.BOTTOM_HALF

        pdf_file_path = self.get_asset_path("pdf.pdf")
        navigate(pdf_file_path)

        pdf_document_opened = exists(
            pdf_file_page_contents_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT
        )
        assert (
            pdf_document_opened
        ), "The PDF file successfully opened in In-browser PDF viewer"

        arrow_down_navigation_works = scroll_until_pattern_found(
            introduction_chapter_pattern, type, (Key.DOWN,), num_of_scroll_iterations=20
        )
        assert (
            arrow_down_navigation_works
        ), "Navigation via 'Arrow down' key works properly"

        arrow_up_navigation_works = scroll_until_pattern_found(
            pdf_file_page_contents_pattern, type, (Key.UP,), num_of_scroll_iterations=20
        )
        assert arrow_up_navigation_works, "Navigation via 'Arrow up' key works properly"

        page_up_navigation_works = scroll_until_pattern_found(
            pdf_file_page_contents_pattern, type, (Key.PAGE_UP,)
        )
        assert page_up_navigation_works, "Navigation via 'Page Up' key works properly"

        page_down_navigation_works = scroll_until_pattern_found(
            introduction_chapter_pattern, type, (Key.PAGE_DOWN,)
        )
        assert (
            page_down_navigation_works
        ), "Navigation via 'Page Down' key works properly"

        type(Key.HOME)

        home_button_navigation_works = exists(
            pdf_file_page_contents_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert home_button_navigation_works, "Navigation via 'Home' key works properly"

        type(Key.END)

        end_button_navigation_works = exists(
            pdf_file_last_page_contents_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert end_button_navigation_works, "Navigation via 'End' key works properly"

        previous_page_button_available = region_top.exists(
            previous_page_button_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert previous_page_button_available, "'Previous page' button available"

        click(previous_page_button_pattern)
        time.sleep(Settings.DEFAULT_UI_DELAY)
        click(previous_page_button_pattern)
        time.sleep(Settings.DEFAULT_UI_DELAY)
        type(Key.DOWN)
        time.sleep(Settings.DEFAULT_UI_DELAY)
        type(Key.DOWN)
        time.sleep(Settings.DEFAULT_UI_DELAY)
        type(Key.DOWN)

        navigation_via_previous_page_button_works = exists(
            history_chapter_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert (
            navigation_via_previous_page_button_works
        ), "By clicking the 'Previous page' button, the current view moves to the previous page"

        next_page_button_available = region_top.exists(
            next_page_button_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert next_page_button_available, "'Next page' button available"

        click(next_page_button_pattern)
        time.sleep(Settings.DEFAULT_UI_DELAY)
        click(next_page_button_pattern)
        time.sleep(Settings.DEFAULT_UI_DELAY)

        navigation_via_next_page_button_works = exists(
            pdf_file_last_page_contents_pattern
        )
        assert (
            navigation_via_next_page_button_works
        ), "By clicking the 'Previous page' button, the current view moves to the previous page"

        tools_button_available = region_top.exists(
            tools_button_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert (
            tools_button_available
        ), "'Tools' button available in In-browser PDF viewer"

        click(tools_button_pattern)

        go_to_first_page_button_available = region_right.exists(
            go_to_first_page_button_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert (
            go_to_first_page_button_available
        ), "'Go to first page' button available in 'Tools' menu"

        click(go_to_first_page_button_pattern)

        navigation_via_go_to_first_page_button_works = exists(
            pdf_file_page_contents_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert (
            navigation_via_go_to_first_page_button_works
        ), "Navigation via 'Go to first page' button from 'Tools' menu works properly"

        tools_button_available = region_top.exists(
            tools_button_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert (
            tools_button_available
        ), "'Tools' button available in In-browser PDF viewer"

        click(tools_button_pattern)

        go_to_last_page_button_available = region_right.exists(
            go_to_last_page_button_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert (
            go_to_last_page_button_available
        ), "'Go to last page' button available in 'Tools' menu"

        click(go_to_last_page_button_pattern)

        navigation_via_go_to_last_page_button_works = exists(
            pdf_file_last_page_contents_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert (
            navigation_via_go_to_last_page_button_works
        ), "Navigation via 'Go to last page' button from 'Tools' menu works properly"

        tools_button_available = region_top.exists(
            tools_button_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert (
            tools_button_available
        ), "'Tools' button available in In-browser PDF viewer"

        click(tools_button_pattern)

        rotate_clockwise_button_available = region_right.exists(
            rotate_clockwise_button_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert (
            rotate_clockwise_button_available
        ), "'Rotate clockwise' button available in 'Tools' menu"

        click(rotate_clockwise_button_pattern)

        page_contents_rotated = exists(
            pdf_file_last_page_contents_rotated_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert (
            page_contents_rotated
        ), "Page contents rotated via 'Rotate clockwise' button"

        rotate_counterclockwise_button_available = region_right.exists(
            rotate_counterclockwise_button_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert (
            rotate_counterclockwise_button_available
        ), "'Tools' menu didn't close after rotating page clockwise and contains 'Rotate counterclockwise' button"

        click(rotate_counterclockwise_button_pattern)

        page_rotated_back = exists(
            pdf_file_last_page_contents_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert (
            page_rotated_back
        ), "Page contents rotated via 'Rotate counterclockwise' button"

        type(Key.ESC)

        tools_button_available = region_top.exists(
            tools_button_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert (
            tools_button_available
        ), "'Tools' button available in In-browser PDF viewer"

        click(tools_button_pattern)

        hand_tool_available = region_right.exists(
            hand_tool_button_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert hand_tool_available, "'Hand tool' button available in 'Tools' menu"

        click(hand_tool_button_pattern)
        time.sleep(Settings.DEFAULT_UI_DELAY)

        drag_drop(
            pdf_file_last_page_contents_pattern,
            Location(Screen.SCREEN_WIDTH // 2, Screen.SCREEN_HEIGHT),
        )

        try:
            content_scrolled_via_hand_tool = wait_vanish(
                pdf_file_last_page_contents_pattern, FirefoxSettings.FIREFOX_TIMEOUT
            )
        except FindError:
            raise FindError("Page contents didn't scroll using 'Hand tool'")

        assert (
            content_scrolled_via_hand_tool
        ), "Scrolling via 'Hand tool' works properly"

        tools_button_available = region_top.exists(
            tools_button_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert (
            tools_button_available
        ), "'Tools' button available in In-browser PDF viewer"

        click(tools_button_pattern)

        text_selection_tool_available = region_right.exists(
            text_selection_tool_button, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert (
            text_selection_tool_available
        ), "'Text selection tool' button available in 'Tools' menu"

        click(text_selection_tool_button)

        text_to_select_present_on_page = exists(
            last_page_text_contents_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert text_to_select_present_on_page, "Text to select is available on the page"

        double_click(last_page_text_contents_pattern)

        text_selection_tool_works = exists(
            text_selected_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert text_selection_tool_works, "'Text selection tool' works"

        tools_button_available = region_top.exists(
            tools_button_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )

        page_end()

        assert (
            tools_button_available
        ), "'Tools' button available in In-browser PDF viewer"

        click(tools_button_pattern)

        document_properties_button_available = region_right.exists(
            document_properties_button_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert (
            document_properties_button_available
        ), "'Document properties' button available in 'Tools' menu"

        click(document_properties_button_pattern)

        if not OSHelper.is_linux():
            document_properties_opened = exists(
                document_properties_filename_pattern, FirefoxSettings.FIREFOX_TIMEOUT
            )
            assert (
                document_properties_opened
            ), "'Document properties' popup successfully opened"

        close_button_available = region_bottom.exists(
            doc_properties_close_button_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert (
            close_button_available
        ), "'Close' button available in 'Document properties' popup"

        region_bottom.click(doc_properties_close_button_pattern)
        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)

        # To prevent matching popup being opened while it closes
        try:
            expected = region_bottom.wait_vanish(
                doc_properties_close_button_pattern, FirefoxSettings.FIREFOX_TIMEOUT
            )
            assert expected is True, "'Document properties' popup successfully closed"
        except FindError:
            raise FindError("The 'Document properties' popup did not close.")

        jump_to_page_field_available = region_top.exists(
            jump_to_page_field_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert jump_to_page_field_available, "'Jump to page' field available"

        click(jump_to_page_field_pattern)
        time.sleep(Settings.DEFAULT_UI_DELAY)

        paste("1")
        time.sleep(Settings.DEFAULT_UI_DELAY)

        type(Key.ENTER)

        first_page_opened = exists(
            pdf_file_page_contents_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
        assert (
            first_page_opened
        ), "The requested page number is shown using 'Jump to page' field"

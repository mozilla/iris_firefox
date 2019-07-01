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
        dialogue_window_cancel_button = History.CLearRecentHistory.CANCEL.similar(0.75)
        introduction_chapter_headline_pattern = Pattern('introduction_chapter_headline_pres_mode.png')
        last_page_contents_rotated_pattern = Pattern('last_page_contents_pres_mode_rotated.png')
        rotate_counterclockwise_option_pattern = Pattern('rotate_counterclockwise_option.png')
        first_page_contents_presentation_mode = Pattern('first_page_contents_pres_mode.png')
        dev_console_inspector_button_pattern = Pattern('dev_console_inspector_button.png')
        last_page_document_contents_pattern = Pattern('last_page_contents_pres_mode.png')
        exit_fullscreen_button_pattern = Pattern('exit_fullscreen_popup_button.png')
        first_page_document_contents_pattern = Pattern('first_page_contents.png')
        go_to_first_page_option_pattern = Pattern('go_to_first_page_option.png')
        exit_full_screen_option_pattern = Pattern('exit_full_screen_option.png')
        rotate_clockwise_option_pattern = Pattern('rotate_clockwise_option.png')
        go_to_last_page_option_pattern = Pattern('go_to_last_page_option.png')
        inspect_element_option_pattern = Pattern('inspect_element_option.png')
        presentation_button_pattern = Pattern('presentation_mode_button.png')
        close_devtools_button_pattern = Pattern('close_devtools_button.png')
        save_page_as_option_pattern = Pattern('save_page_as_option.png')
        view_page_info_pattern = Pattern('view_page_info_option.png')
        page_info_pattern = Pattern('page_info.png')

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

        if OSHelper.is_windows():
            scrolling_works = scroll_until_pattern_found(introduction_chapter_headline_pattern, scroll, (-100,))
        else:
            scrolling_works = scroll_until_pattern_found(introduction_chapter_headline_pattern, scroll, (-1,))

        assert scrolling_works, 'Navigation via mouse scroll works in presentation mode'

        right_click(Location(Screen.SCREEN_WIDTH // 2, Screen.SCREEN_HEIGHT // 2))

        go_to_last_page_option_available = exists(go_to_first_page_option_pattern,
                                                  FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert go_to_last_page_option_available, \
            '\'Go to last page\' option available in context menu after right-click at the document area'

        click(go_to_last_page_option_pattern)

        last_page_opened = exists(last_page_document_contents_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert last_page_opened, '\'Go to last page\' option works as expected'

        right_click(Location(Screen.SCREEN_WIDTH // 2, Screen.SCREEN_HEIGHT // 2))

        rotate_clockwise_option_available = exists(rotate_clockwise_option_pattern,
                                                   FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert rotate_clockwise_option_available, \
            '\'Rotate clockwise\' option available in context menu after right-click at the document area'

        click(rotate_clockwise_option_pattern)

        page_contents_rotated = exists(last_page_contents_rotated_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert page_contents_rotated, '\'Rotate clockwise\' option works as expected'

        right_click(Location(Screen.SCREEN_WIDTH // 2, Screen.SCREEN_HEIGHT // 2))

        rotate_counterclockwise_option_available = exists(rotate_counterclockwise_option_pattern,
                                                          FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert rotate_counterclockwise_option_available, \
            '\'Rotate counterclockwise\' option available in context menu after right-click at the document area'

        click(rotate_counterclockwise_option_pattern)

        page_contents_rotated = exists(last_page_document_contents_pattern)
        assert page_contents_rotated, '\'Rotate Counterclockwise\' option works as expected'

        right_click(Location(Screen.SCREEN_WIDTH // 2, Screen.SCREEN_HEIGHT // 2))

        go_to_first_page_option_available = exists(go_to_first_page_option_pattern,
                                                   FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert go_to_first_page_option_available, \
            '\'Go to first page\' option available in context menu after right-click at the document area'

        click(go_to_first_page_option_pattern)

        first_page_opened = exists(first_page_contents_presentation_mode)
        assert first_page_opened, '\'Go to first page\' option works as expected'

        right_click(Location(Screen.SCREEN_WIDTH // 2, Screen.SCREEN_HEIGHT // 2))

        view_page_info_option_available = exists(view_page_info_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert view_page_info_option_available, \
            '\'View page info\' option available in context menu after right-click at the document area'

        click(view_page_info_pattern)

        page_info_opened = exists(page_info_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert page_info_opened, '\'Page info\' window opened'

        close_window_control('auxiliary')

        try:
            page_info_closed = wait_vanish(page_info_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
            assert page_info_closed, '\'Page info\' window closed'
        except FindError:
            raise FindError('\'Page info\' window did not close')

        right_click(Location(Screen.SCREEN_WIDTH // 2, Screen.SCREEN_HEIGHT // 2))

        save_page_as_option_available = exists(save_page_as_option_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert save_page_as_option_available, \
            '\'Save page as...\' option available in context menu after right-click at the document area'

        click(save_page_as_option_pattern)

        dialogue_window_opened = exists(dialogue_window_cancel_button, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert dialogue_window_opened, \
            '\'Save page as...\' option works as expected'

        click(dialogue_window_cancel_button)

        try:
            save_as_dialogue_closed = wait_vanish(dialogue_window_cancel_button, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
            assert save_as_dialogue_closed, '\'Save page as...\' dialogue closed'
        except FindError:
            raise FindError('\'Save page as...\' dialogue did not close')

        right_click(Location(Screen.SCREEN_WIDTH // 2, Screen.SCREEN_HEIGHT // 2))

        inspect_element_option_available = exists(inspect_element_option_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert inspect_element_option_available, \
            '\'Inspect element\' option available in context menu after right-click at the document area'

        click(inspect_element_option_pattern)

        inspect_element_option_works = exists(dev_console_inspector_button_pattern,
                                              FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert inspect_element_option_works, '\'Inspect element...\' option works as expected'

        close_devtools_button_available = exists(close_devtools_button_pattern)
        assert close_devtools_button_available, '\'Close\' button available in devtools panel'

        click(close_devtools_button_pattern)

        try:
            dev_console_closed = wait_vanish(dev_console_inspector_button_pattern,
                                             FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
            assert dev_console_closed, 'Dev tools Inspector successfully closed'
        except FindError:
            raise FindError('Dev tools Inspector didn\'t close')

        right_click(Location(Screen.SCREEN_WIDTH // 2, Screen.SCREEN_HEIGHT // 2))

        exit_full_screen_option_available = exists(exit_full_screen_option_pattern,
                                                   FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert exit_full_screen_option_available, \
            '\'Exit Full Screen\' option available in context menu after right-click at the document area'

        click(exit_full_screen_option_pattern)

        exit_fullscreen_option_works = exists(presentation_button_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert exit_fullscreen_option_works, '\'Exit Full Screen\' option works as expected'

        click(presentation_button_pattern)

        assert exists(exit_fullscreen_button_pattern) and not exists(presentation_button_pattern), \
            'Presentation mode can be enabled after clicking at \'Exit Full Screen\' option'

        # "Take screenshot" option is not tested because of a bug:
        # https://bugzilla.mozilla.org/show_bug.cgi?id=1541376

        # "Select all" option is not tested because of a bug:
        # https://bugzilla.mozilla.org/show_bug.cgi?id=1267592

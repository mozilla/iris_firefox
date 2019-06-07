# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Bookmark a website from the Library - History menu.',
        locale=['en-US'],
        test_case_id='165088',
        test_suite_id='102',
        preferences={'devtools.chrome.enabled': True},
    )
    def run(self, firefox):
        drop_html_unfollowed_pattern = Pattern('drop_html_unfollowed.png')
        drop_html_inactive_pattern = Pattern('drop_html_inactive.png')
        drop_verified_pattern = Pattern('drop_matching_verified.png')
        drop_not_matching_pattern = Pattern('drop_not_matching.png')
        correct_result_pattern = Pattern('correct_result.png').similar(0.6)
        soap_url_selected_pattern = Pattern('soap_url_selected.png').similar(0.7)
        browser_console_title_pattern = Pattern('browser_console_title.png')

        navigate('https://mystor.github.io/dragndrop/')
        drop_page_loaded = exists(drop_html_unfollowed_pattern)
        assert drop_page_loaded, 'Drop page is loaded successfully'

        click(drop_html_unfollowed_pattern)

        drop_html_activated = exists(drop_html_inactive_pattern)
        assert drop_html_activated, 'The drop-html-data changed color to red which indicates that it has been selected.'

        type(Key.END)

        new_window()
        new_window_opened = exists(Tabs.NEW_TAB_HIGHLIGHTED)
        assert new_window_opened, 'New window opened'

        offset = Screen.SCREEN_WIDTH // 5
        if not OSHelper.is_mac():
            minimize_window()
            new_tab_location = find(Tabs.NEW_TAB_HIGHLIGHTED).right(offset)
            start_x = Screen.SCREEN_WIDTH // 5 if OSHelper.is_windows() else Screen.SCREEN_WIDTH // 4
            start_position = Location(start_x, Screen.SCREEN_HEIGHT // 18)

            drag_drop(new_tab_location, start_position)

        open_browser_console()
        console_opened = exists(browser_console_title_pattern)
        assert console_opened, 'Browser console is opened'

        click(browser_console_title_pattern)

        paste(f'window.resizeTo({Screen.SCREEN_WIDTH * 4 // 7}, {Screen.SCREEN_HEIGHT * 8 // 9})')
        type(Key.ENTER)
        close_tab()

        opened_tab_location = find(Tabs.NEW_TAB_HIGHLIGHTED).right(offset)
        new_window_drop_location = Location(Screen.SCREEN_WIDTH * 3 // 4, Screen.SCREEN_HEIGHT // 20)

        drag_drop(opened_tab_location, new_window_drop_location)

        tab_still_displayed = exists(Tabs.NEW_TAB_HIGHLIGHTED)
        assert tab_still_displayed, 'Selected "New tab" still displayed'

        click(Tabs.NEW_TAB_HIGHLIGHTED)

        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)
        wiki_page_loaded = exists(LocalWeb.SOAP_WIKI_SOAP_LABEL, Settings.DEFAULT_HEAVY_SITE_LOAD_TIMEOUT)
        assert wiki_page_loaded, 'Wiki webpage successfully is loaded.'

        # Selecting paragraph by triple click on location (pattern click doesn't select)
        paragraph_x, paragraph_y = LocalWeb.SOAP_WIKI_SOAP_LABEL.get_size()
        paragraph = find(LocalWeb.SOAP_WIKI_SOAP_LABEL)
        selection_end = find(LocalWeb.SOAP_WIKI_SOAP_LABEL).below(paragraph_y * 2)

        drag_drop(paragraph, selection_end)

        paragraph.offset(paragraph_x // 2, paragraph_y // 2)

        drop_position_offset_x, drop_position_offset_y = drop_not_matching_pattern.get_size()
        drop_html_position = find(drop_not_matching_pattern)
        drop_html_position.offset(drop_position_offset_x * 2, -drop_position_offset_y * 5)

        drag_drop(paragraph, drop_html_position)

        drop_verified = exists(drop_verified_pattern)
        assert drop_verified, '"Matching" appears under the "Drop Stuff Here" area.'
        matched_size_x, matched_size_y = drop_verified_pattern.get_size()
        result_region_location = find(drop_verified_pattern).offset(matched_size_x // 2, matched_size_y)
        result_region = Rectangle(result_region_location.x, 0, Screen.SCREEN_WIDTH // 2,
                                  Screen.SCREEN_HEIGHT)

        correct_result_displayed = exists(correct_result_pattern, region=result_region)
        assert correct_result_displayed, 'Actual and expected drop results are equal.'

        select_location_bar()
        link_selected = exists(soap_url_selected_pattern)
        assert link_selected, 'Local wiki url selected.'

        url_location = find(soap_url_selected_pattern)

        drag_drop(url_location, drop_html_position)

        drop_not_matched = exists(drop_not_matching_pattern)
        assert drop_not_matched, '"Not matching" phrase is appeared'

        wrong_result = not exists(correct_result_pattern, region=result_region)
        assert wrong_result, 'The expected result is different to result.'

        close_window()

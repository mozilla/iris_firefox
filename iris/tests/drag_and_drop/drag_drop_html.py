# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Drop html data in demopage'
        self.test_case_id = '165088'
        self.test_suite_id = '102'
        self.locale = ['en-US']

    def setup(self):
        BaseTest.setup(self)
        self.set_profile_pref({'devtools.chrome.enabled': True})

    def run(self):
        drop_html_unfollowed_pattern = Pattern('drop_html_unfollowed.png')
        drop_html_inactive_pattern = Pattern('drop_html_inactive.png')
        drop_verified_pattern = Pattern('drop_matching_verified.png')
        drop_not_matching_pattern = Pattern('drop_not_matching.png')
        correct_result_pattern = Pattern('correct_result.png').similar(0.6)
        soap_url_selected_pattern = Pattern('soap_url_selected.png').similar(0.7)
        browser_console_title_pattern = Pattern('browser_console_title.png')

        navigate('https://mystor.github.io/dragndrop/')
        drop_page_loaded = exists(drop_html_unfollowed_pattern)
        assert_true(self, drop_page_loaded, 'Drop page is loaded successfully.')
        click(drop_html_unfollowed_pattern)

        drop_html_activated = exists(drop_html_inactive_pattern)
        assert_true(self, drop_html_activated,
                    'The drop-html-data changed color to red which indicates that it has been selected.')
        type(Key.END)

        new_window()
        new_window_opened = exists(Tabs.NEW_TAB_HIGHLIGHTED)
        assert_true(self, new_window_opened, 'New window opened')
        offset = SCREEN_WIDTH // 5
        if not Settings.is_mac():
            minimize_window()
            new_tab_location = find(Tabs.NEW_TAB_HIGHLIGHTED).offset(offset, 0)
            start_x = SCREEN_WIDTH // 5 if Settings.is_windows() else SCREEN_WIDTH // 4
            start_position = Location(start_x, SCREEN_HEIGHT // 18)
            drag_drop(new_tab_location, start_position)

        open_browser_console()
        console_opened = exists(browser_console_title_pattern)
        assert_true(self, console_opened, 'Browser console is opened')
        click(browser_console_title_pattern)
        paste('window.resizeTo({0}, {1})'.format(SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.9))
        type(Key.ENTER)
        close_tab()

        opened_tab_location = find(Tabs.NEW_TAB_HIGHLIGHTED).offset(offset, 0)
        new_window_drop_location = Location(SCREEN_WIDTH * 0.75, SCREEN_HEIGHT / 20)
        drag_drop(opened_tab_location, new_window_drop_location)

        tab_still_displayed = exists(Tabs.NEW_TAB_HIGHLIGHTED)
        assert_true(self, tab_still_displayed, 'Selected "New tab" still displayed')

        click(Tabs.NEW_TAB_HIGHLIGHTED)

        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)
        wiki_page_loaded = exists(LocalWeb.SOAP_WIKI_SOAP_LABEL, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, wiki_page_loaded, 'Wiki webpage successfully is loaded.')

        # Selecting paragraph by triple click on location (pattern click doesn't select)
        paragraph_x, paragraph_y = LocalWeb.SOAP_WIKI_SOAP_LABEL.get_size()
        paragraph = find(LocalWeb.SOAP_WIKI_SOAP_LABEL)
        selection_end = find(LocalWeb.SOAP_WIKI_SOAP_LABEL).offset(0, paragraph_y * 2)
        drag_drop(paragraph, selection_end)
        paragraph.offset(paragraph_x / 2, paragraph_y / 2)

        drop_position_offset_x, drop_position_offset_y = drop_not_matching_pattern.get_size()
        drop_html_position = find(drop_not_matching_pattern)
        drop_html_position.offset(drop_position_offset_x * 2, -drop_position_offset_y * 5)
        drag_drop(paragraph, drop_html_position)

        drop_verified = exists(drop_verified_pattern)
        assert_true(self, drop_verified, '"Matching" appears under the "Drop Stuff Here" area.')
        matched_size_x, matched_size_y = drop_verified_pattern.get_size()
        result_region_location = find(drop_verified_pattern).offset(matched_size_x / 2, matched_size_y)
        result_region = Region(result_region_location.x, 0, SCREEN_WIDTH / 2,
                               SCREEN_HEIGHT)

        correct_result_displayed = exists(correct_result_pattern, in_region=result_region)
        assert_true(self, correct_result_displayed, 'Actual and expected drop results are equal.')
        select_location_bar()

        link_selected = exists(soap_url_selected_pattern)
        assert_true(self, link_selected, 'Local wiki url selected.')
        url_location = find(soap_url_selected_pattern)
        drag_drop(url_location, drop_html_position)

        drop_not_matched = exists(drop_not_matching_pattern)
        assert_true(self, drop_not_matched, '"Not matching" phrase is appeared')

        wrong_result = not exists(correct_result_pattern.similar(0.8), in_region=result_region)
        assert_true(self, wrong_result, 'The expected result is different to result.')
        close_window()

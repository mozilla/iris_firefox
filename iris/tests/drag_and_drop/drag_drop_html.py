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

    def run(self):

        drop_html_unfollowed_pattern = Pattern('drop_html_unfollowed.png')
        drop_html_inactive_pattern = Pattern('drop_html_inactive.png')
        drop_here_pattern = Pattern('drop_here.png')
        drop_verified_pattern = Pattern('drop_matching_verified.png')
        drop_not_matching_pattern = Pattern('drop_not_matching.png')
        correct_result_pattern = Pattern('correct_result.png').similar(0.98)
        soap_url_selected_pattern = Pattern('soap_url_selected.png')

        change_preference('devtools.chrome.enabled', True)
        minimize_window()
        open_browser_console()
        paste('window.resizeTo({0}, {1})'.format(SCREEN_WIDTH*0.45, SCREEN_HEIGHT*0.9))
        type(Key.ENTER)
        close_tab()

        navigate('https://mystor.github.io/dragndrop/')
        drop_page_loaded = exists(drop_html_unfollowed_pattern)
        assert_true(self, drop_page_loaded, 'Drop page loaded successfully.')
        click(drop_html_unfollowed_pattern)

        drop_html_activated = exists(drop_html_inactive_pattern)
        assert_true(self, drop_html_activated,
                    'The drop-html-data changed color to red which indicates that it has been selected.')

        drop_not_matched = exists(drop_not_matching_pattern)
        assert_true(self, drop_not_matched, 'No drop to match now.')
        type(Key.END)

        new_window()
        opened_tab_location = find(Tabs.NEW_TAB_HIGHLIGHTED)
        new_window_drop_location = Location(SCREEN_WIDTH/2, SCREEN_HEIGHT/20)
        drag_drop(opened_tab_location, new_window_drop_location)

        drop_position_visible = exists(drop_here_pattern)
        assert_true(self, drop_position_visible, 'Drop position can be reached.')

        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)
        wiki_page_loaded = exists(LocalWeb.SOAP_WIKI_SOAP_LABEL, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, wiki_page_loaded, 'Wiki webpage successfully loaded.')

        # Selecting paragraph by triple click on location (pattern click doesn't select)
        paragraph = find(LocalWeb.SOAP_WIKI_SOAP_LABEL)
        [click(paragraph, DEFAULT_TYPE_DELAY) for _ in range(3)]
        paragraph_x, paragraph_y = LocalWeb.SOAP_WIKI_SOAP_LABEL.get_size()
        paragraph.offset(paragraph_x/2, paragraph_y/2)
        drop_position_offset_x, drop_position_offset_y = drop_here_pattern.get_size()
        drop_html_position = find(drop_here_pattern)
        drop_html_position.offset(drop_position_offset_x, drop_position_offset_y)
        drag_drop(paragraph, drop_html_position)

        drop_verified = exists(drop_verified_pattern)
        assert_true(self, drop_verified, '"Matching" appears under the "Drop Stuff Here" area.')

        result_correct = exists(correct_result_pattern)
        assert_true(self, result_correct, 'Actual and expected drop results are equal.')
        select_location_bar()

        link_selected = exists(soap_url_selected_pattern)
        assert_true(self, link_selected, 'Local wiki url selected.')
        url_location = find(soap_url_selected_pattern)
        drag_drop(url_location, drop_html_position)

        drop_not_matched = exists(drop_not_matching_pattern)
        assert_true(self, drop_not_matched, '"Not matched" appeared')

        wrong_result = not exists(correct_result_pattern, DEFAULT_UI_DELAY)
        assert_true(self, wrong_result, 'The expected result is different to result.')
        close_window()

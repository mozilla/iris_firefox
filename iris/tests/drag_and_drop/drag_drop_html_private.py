# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = "Drop html data in demopage opened in Private Window"
        self.test_case_id = "165089"
        self.test_suite_id = "102"
        self.locale = ["en-US"]

    def run(self):
        drop_html_data_button_pattern = Pattern('drop_html_data_button.png')
        drop_html_data_selected_button_pattern = Pattern('drop_html_data_selected_button.png')
        drop_here_pattern = Pattern('drop_here.png')
        soap_wiki_tab_pattern = Pattern('soap_wiki_tab.png')
        link_to_drag_drop_pattern = Pattern('link_to_drag_drop.png')
        matching_message_pattern = Pattern('matching_message.png')
        not_matching_message_pattern = Pattern('not_matching_message.png')

        new_private_window()

        private_window_opened = exists(PrivateWindow.private_window_pattern)
        assert_true(self, private_window_opened, 'New Private Window opened')

        navigate('https://mystor.github.io/dragndrop/')

        drop_html_data_button_displayed = exists(drop_html_data_button_pattern, Settings.SITE_LOAD_TIMEOUT)
        assert_true(self, drop_html_data_button_displayed, 'Site downloaded')

        click(drop_html_data_button_pattern)

        drop_html_data_selected_button_displayed = exists(drop_html_data_selected_button_pattern)
        assert_true(self, drop_html_data_selected_button_displayed, 'Button is selected')

        dropping_area_displayed = scroll_until_pattern_found(not_matching_message_pattern, repeat_key_down, (5,))
        assert_true(self, dropping_area_displayed, 'The dropping are is displayed')

        new_private_window()

        private_window_opened = exists(PrivateWindow.private_window_pattern)
        assert_true(self, private_window_opened, 'New Private Window opened')

        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)

        home_button_exists = exists(NavBar.HOME_BUTTON)
        assert_true(self, home_button_exists, 'Home button exists')

        home_height, home_width = NavBar.HOME_BUTTON.get_size()
        tabs_region = Region(0, 0, SCREEN_WIDTH, home_height * 4)

        soap_wiki_opened = exists(soap_wiki_tab_pattern, Settings.SITE_LOAD_TIMEOUT, tabs_region)
        assert_true(self, soap_wiki_opened, 'Soap wiki page opened')

        point_to_move_wiki_window = find(soap_wiki_tab_pattern, tabs_region).right(SCREEN_WIDTH/5)
        if Settings.is_mac():
            location_to_shift_wiki_window = find(soap_wiki_tab_pattern, tabs_region).right(SCREEN_WIDTH/2)
        else:
            location_to_shift_wiki_window = find(soap_wiki_tab_pattern, tabs_region).right(SCREEN_WIDTH)

        drag_drop(point_to_move_wiki_window, location_to_shift_wiki_window)

        soap_wiki_label_exists = exists(LocalWeb.SOAP_WIKI_SOAP_LABEL)
        assert_true(self, soap_wiki_label_exists, 'Paragraph to drag and drop is displayed')

        soap_wiki_label_location = find(LocalWeb.SOAP_WIKI_SOAP_LABEL)
        paragraph_to_select = find(LocalWeb.SOAP_WIKI_SOAP_LABEL).below(120)

        soap_wiki_label_location_to_drag = find(LocalWeb.SOAP_WIKI_SOAP_LABEL).offset(10, 10)

        drag_drop(soap_wiki_label_location, paragraph_to_select)

        drag_drop(soap_wiki_label_location_to_drag, drop_here_pattern)

        matching_message_displayed = exists(matching_message_pattern)
        assert_true(self, matching_message_displayed, 'The data is matching')

        click(soap_wiki_label_location)

        drag_drop(link_to_drag_drop_pattern, drop_here_pattern)

        not_matching_message_displayed = exists(not_matching_message_pattern)
        assert_true(self, not_matching_message_displayed, 'The data is not matching')

        close_window()
        close_window()












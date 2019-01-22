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
        navigate('https://mystor.github.io/dragndrop/')

        drop_html_data_button_displayed = exists(drop_html_data_button_pattern, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, drop_html_data_button_displayed, 'Site downloaded')

        click(drop_html_data_button_pattern)

        drop_html_data_selected_button_displayed = exists(drop_html_data_selected_button_pattern)
        assert_true(self, drop_html_data_selected_button_displayed, 'Button is selected')

        new_private_window()
        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)

        soap_wiki_opened = exists(LocalWeb.SOAP_WIKI_SOAP_LABEL, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, soap_wiki_opened, 'Soap wiki page opened')

        point_to_move_wiki_window = find(soap_wiki_tab_pattern).right(400)
        location_to_shift_wiki_window = find(soap_wiki_tab_pattern).right(800)
        location_to_shift_wiki_window_linux = find(soap_wiki_tab_pattern).right(2000)

        if Settings.is_linux():
            drag_drop(point_to_move_wiki_window, location_to_shift_wiki_window_linux)
        else:
            drag_drop(point_to_move_wiki_window, location_to_shift_wiki_window)

        time.sleep(DEFAULT_UI_DELAY)

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












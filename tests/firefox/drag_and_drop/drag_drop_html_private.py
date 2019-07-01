# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Drop html data in demopage opened in Private Window',
        locale=['en-US'],
        test_case_id='165089',
        test_suite_id='102',
    )
    def run(self, firefox):
        drop_html_data_button_pattern = Pattern('drop_html_data_button.png')
        drop_html_data_selected_button_pattern = Pattern('drop_html_data_selected_button.png')
        drop_here_pattern = Pattern('drop_here.png').similar(0.7)
        soap_wiki_tab_pattern = Pattern('soap_wiki_tab.png')
        link_to_drag_drop_pattern = Pattern('link_to_drag_drop.png')
        matching_message_pattern = Pattern('matching_message.png')
        not_matching_message_pattern = Pattern('not_matching_message.png')

        new_private_window()

        private_window_opened = exists(PrivateWindow.private_window_pattern)
        assert private_window_opened, 'New Private Window opened'

        navigate('https://mystor.github.io/dragndrop/')

        drop_html_data_button_displayed = exists(drop_html_data_button_pattern, Settings.SITE_LOAD_TIMEOUT)
        assert drop_html_data_button_displayed, 'Site downloaded'

        click(drop_html_data_button_pattern)

        drop_html_data_selected_button_displayed = exists(drop_html_data_selected_button_pattern)
        assert drop_html_data_selected_button_displayed, 'Button is selected'

        dropping_area_displayed = scroll_until_pattern_found(not_matching_message_pattern, repeat_key_down, (5,))
        assert dropping_area_displayed, 'The dropping are is displayed'

        new_private_window()

        private_window_opened = exists(PrivateWindow.private_window_pattern)
        assert private_window_opened, 'New Private Window opened'

        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)

        home_button_exists = exists(NavBar.HOME_BUTTON)
        assert home_button_exists, 'Home button exists'

        home_height, home_width = NavBar.HOME_BUTTON.get_size()
        tabs_region = Region(0, 0, Screen.SCREEN_WIDTH, home_height * 4)

        soap_wiki_opened = exists(soap_wiki_tab_pattern, Settings.SITE_LOAD_TIMEOUT, tabs_region)
        assert soap_wiki_opened, 'Soap wiki page opened'

        point_to_move_wiki_window = find(soap_wiki_tab_pattern, tabs_region).right(Screen.SCREEN_WIDTH // 5)
        if OSHelper.is_mac():
            location_to_shift_wiki_window = find(soap_wiki_tab_pattern, tabs_region).right(Screen.SCREEN_WIDTH // 2)
        else:
            location_to_shift_wiki_window = find(soap_wiki_tab_pattern, tabs_region).right(Screen.SCREEN_WIDTH)

        drag_drop(point_to_move_wiki_window, location_to_shift_wiki_window)

        soap_wiki_label_exists = exists(LocalWeb.SOAP_WIKI_SOAP_LABEL)
        assert soap_wiki_label_exists, 'Paragraph to drag and drop is displayed'

        soap_wiki_label_location = find(LocalWeb.SOAP_WIKI_SOAP_LABEL)
        paragraph_to_select = find(LocalWeb.SOAP_WIKI_SOAP_LABEL).below(120)

        soap_wiki_label_location_to_drag = find(LocalWeb.SOAP_WIKI_SOAP_LABEL).offset(10, 10)

        drag_drop(soap_wiki_label_location, paragraph_to_select)

        drag_drop(soap_wiki_label_location_to_drag, drop_here_pattern)

        matching_message_displayed = exists(matching_message_pattern)
        assert matching_message_displayed, 'The data is matching'

        click(soap_wiki_label_location)

        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT/2)

        drag_drop(link_to_drag_drop_pattern, drop_here_pattern)

        not_matching_message_displayed = exists(not_matching_message_pattern)
        assert not_matching_message_displayed, 'The data is not matching'

        close_window()
        close_window()

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(BaseTest):

    @pytest.mark.details(
        description='Drop image data in demopage opened in Private Window',
        locale=['en-US'],
        test_case_id='165087',
        test_suite_id='102',
        preferences={'devtools.chrome.enabled': True},
        blocked_by={'id': '1288773', 'platform': OSPlatform.ALL}
    )
    def run(self, firefox):
        drop_image_data_radiobutton_selected_pattern = Pattern('drop_image_data_selected.png')
        drop_image_data_radiobutton_pattern = Pattern('drop_image_data.png')
        browser_console_title_pattern = Pattern('browser_console_title.png')
        private_tab_logo_pattern = Pattern('private_window_logo.png')
        drop_here_pattern = Pattern('drop_here.png')
        image_from_page_pattern = Pattern('image_from_wiki.png')
        link_from_page_pattern = Pattern('link.png')
        not_matching_message_pattern = Pattern('drop_not_matching.png')

        new_private_window()

        private_window_opened = exists(PrivateWindow.private_window_pattern)
        assert private_window_opened, 'Private window is opened'

        private_tab_opened = exists(private_tab_logo_pattern)
        assert private_tab_opened, 'Private window is opened'

        navigate('https://mystor.github.io/dragndrop/')
        test_page_opened = exists(drop_image_data_radiobutton_pattern, Settings.site_load_timeout)
        assert test_page_opened, 'Firefox started and test page loaded successfully.'

        click(drop_image_data_radiobutton_pattern)
        drop_image_data_selected = exists(drop_image_data_radiobutton_selected_pattern)
        assert drop_image_data_selected, \
            'The "drop-image-data" changed color to red which indicates that it has been selected.'

        drop_result_message_displayed = scroll_until_pattern_found(not_matching_message_pattern, type, (Key.DOWN,))
        assert drop_result_message_displayed, \
            'Area where the drop result verification message is supposed ' \
            'to be displayed is present on the page after the scrolling'

        new_window()

        if not OSHelper.is_mac():
            minimize_window()

        open_browser_console()
        console_opened = exists(browser_console_title_pattern)
        assert console_opened, 'Browser console opened'

        click(browser_console_title_pattern)

        paste('window.resizeTo({0}, {1})'.format(Screen.SCREEN_WIDTH * 9 // 20, Screen.SCREEN_HEIGHT * 9 // 10))
        type(Key.ENTER)
        close_tab()

        new_window_opened = exists(Tabs.NEW_TAB_HIGHLIGHTED)
        assert new_window_opened, 'New window is opened'

        opened_tab_location = find(Tabs.NEW_TAB_HIGHLIGHTED).right(Screen.SCREEN_WIDTH // 4)
        new_window_drop_location = Location(Screen.SCREEN_WIDTH * 11 // 20, Screen.SCREEN_HEIGHT // 20)

        drag_drop(opened_tab_location, new_window_drop_location)

        drop_position_visible = exists(drop_here_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert drop_position_visible, 'Drop position can be reached.'

        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)
        page_loaded = exists(image_from_page_pattern, Settings.DEFAULT_SITE_LOAD_TIMEOUT)
        assert page_loaded, \
            'Wiki page loaded and contains an image that will be dropped into "Drop stuff here" area'

        drag_drop(image_from_page_pattern, drop_here_pattern)

        not_matching_message_appears = exists(not_matching_message_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert not_matching_message_appears is False, \
            '"Matching" appears under the "Drop Stuff Here" area, the expected result is ' \
            'identical to result and the image is displayed lower in the page.'

        link_displayed = exists(link_from_page_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert link_displayed, 'Wiki page contains link that will be dropped into "Drop stuff here" area'

        drag_drop(link_from_page_pattern, drop_here_pattern)
        not_matching_message_appears = exists(not_matching_message_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert not_matching_message_appears, '"Not Matching" appears under the Drop Stuff Here ' \
                                             'area, the expected result is different to result.'

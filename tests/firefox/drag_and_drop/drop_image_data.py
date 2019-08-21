# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(BaseTest):

    @pytest.mark.details(
        description='Drop image data in demopage',
        locale=['en-US'],
        test_case_id='165086',
        test_suite_id='102',
        preferences={'devtools.chrome.enabled': True},
        blocked_by={'id': '1288773', 'platform': OSPlatform.ALL}
    )
    def run(self, firefox):
        drop_image_data_radiobutton_selected_pattern = Pattern('drop_image_data_selected.png')
        drop_image_data_radiobutton_pattern = Pattern('drop_image_data.png')
        browser_console_title_pattern = Pattern('browser_console_title.png')
        drop_here_pattern = Pattern('drop_here.png').similar(0.7)
        image_from_page_pattern = Pattern('image_from_wiki.png')
        link_from_page_pattern = Pattern('link.png')
        not_matching_message_pattern = Pattern('drop_not_matching.png')
        offset = Screen.SCREEN_WIDTH // 5

        navigate('https://mystor.github.io/dragndrop/')
        test_page_opened = exists(drop_image_data_radiobutton_pattern, Settings.DEFAULT_SITE_LOAD_TIMEOUT)
        assert test_page_opened, 'Firefox started and test page loaded successfully.'

        click(drop_image_data_radiobutton_pattern)

        drop_image_data_selected = exists(drop_image_data_radiobutton_selected_pattern)
        assert drop_image_data_selected, \
            'The \'drop-image-data\' changed color to red which indicates that it has been selected.'

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

        paste(f'window.resizeTo({Screen.SCREEN_WIDTH * 11//20}, {Screen.SCREEN_HEIGHT * 9 // 10})')
        type(Key.ENTER)
        close_tab()

        opened_tab_location = find(Tabs.NEW_TAB_HIGHLIGHTED).right(offset)
        new_window_drop_location = Location(Screen.SCREEN_WIDTH * 3 // 5, Screen.SCREEN_HEIGHT // 20)

        drag_drop(opened_tab_location, new_window_drop_location)

        drop_position_visible = exists(drop_here_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert drop_position_visible, 'Drop position can be reached.'

        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)
        page_loaded = exists(image_from_page_pattern, Settings.DEFAULT_SITE_LOAD_TIMEOUT)
        assert page_loaded, 'Wiki page loaded and contains an image that will be dropped into \'Drop stuff here\' area'

        drag_drop(image_from_page_pattern, drop_here_pattern)

        not_matching_message_appears = exists(not_matching_message_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert not_matching_message_appears, \
            '"Matching" appears under the "Drop Stuff Here" area, the expected result is ' \
            'identical to result and the image is displayed lower in the page.'

        link_displayed = exists(link_from_page_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert link_displayed, 'Wiki page contains link that will be dropped into \'Drop stuff here\' area'

        drag_drop(link_from_page_pattern, drop_here_pattern)

        not_matching_message_appears = exists(not_matching_message_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert not_matching_message_appears, '"Not Matching" appears under the Drop Stuff Here ' \
                                             'area, the expected result is different to result.'

        close_window()

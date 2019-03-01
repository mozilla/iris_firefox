# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Drop image data in demopage opened in Private Window'
        self.test_case_id = '165087'
        self.test_suite_id = '102'
        self.locales = ['en-US']
        self.blocked_by = {'id': '1328964', 'platform': Platform.ALL}

    def setup(self):
        BaseTest.setup(self)
        self.set_profile_pref({'devtools.chrome.enabled': True})

    def run(self):
        drop_image_data_radiobutton_selected_pattern = Pattern('drop_image_data_selected.png')
        drop_image_data_radiobutton_pattern = Pattern('drop_image_data.png')
        browser_console_title_pattern = Pattern('browser_console_title.png')
        iris_tab_favicon_pattern = Pattern('iris_tab.png')
        drop_here_pattern = Pattern('drop_here.png')
        image_from_page_pattern = Pattern('image_from_wiki.png')
        link_from_page_pattern = Pattern('link.png')
        not_matching_message_pattern = Pattern('drop_not_matching.png')

        close_window()
        new_private_window()

        if not Settings.is_mac():
            minimize_window()
            iris_tab_location = find(iris_tab_favicon_pattern)
            start_position = Location(SCREEN_WIDTH / 25, SCREEN_HEIGHT / 25)
            drag_drop(iris_tab_location, start_position)

        open_browser_console()
        console_opened = exists(browser_console_title_pattern)
        assert_true(self, console_opened, 'Browser console opened')

        click(browser_console_title_pattern)
        paste('window.resizeTo({0}, {1})'.format(SCREEN_WIDTH * 0.45, SCREEN_HEIGHT * 0.9))
        type(Key.ENTER)
        close_tab()

        navigate('https://mystor.github.io/dragndrop/')
        test_page_opened = exists(drop_image_data_radiobutton_pattern, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, test_page_opened, 'Firefox started and test page loaded successfully.')

        click(drop_image_data_radiobutton_pattern)
        drop_image_data_selected = exists(drop_image_data_radiobutton_selected_pattern)
        assert_true(self, drop_image_data_selected,
                    'The \'drop-image-data\' changed color to red which indicates that it has been selected.')

        drop_result_message_displayed = scroll_until_pattern_found(not_matching_message_pattern, type, (Key.DOWN,))
        assert_true(self, drop_result_message_displayed,
                    'Area where the drop result verification message is supposed '
                    'to be displayed is present on the page after the scrolling')

        new_window()
        opened_tab_location = find(Tabs.NEW_TAB_HIGHLIGHTED)
        new_window_drop_location = Location(SCREEN_WIDTH * 0.55, SCREEN_HEIGHT / 20)
        drag_drop(opened_tab_location, new_window_drop_location)
        drop_position_visible = exists(drop_here_pattern)
        assert_true(self, drop_position_visible, 'Drop position can be reached.')

        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)
        page_loaded = exists(image_from_page_pattern, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, page_loaded,
                    'Wiki page loaded and contains an image that will be dropped into \'Drop stuff here\' area')

        drag_drop(image_from_page_pattern, drop_here_pattern)
        not_matching_message_appears = exists(not_matching_message_pattern)
        assert_false(self, not_matching_message_appears,
                     '\'Matching\' appears under the \'Drop Stuff Here\' area, the expected result is '
                     'identical to result and the image is displayed lower in the page.')

        link_displayed = exists(link_from_page_pattern)
        assert_true(self, link_displayed, 'Wiki page contains link that will be dropped into \'Drop stuff here\' area')

        drag_drop(link_from_page_pattern, drop_here_pattern)
        not_matching_message_appears = exists(not_matching_message_pattern)
        assert_true(self, not_matching_message_appears, '\'Not Matching\' appears under the Drop Stuff Here '
                                                        'area, the expected result is different to result.')

        close_window()
        close_window()

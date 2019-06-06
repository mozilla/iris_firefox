# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Bug 1453545 - "Properties" option disabled when right-clicking folder in Bookmarks Toolbar',
        locale=['en-US'],
        test_case_id='171345',
        test_suite_id='2525',
        profile=Profiles.TEN_BOOKMARKS
    )
    def run(self, firefox):
        getting_started_toolbar_bookmark_pattern = Pattern('getting_started_in_toolbar.png')
        toolbar_new_folder_pattern = Pattern('new_folder_toolbar.png')
        properties_option_pattern = Pattern('properties_option.png')
        new_folder_option_pattern = Pattern('new_folder_option.png')
        new_folder_panel_pattern = Pattern('new_folder_panel.png')

        open_bookmarks_toolbar()

        toolbar_opened = exists(getting_started_toolbar_bookmark_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert toolbar_opened is True, 'The Bookmarks Toolbar is successfully enabled.'

        getting_started_bookmark_location = find(getting_started_toolbar_bookmark_pattern)
        click_location_x_offset = Screen.SCREEN_WIDTH // 2
        click_location_y_offset = getting_started_toolbar_bookmark_pattern.get_size()[1] // 2

        getting_started_bookmark_location.offset(click_location_x_offset, click_location_y_offset)

        right_click(getting_started_bookmark_location)

        new_folder_option_available = exists(new_folder_option_pattern)
        assert new_folder_option_available is True, '\'New Folder\' option available in context menu after ' \
                                                    'right click at toolbar.'

        click(new_folder_option_pattern)

        new_folder_panel_opened = exists(new_folder_panel_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert new_folder_panel_opened is True,  '\'New folder\' panel opened after clicking ' \
                                                 'at the \'New Folder\' option from context menu'

        type(Key.ENTER)

        new_folder_created = exists(toolbar_new_folder_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert new_folder_created is True, 'The folder is created and displayed on the Bookmark Toolbar.'

        right_click(toolbar_new_folder_pattern)

        properties_option_available = exists(properties_option_pattern)
        assert properties_option_available is True,'\'Properties\' option available in context menu after right click' \
                                                   ' at created folder on toolbar.'

        click(properties_option_pattern)

        folder_properties_opened = exists(new_folder_panel_pattern)
        assert folder_properties_opened is True, 'The Properties option is active and clickable. Note: In the ' \
                                                 'affected builds the Properties option was grey out.'

        type(Key.ESC)

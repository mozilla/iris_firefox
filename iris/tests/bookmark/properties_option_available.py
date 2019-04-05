# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Bug 1453545 - "Properties" option disabled when right-clicking folder in Bookmarks Toolbar'
        self.test_case_id = '171345'
        self.test_suite_id = '2525'
        self.locales = ['en-US']

    def setup(self):
        BaseTest.setup(self)
        self.profile = Profile.TEN_BOOKMARKS

    def run(self):
        getting_started_toolbar_bookmark_pattern = Pattern('getting_started_in_toolbar.png')
        toolbar_new_folder_pattern = Pattern('new_folder_toolbar.png')
        properties_option_pattern = Pattern('properties_option.png')
        new_folder_option_pattern = Pattern('new_folder_option.png')
        new_folder_panel_pattern = Pattern('new_folder_panel.png')

        open_bookmarks_toolbar()

        toolbar_opened = exists(getting_started_toolbar_bookmark_pattern, Settings.SHORT_FIREFOX_TIMEOUT)
        assert_true(self, toolbar_opened, 'The Bookmarks Toolbar is successfully enabled.')

        getting_started_bookmark_location = find(getting_started_toolbar_bookmark_pattern)
        getting_started_bookmark_location.x += 300
        getting_started_bookmark_location.y += 15

        right_click(getting_started_bookmark_location)

        new_folder_option_available = exists(new_folder_option_pattern)
        assert_true(self, new_folder_option_available,
                    '\'New Folder\' option available in context menu after right click at toolbar.')

        click(new_folder_option_pattern)

        new_folder_panel_opened = exists(new_folder_panel_pattern, Settings.SHORT_FIREFOX_TIMEOUT)
        assert_true(self, new_folder_panel_opened,
                    '\'New folder\' panel opened after clicking at the \'New Folder\' option from context menu')

        type(Key.ENTER)

        new_folder_created = exists(toolbar_new_folder_pattern, Settings.SHORT_FIREFOX_TIMEOUT)
        assert_true(self, new_folder_created, 'The folder is created and displayed on the Bookmark Toolbar.')

        right_click(toolbar_new_folder_pattern)

        properties_option_available = exists(properties_option_pattern)
        assert_true(self, properties_option_available,
                    '\'Properties\' option available in context menu after right click at created folder on toolbar.')

        click(properties_option_pattern)

        folder_properties_opened = exists(new_folder_panel_pattern)
        assert_true(self, folder_properties_opened,
                    'The Properties option is active and clickable. '
                    'Note: In the affected builds the Properties option was grey out.')

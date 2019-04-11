# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Search for text that appears on buttons'
        self.test_case_id = '127250'
        self.test_suite_id = '2085'
        self.locales = ['en-US']

    def run(self):
        google_search_button_pattern = Pattern('google_search_button.png')
        season_label_not_selected_pattern = Pattern('season_label_not_selected.png')
        season_label_selected_pattern = Pattern('season_label_selected.png')
        settings_label_not_selected_pattern = Pattern('settings_label_not_selected.png')
        settings_label_selected = Pattern('settings_label_selected.png')

        test_page_local = self.get_asset_path('google.htm')
        navigate(test_page_local)

        google_search_button_exists = exists(google_search_button_pattern, Settings.SITE_LOAD_TIMEOUT)
        assert_true(self, google_search_button_exists, 'The page is successfully loaded.')

        open_find()
        edit_select_all()
        edit_delete()

        find_toolbar_opened = exists(FindToolbar.FINDBAR_TEXTBOX, Settings.FIREFOX_TIMEOUT)
        assert_true(self, find_toolbar_opened, 'Find Toolbar is opened.')

        type('se', interval=1)

        selected_label_exists = exists(season_label_selected_pattern, Settings.TINY_FIREFOX_TIMEOUT)
        assert_true(self, selected_label_exists, 'The first one has a green background highlighted')

        label_not_found = exists(settings_label_not_selected_pattern, Settings.TINY_FIREFOX_TIMEOUT)
        assert_true(self, label_not_found, 'the others are not highlighted.')

        button_not_selected = exists(google_search_button_pattern, Settings.TINY_FIREFOX_TIMEOUT)
        assert_true(self, button_not_selected, 'Submit button is not highlighted.')

        click(FindToolbar.FIND_NEXT)

        settings_selected = exists(settings_label_selected, Settings.TINY_FIREFOX_TIMEOUT)
        assert_true(self, settings_selected, 'The second one has a green background highlighted')

        season_not_selected = exists(season_label_not_selected_pattern, Settings.TINY_FIREFOX_TIMEOUT)
        assert_true(self, season_not_selected, 'the others are not highlighted.')

        button_not_selected = exists(google_search_button_pattern, Settings.TINY_FIREFOX_TIMEOUT)
        assert_true(self, button_not_selected, 'Submit button is not highlighted.')

        click(FindToolbar.FIND_PREVIOUS)

        season_selected = exists(season_label_selected_pattern, Settings.TINY_FIREFOX_TIMEOUT)
        assert_true(self, season_selected, 'The first one has a green background highlighted')

        settings_not_selected = exists(settings_label_not_selected_pattern, Settings.TINY_FIREFOX_TIMEOUT)
        assert_true(self, settings_not_selected, 'the others are not highlighted.')

        button_not_selected = exists(google_search_button_pattern, Settings.TINY_FIREFOX_TIMEOUT)
        assert_true(self, button_not_selected, 'Submit button is not highlighted.')

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description='Search for text that appears on buttons',
        locale=['en-US'],
        test_case_id='127250',
        test_suite_id='2085'
    )
    def run(self, firefox):
        google_search_button_pattern = Pattern('google_search_button.png')
        season_label_not_selected_pattern = Pattern('season_label_not_selected.png')
        season_label_selected_pattern = Pattern('season_label_selected.png')
        settings_label_not_selected_pattern = Pattern('settings_label_not_selected.png')
        settings_label_selected = Pattern('settings_label_selected.png')

        test_page_local = self.get_asset_path('google.htm')
        navigate(test_page_local)

        google_search_button_exists = exists(google_search_button_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert google_search_button_exists, 'The page is successfully loaded.'

        open_find()
        edit_select_all()
        edit_delete()

        find_toolbar_opened = exists(FindToolbar.FINDBAR_TEXTBOX, FirefoxSettings.FIREFOX_TIMEOUT)
        assert find_toolbar_opened, 'Find Toolbar is opened.'

        type('se', interval=1)

        selected_label_exists = exists(season_label_selected_pattern)
        assert selected_label_exists, 'The first one has a green background highlighted'

        label_not_found = exists(settings_label_not_selected_pattern)
        assert label_not_found, 'the others are not highlighted.'

        button_not_selected = exists(google_search_button_pattern)
        assert button_not_selected, 'Submit button is not highlighted.'

        click(FindToolbar.FIND_NEXT)

        settings_selected = exists(settings_label_selected)
        assert settings_selected, 'The second one has a green background highlighted'

        season_not_selected = exists(season_label_not_selected_pattern)
        assert season_not_selected, 'the others are not highlighted.'

        button_not_selected = exists(google_search_button_pattern)
        assert button_not_selected, 'Submit button is not highlighted.'

        find_previous_button_region = Screen.BOTTOM_THIRD
        find_previous_button = exists(FindToolbar.FIND_PREVIOUS, region=find_previous_button_region)
        assert find_previous_button, 'Find previous button available.'

        click(FindToolbar.FIND_PREVIOUS, duration=1, region=find_previous_button_region)

        season_selected = exists(season_label_selected_pattern)
        assert season_selected, 'The first one has a green background highlighted'

        settings_not_selected = exists(settings_label_not_selected_pattern)
        assert settings_not_selected, 'the others are not highlighted.'

        button_not_selected = exists(google_search_button_pattern)
        assert button_not_selected, 'Submit button is not highlighted.'

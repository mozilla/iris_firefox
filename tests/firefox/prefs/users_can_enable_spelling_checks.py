# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Users can enable/disable language spelling checks',
        test_case_id='143564',
        test_suite_id='2241',
        locale=['en-US'],
    )
    def run(self, firefox):
        preferences_search_pattern = AboutPreferences.ABOUT_PREFERENCE_SEARCH_PAGE_PATTERN
        text_editor_page = self.get_asset_path('editor.html')

        navigate('about:preferences#general')

        page_loaded = exists(AboutPreferences.PRIVACY_AND_SECURITY_BUTTON_NOT_SELECTED,
                             FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert page_loaded, 'about:preferences page loaded'

        navigate(text_editor_page)

        text_editor_loaded = exists(text_editor_title_pattern)
        assert text_editor_loaded, 'Text editor page loaded.'

        screen_center_location = Location(Screen.SCREEN_WIDTH//2, Screen.SCREEN_HEIGHT//2)

        click(screen_center_location)

        # The word that was spelled wrong is underlined with a red squiggly line.

        paste('test   ttteeesssttt')

        # From "Language and Appearance", underneath the "Language", uncheck the box "Check your spelling as you type".

        navigate('about:preferences#general')


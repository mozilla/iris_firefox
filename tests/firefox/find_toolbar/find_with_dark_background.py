# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description='Check the highlight of the found items on a page with dark background',
        locale=['en-US'],
        test_case_id='127242',
        test_suite_id='2085',
    )
    def run(self, firefox):
        work_in_label_pattern = Pattern('work_in_selected_label.png')
        instagram_unselected_pattern = Pattern('instagram_unselected_label.png')

        # Open Firefox and navigate to a page with dark background
        test_page_local = self.get_asset_path('dark_backgound.html')
        navigate(test_page_local)

        page_loaded = exists(instagram_unselected_pattern, FirefoxSettings.HEAVY_SITE_LOAD_TIMEOUT)
        assert page_loaded, 'The page is successfully loaded.'

        # Open the Find Toolbar
        open_find()
        edit_select_all()
        edit_delete()

        find_toolbar_opened = exists(FindToolbar.FINDBAR_TEXTBOX, FirefoxSettings.FIREFOX_TIMEOUT)
        assert find_toolbar_opened, 'Find Toolbar is opened.'

        # Search for a term that appears in the page and check the visibility of the highlighted term
        type('in', interval=1)

        selected_label_exists = exists(work_in_label_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert selected_label_exists, 'The first one has a green background highlighted.'

        unselected_label_exists = exists(instagram_unselected_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert unselected_label_exists, 'The others are not highlighted.'

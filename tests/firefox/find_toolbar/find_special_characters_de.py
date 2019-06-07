# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description='Search a word that contains special characters (1)',
        locale=['en-US'],
        test_case_id='127275',
        test_suite_id='2085'
    )
    def run(self, firefox):
        first_uber_highlighted_pattern = Pattern('first_uber_highlighted.png')
        second_uber_highlighted_pattern = Pattern('second_uber_highlighted.png')
        uber_not_highlighted_pattern = Pattern('uber_not_highlighted.png')

        test_page_local = self.get_asset_path('de.htm')
        navigate(test_page_local)

        page_loaded_anchor_exists = exists(LocalWeb.SOAP_WIKI_TEST_LABEL_PATTERN, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert page_loaded_anchor_exists, 'The page is successfully loaded.'

        open_find()
        edit_select_all()
        edit_delete()

        find_toolbar_opened = exists(FindToolbar.FINDBAR_TEXTBOX, FirefoxSettings.FIREFOX_TIMEOUT)
        assert find_toolbar_opened, 'Find Toolbar is opened.'

        paste('über')

        selected_label_exists = exists(first_uber_highlighted_pattern)
        assert selected_label_exists, 'The first one has a green background highlighted.'

        not_selected_label_exists = exists(uber_not_highlighted_pattern)
        assert not_selected_label_exists, 'The second one is not highlighted.'

        find_next()

        second_highlighted_exists = exists(second_uber_highlighted_pattern)
        assert second_highlighted_exists, 'The green box is moved with the current item.'

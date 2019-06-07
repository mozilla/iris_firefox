# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description='Search for characters like " #$%^&*( +-<>" ? !',
        locale=['en-US'],
        test_case_id='127277',
        test_suite_id='2085',
        enabled=False
    )
    def run(self, firefox):
        first_symbols_highlighted_pattern = Pattern('first_symbols_highlighted.png')
        second_symbols_highlighted_pattern = Pattern('second_symbols_highlighted.png')
        symbols_not_highlighted_pattern = Pattern('symbols_not_highlighted.png')

        test_page_local = self.get_asset_path('symbols.htm')
        navigate(test_page_local)

        page_loaded_anchor_exists = exists(LocalWeb.SOAP_WIKI_TEST_LABEL_PATTERN, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert page_loaded_anchor_exists, 'The page is successfully loaded.'

        open_find()
        edit_select_all()
        edit_delete()

        find_toolbar_opened = exists(FindToolbar.FINDBAR_TEXTBOX, FirefoxSettings.FIREFOX_TIMEOUT)
        assert find_toolbar_opened, 'Find Toolbar is opened.'

        paste('#$%^&*(+-<>')

        selected_label_exists = exists(first_symbols_highlighted_pattern)
        assert selected_label_exists, 'The first one has a green background highlighted.'

        not_selected_label_exists = exists(symbols_not_highlighted_pattern)
        assert not_selected_label_exists, 'The second one is not highlighted.'

        find_next()

        second_highlighted_exists = exists(second_symbols_highlighted_pattern)
        assert second_highlighted_exists, 'The green box is moved with the current item.'

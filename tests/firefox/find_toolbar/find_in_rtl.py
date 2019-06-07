# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description='Search on a page with RTL language',
        locale=['en-US'],
        test_case_id='127251',
        test_suite_id='2085',
    )
    def run(self, firefox):
        rtl_full_selected_pattern = Pattern('rtl_full_selected.png')
        rtl_deleted_selected_pattern = Pattern('rtl_deleted_selected.png')
        rtl_second_highlighted_pattern = Pattern('rtl_second_highlighted.png')
        rtl_second_not_highlighted_pattern = Pattern('rtl_second_not_highlighted.png')

        test_page_local = self.get_asset_path('rtl.html')
        navigate(test_page_local)

        page_loaded_anchor_exists = exists(rtl_second_not_highlighted_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert page_loaded_anchor_exists, 'The page is successfully loaded.'

        open_find()
        edit_select_all()
        edit_delete()

        find_toolbar_opened = exists(FindToolbar.FINDBAR_TEXTBOX, FirefoxSettings.FIREFOX_TIMEOUT)
        assert find_toolbar_opened, 'Find Toolbar is opened.'

        paste('على')

        selected_label_exists = exists(rtl_full_selected_pattern)
        assert selected_label_exists, 'The first one has a green background highlighted.'

        type(Key.BACKSPACE)
        rtl_deleted_selected_exists = exists(rtl_deleted_selected_pattern)
        assert rtl_deleted_selected_exists, 'Typing and deleting work. The caret is placed on the left side ' \
                                            'of the word.'

        edit_select_all()
        edit_delete()
        paste('ما')

        rtl_second_highlighted_exists = exists(rtl_second_highlighted_pattern)
        assert rtl_second_highlighted_exists, 'The first one has a green background highlighted.'

        rtl_second_not_highlighted_exists = exists(rtl_second_not_highlighted_pattern)
        assert rtl_second_not_highlighted_exists, 'The second one not highlighted.'

        edit_select_all()
        edit_delete()

        paste('على')
        find_next()
        find_next()

        selected_label_exists = exists(rtl_full_selected_pattern)
        assert selected_label_exists, 'After navigation The first one has a green background highlighted.'

        repeat_key_down(4)
        repeat_key_up(4)

        selected_label_exists = exists(rtl_full_selected_pattern)
        assert selected_label_exists, 'After scroll, no checkboarding is present.'

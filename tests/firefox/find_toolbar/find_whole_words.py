# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description='"Whole Words" button works properly',
        locale=['en-US'],
        test_case_id='127453',
        test_suite_id='2085',
    )
    def run(self, firefox):
        tester_label_pattern = Pattern('tester_label.png')
        test_selected_label_pattern = Pattern('test_selected_label.png')
        other_label_is_not_highlighted = Pattern('testex_label.png')
        second_selected_label_pattern = Pattern('text_label_selected_second.png')

        # Open Firefox and navigate to a popular website
        test_page_local = self.get_asset_path('words.html')
        navigate(test_page_local)

        soap_label_exists = exists(tester_label_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert soap_label_exists, 'The page is successfully loaded.'

        # Open the Find Toolbar
        open_find()
        edit_select_all()
        edit_delete()

        find_toolbar_opened = exists(FindToolbar.FINDBAR_TEXTBOX, FirefoxSettings.FIREFOX_TIMEOUT)
        assert find_toolbar_opened, 'Find Toolbar is opened.'

        # Enter a search term using a word written with an upper case, activate "Whole Words" and press ENTER
        type('test', interval=1)
        click(FindToolbar.FIND_ENTIRE_WORD)

        selected_label_exists = exists(test_selected_label_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert selected_label_exists, 'All the matching words/characters are found. The first one has a green ' \
                                      'background highlighted, and the others are not highlighted.'

        # Navigate through the results
        type(Key.F3, interval=1)

        first_label_is_green = exists(second_selected_label_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert first_label_is_green, 'The next matching words/characters have a green background highlighted'

        other_label_is_not_highlighted = exists(other_label_is_not_highlighted, FirefoxSettings.FIREFOX_TIMEOUT)
        assert other_label_is_not_highlighted, 'The other is not highlighted'

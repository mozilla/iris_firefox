# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description='Search on a page with vertical text [Blocked by a bug of not focusing find item if text is '
                    'larger than a screen]',
        locale=['en-US'],
        test_case_id='127278',
        test_suite_id='2085'
    )
    def run(self, firefox):
        word_mozilla_first_selected_pattern = Pattern('word_mozilla_first_selected.png')
        word_mozilla_second_selected_pattern = Pattern('word_mozilla_second_selected.png')
        word_mozilla_second_unselected_pattern = Pattern('word_mozilla_second_unselected.png').similar(.7)

        vertical_search_page_local = self.get_asset_path('findbug.html')
        navigate(vertical_search_page_local)

        home_button_displayed = exists(NavBar.HOME_BUTTON)
        assert home_button_displayed, 'Home button displayed'

        home_buton_location = find(NavBar.HOME_BUTTON)
        text_region = Region(0, 0, home_buton_location.x, Screen.SCREEN_HEIGHT)

        navigated_to_find_bug = exists(word_mozilla_second_unselected_pattern, FirefoxSettings.FIREFOX_TIMEOUT,
                                       text_region)
        assert navigated_to_find_bug, 'URL loaded successfully.'

        open_find()
        edit_select_all()
        edit_delete()

        find_toolbar_is_opened = exists(FindToolbar.FINDBAR_TEXTBOX, FirefoxSettings.FIREFOX_TIMEOUT)
        assert find_toolbar_is_opened, 'The Find Toolbar is successfully displayed by pressing CTRL + F / Cmd + F,.'

        type('Mozilla')

        selected_label_exists = exists(word_mozilla_first_selected_pattern, FirefoxSettings.FIREFOX_TIMEOUT,
                                       text_region)
        unselected_label_exists = exists(word_mozilla_second_unselected_pattern, FirefoxSettings.FIREFOX_TIMEOUT,
                                         text_region)
        assert selected_label_exists and unselected_label_exists, 'The first one has a green background highlighted' \
                                                                  ' and the others are not highlighted.'

        before_next_selected_label_y = find(word_mozilla_first_selected_pattern, text_region).y
        find_next()

        after_next_selected_label_y = find(word_mozilla_second_selected_pattern, text_region).y
        assert before_next_selected_label_y != after_next_selected_label_y, 'Selected label moved forward.'

        before_prev_selected_label_y = find(word_mozilla_second_selected_pattern, text_region).y
        find_previous()

        after_prev_selected_label_y = find(word_mozilla_first_selected_pattern, text_region).y
        assert before_prev_selected_label_y != after_prev_selected_label_y, 'Selected label moved backward.'

        before_scroll_selected_exists = exists(word_mozilla_first_selected_pattern, FirefoxSettings.FIREFOX_TIMEOUT,
                                               text_region)

        repeat_key_down(4)
        repeat_key_up(4)

        after_scroll_selected_exists = exists(word_mozilla_first_selected_pattern, FirefoxSettings.FIREFOX_TIMEOUT,
                                              text_region)
        assert before_scroll_selected_exists and after_scroll_selected_exists, 'Occurrence is present after ' \
                                                                               'scroll up and down. No checkboarding ' \
                                                                               'is present'

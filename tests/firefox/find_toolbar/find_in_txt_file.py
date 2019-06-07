# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description='Search on a text file (.txt)',
        locale=['en-US'],
        test_case_id='127273',
        test_suite_id='2085',
    )
    def run(self, firefox):
        txt_page_title_pattern = Pattern('txt_page_title.png')
        text_first_occurrence_hightlighted_pattern = Pattern('txt_text_first_occurrence_hl.png')
        text_first_occurrence_unhighlighted_pattern = Pattern('txt_text_first_occurrence_white.png')
        text_second_occurrence_highlighted_pattern = Pattern('txt_text_second_occurrence_hl.png')
        text_second_occurrence_unhighlighted_pattern = Pattern('txt_text_second_occurrence_white.png')
        txt_page_title_pattern.similarity = 0.6

        # Open Firefox and open a [.txt page]
        test_page_local = self.get_asset_path('dmatest.txt')
        navigate(test_page_local)

        txt_page_title_pattern_exists = exists(txt_page_title_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert txt_page_title_pattern_exists, 'The page is successfully loaded.'

        # Open the Find Toolbar
        open_find()
        edit_select_all()
        edit_delete()

        find_toolbar_is_opened = exists(FindToolbar.FINDBAR_TEXTBOX, FirefoxSettings.FIREFOX_TIMEOUT)
        assert find_toolbar_is_opened, 'The Find Toolbar is displayed '

        # Search for a term that appears on the page
        type('Part')

        text_first_occurrence_highlighted = exists(text_first_occurrence_hightlighted_pattern,
                                                   FirefoxSettings.FIREFOX_TIMEOUT)
        assert text_first_occurrence_highlighted, 'The first occurrence is highlighted.'

        text_second_occurrence_unhighlighted = exists(text_second_occurrence_unhighlighted_pattern,
                                                      FirefoxSettings.FIREFOX_TIMEOUT)
        assert text_second_occurrence_unhighlighted, 'The second occurrence is not highlighted.'

        # Navigate through found items
        find_next()

        text_first_occurrence_unhighlighted = exists(text_first_occurrence_unhighlighted_pattern,
                                                     FirefoxSettings.FIREFOX_TIMEOUT)
        assert text_first_occurrence_unhighlighted, 'The first occurrence is not highlighted.'

        text_second_occurrence_highlighted = exists(text_second_occurrence_highlighted_pattern,
                                                    FirefoxSettings.FIREFOX_TIMEOUT)
        assert text_second_occurrence_highlighted, 'The first occurrence is not highlighted.'

        find_previous()

        text_first_occurrence_highlighted = exists(text_first_occurrence_hightlighted_pattern,
                                                   FirefoxSettings.FIREFOX_TIMEOUT)
        assert text_first_occurrence_highlighted, 'The first occurrence is highlighted again.'

        text_second_occurrence_unhighlighted = exists(text_second_occurrence_unhighlighted_pattern,
                                                      FirefoxSettings.FIREFOX_TIMEOUT)
        assert text_second_occurrence_unhighlighted, 'The second occurrence is not highlighted again.'

        # Scroll the page up and down
        [type(Key.DOWN) for _ in range(4)]
        [type(Key.UP) for _ in range(4)]

        assert text_first_occurrence_highlighted, 'The first occurrence is highlighted after scrolling down and up.'
        assert text_second_occurrence_unhighlighted, 'The second occurrence is not highlighted after scrolling ' \
                                                     'down and up.'

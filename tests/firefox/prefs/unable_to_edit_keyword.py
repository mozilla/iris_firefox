# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description="Bug 1129597 - Unable to edit keyword",
        test_case_id="145302",
        test_suite_id="2241",
        locale=["en-US"],
    )
    def run(self, firefox):
        preferences_search_pattern = AboutPreferences.ABOUT_PREFERENCE_SEARCH_PAGE_PATTERN
        one_click_search_engines_pattern = Pattern("one_click_search_engines.png")
        search_engines_keyword_pattern = Pattern("search_engines_keyword.png")
        initial_text_pattern = Pattern("initial_text.png")
        preferences_general_pane_pattern = Pattern("preferences_general_pane.png")
        preferences_search_pane_pattern = Pattern("preferences_search_pane.png")
        pre_selected_text_pattern = Pattern("pre_selected_text.png")
        final_text_pattern = Pattern("final_text.png")

        navigate("about:preferences#search")

        preferences_search_loaded = exists(preferences_search_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert preferences_search_loaded, "The about:preferences#search page couldn't load."

        click(AboutPreferences.FIND_IN_OPTIONS)
        paste('One-Click Search Engines')

        one_click_search_engines_found = exists(one_click_search_engines_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert one_click_search_engines_found, "'One-Click Search Engines' couldn't found in about:preferences#search"

        search_engines_keyword_found = exists(search_engines_keyword_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert search_engines_keyword_found, "Keyword column could not found in 'One-Click Search Engines'"

        keyword_location = find(search_engines_keyword_pattern)
        keyword_pattern_width, keyword_pattern_height = search_engines_keyword_pattern.get_size()
        keyword_section = Region(
            keyword_location.x - keyword_pattern_width / 6,
            keyword_location.y,
            keyword_pattern_width * 1.5,
            keyword_pattern_height * 2.5
        )

        double_click(keyword_location.offset(0, keyword_pattern_height*1.1))
        paste("b")
        type(Key.ENTER)
        initial_text_found = exists(initial_text_pattern, FirefoxSettings.FIREFOX_TIMEOUT, region=keyword_section)
        assert initial_text_found, "Initial text 'b' couldn't found in keyboard column"

        click(preferences_general_pane_pattern)
        click(preferences_search_pane_pattern)
        preferences_search_loaded = exists(preferences_search_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert preferences_search_loaded, "The about:preferences#search page couldn't load."

        for _ in range(3):
            type(Key.TAB)
        click(AboutPreferences.FIND_IN_OPTIONS)
        paste('One-Click Search Engines')

        one_click_search_engines_found = exists(one_click_search_engines_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert one_click_search_engines_found, "'One-Click Search Engines' couldn't found in about:preferences#search"

        double_click(keyword_location.offset(0, keyword_pattern_height * 1.1))
        pre_selected_text_pattern_found = exists(pre_selected_text_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert pre_selected_text_pattern_found, "Initial text 'b' is not getting selected on double click"

        pre_selected_text_location = find(pre_selected_text_pattern)
        text_width, text_height = pre_selected_text_pattern.get_size()
        click(pre_selected_text_location.offset(text_width, text_height/2))
        type(text="ing", interval=0.5)
        type(Key.ENTER)

        final_text_found = exists(final_text_pattern, FirefoxSettings.FIREFOX_TIMEOUT, region=keyword_section)
        assert final_text_found, "Final text 'bing' couldn't found in keyboard column"

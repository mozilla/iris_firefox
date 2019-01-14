# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Firefox can be set to no longer remember search and form history.'
        self.test_suite_id = '105209'
        self.test_case_id = '1956'
        self.locale = ['en-US']

    def run(self):
        remember_history_pattern = Pattern('remember_history.png')
        custom_history_settings_pattern = Pattern('custom_history_settings.png')
        remember_search_history_pattern = Pattern('remember_search_history.png')
        add_search_bar_pattern = Pattern('add_search_bar.png')
        search_tab_pattern = Pattern('random_search.png').similar(0.9)
        search_bar_not_empty_pattern = Pattern('search_bar_not_empty.png')
        search_form_suggestion_pattern = Pattern('search_form_suggestion.png')

        new_tab()
        navigate("about:preferences#privacy")
        preferences_opened = exists(AboutPreferences.PRIVACY_AND_SECURITY_BUTTON_SELECTED)
        assert_true(self, preferences_opened, 'The page is successfully displayed.')

        paste('remember')
        remember_history_menu_found = exists(remember_history_pattern)
        assert_true(self, remember_history_menu_found, 'History menu found.')

        click(remember_history_pattern)
        history_dropdown_opened = exists(custom_history_settings_pattern)
        assert_true(self, history_dropdown_opened, 'The option is successfully selected and remembered.')

        click(custom_history_settings_pattern)
        click(remember_search_history_pattern)

        navigate("about:preferences#search")
        search_preferences_opened = exists(add_search_bar_pattern)
        assert_true(self, search_preferences_opened, 'The about:preferences#search page is successfully displayed.')

        click(add_search_bar_pattern)
        search_bar_appeared = exists(LocationBar.SEARCH_BAR)
        assert_true(self, search_bar_appeared, 'The search bar is successfully added in the toolbar.')

        click(LocationBar.SEARCH_BAR)
        paste('random')
        type(Key.ENTER)
        search_done = exists(search_tab_pattern, DEFAULT_FIREFOX_TIMEOUT*3)
        assert_true(self, search_done, 'The Search is successfully performed.')

        new_tab()
        click(search_bar_not_empty_pattern)
        paste('r')
        previously_searched_not_saved = not exists(search_form_suggestion_pattern)
        assert_true(self, previously_searched_not_saved, 'The previously searched word is not saved.')

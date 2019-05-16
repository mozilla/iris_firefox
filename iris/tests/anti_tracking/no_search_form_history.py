# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Firefox can be set to no longer remember search and form history.'
        self.test_suite_id = '105209'
        self.test_case_id = '1826'
        self.locale = ['en-US']

    def run(self):
        remember_history_pattern = Pattern('remember_history.png')
        custom_history_settings_pattern = Pattern('custom_history_settings.png')
        remember_search_history_pattern = Pattern('remember_search_history.png')
        search_history_unticked_pattern = Pattern('remember_search_history_unticked.png')
        add_search_bar_pattern = Pattern('add_search_bar.png')
        search_tab_pattern = Pattern('google_tab.png')
        search_bar_not_empty_pattern = Pattern('search_bar_not_empty.png')
        search_form_suggestion_pattern = Pattern('search_form_suggestion.png')
        name_form_pattern = Pattern('name_form.png')
        password_form_pattern = Pattern('password_form.png').similar(.6)
        autocomplete_pattern = Pattern('word_autocomplete.png')
        form_address = self.get_asset_path('form.html')

        navigate('about:preferences#privacy')
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

        remember_search_unticked = exists(search_history_unticked_pattern)
        assert_true(self, remember_search_unticked, 'The checkbox is successfully unticked.')

        navigate('about:preferences#search')
        search_preferences_opened = exists(add_search_bar_pattern)
        assert_true(self, search_preferences_opened, 'The about:preferences#search page is successfully displayed.')

        click(add_search_bar_pattern)

        search_bar_appeared = exists(LocationBar.SEARCH_BAR)
        assert_true(self, search_bar_appeared, 'The search bar is successfully added in the toolbar.')

        click(LocationBar.SEARCH_BAR)

        paste('random')
        type(Key.ENTER)
        search_done = exists(search_tab_pattern, Settings.SITE_LOAD_TIMEOUT)
        assert_true(self, search_done, 'The Search is successfully performed.')

        new_tab()

        search_bar_is_not_empty = exists(search_bar_not_empty_pattern)
        assert_true(self, search_bar_is_not_empty, 'Search button isn\'t empty')

        if Settings.is_linux():

            double_click(search_bar_not_empty_pattern)

        else:

            click(search_bar_not_empty_pattern)

        paste('r')
        previously_searched_not_saved = not exists(search_form_suggestion_pattern)
        assert_true(self, previously_searched_not_saved, 'The previously searched word is not saved.')

        navigate(form_address)
        name_form_displayed = exists(name_form_pattern)
        assert_true(self, name_form_displayed, 'Form displayed.')

        click(name_form_pattern)

        paste('random')
        password_form_displayed = exists(password_form_pattern)
        assert_true(self, password_form_displayed, 'The website is successfully displayed.')

        click(password_form_pattern)

        paste('Asdf1@3$')
        type(Key.ENTER)

        navigate(form_address)

        click(name_form_pattern)

        type('r')
        no_autocomplete = not exists(autocomplete_pattern)
        assert_true(self, no_autocomplete, 'The form history is not saved.')

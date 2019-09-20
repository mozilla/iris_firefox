# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Firefox hijacking - default search engine.',
        locale=['en-US'],
        test_case_id='219663',
        test_suite_id='3063'
    )
    def run(self, firefox):
        picker_pattern = Pattern('search_engines_picker.png')
        about_preferences_search_pattern = Pattern('about_preferences_search.png')
        default_search_engines_list_small_pattern = Pattern('default_search_engines_list_small.png')
        default_search_engines_list_pattern = Pattern('default_search_engines_list.png')
        one_click_search_engines_pattern = Pattern('one_click_search_engines.png')

        navigate('about:preferences#search')
        assert exists(about_preferences_search_pattern, Settings.DEFAULT_SITE_LOAD_TIMEOUT), \
            'About preferences search page is successfully opened.'
        assert exists(picker_pattern), 'Picker displayed.'

        click(picker_pattern)
        assert exists(default_search_engines_list_pattern) or exists(default_search_engines_list_small_pattern), \
            'The default search engine list is not changed.'

        restore_firefox_focus()

        open_find()
        paste('One-click')
        assert exists(one_click_search_engines_pattern), 'The default One-click search engine list is not changed.'

        firefox.restart()
        navigate('about:preferences#search')
        assert exists(about_preferences_search_pattern)
        time.sleep(Settings.DEFAULT_UI_DELAY)

        click(picker_pattern)
        assert exists(default_search_engines_list_pattern) or exists(default_search_engines_list_small_pattern), \
            'The default search engine list is not changed after antivirus was installed.'

        restore_firefox_focus()
        open_find()
        paste('One-click')
        assert exists(one_click_search_engines_pattern), \
            'The default One-click search engine list is not changed after antivirus was installed.'

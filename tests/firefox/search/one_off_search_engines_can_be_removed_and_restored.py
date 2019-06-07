# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Items from the list of one-click search engines can be removed and restored.',
        locale=['en-US'],
        test_case_id='4276',
        test_suite_id='83',
    )
    def run(self, firefox):
        change_search_settings_pattern = Pattern('change_search_settings.png').similar(0.6)
        about_preferences_search_page_pattern = Pattern('about_preferences_search_page.png').similar(0.6)
        search_engine_pattern = Pattern('search_engine.png')
        amazon_search_bar_pattern = Pattern('amazon_search_bar.png')
        remove_pattern = Pattern('remove.png')
        restore_default_search_engine_pattern = Pattern('restore_default_search_engine.png')

        # Enable the search bar.
        change_preference('browser.search.widget.inNavBar', True)

        # Navigate to the 'about:preferences#search' page.
        select_search_bar()
        type(Key.DOWN)

        expected = exists(amazon_search_bar_pattern, 10)
        assert expected is True, 'The \'Amazon\' search engine found in the one-offs list.'

        expected = exists(change_search_settings_pattern, 10)
        assert expected is True, 'The \'Change Search Settings\' button found in the page.'

        click(change_search_settings_pattern)

        expected = exists(about_preferences_search_page_pattern, 10)
        assert expected is True, 'The \'about:preferences#search\' page opened.'

        # Select a search engine from the One-click search engines list and click the Remove button.
        paste('one-click')

        expected = exists(search_engine_pattern, 10)
        assert expected is True, 'The \'One-Click Search Engines\' section found.'

        expected = exists(amazon_search_bar_pattern, 10)
        assert expected is True, 'The \'Amazon\' search engine found in the \'about:preferences#search\' page.'

        click(amazon_search_bar_pattern)

        expected = exists(remove_pattern, 10)
        assert expected is True, 'The \'Remove\' button found.'

        click(remove_pattern)

        try:
            expected = wait_vanish(amazon_search_bar_pattern, 10)
            assert expected is True, 'The \'Amazon\' search engine is removed from the the ' \
                                     '\'about:preferences#search\' page.'
        except FindError:
            raise FindError('The \'Amazon\' search engine is still displayed in the page.')

        # Open the drop down menu from the Search Bar and check that the search engine previously removed is no longer
        # displayed in the one-offs list.
        select_search_bar()
        type(Key.DOWN)

        expected = exists(amazon_search_bar_pattern, 3)
        assert expected is False, 'The search engine previously removed is no longer displayed in the list.'

        # Open a new tab and a private window and repeat the above step.
        new_tab()
        select_search_bar()
        type(Key.DOWN)

        expected = exists(amazon_search_bar_pattern, 3)
        assert expected is False, 'The search engine previously removed is no longer displayed in the list.'

        new_private_window()
        select_search_bar()
        type(Key.DOWN)

        expected = exists(amazon_search_bar_pattern, 3)
        assert expected is False, 'The search engine previously removed is no longer displayed in the list.'

        close_window()

        # Select again 'Change Search Settings' and add back the previously removed search engine by selecting
        # "Restore Default Search Engines".
        select_search_bar()
        type(Key.DOWN)

        click(change_search_settings_pattern)

        expected = exists(about_preferences_search_page_pattern, 10)
        assert expected is True, 'The \'about:preferences#search\' page loaded.'

        type(Key.TAB)

        expected = exists(restore_default_search_engine_pattern, 10)
        assert expected is True, 'The \'Restore Default Search Engines\' button found.'

        click(restore_default_search_engine_pattern)

        expected = exists(amazon_search_bar_pattern, 10)
        assert expected is True, 'The search engine previously removed is placed back in the list.'

        # Repeat the above steps to see that the search engine is restored.
        new_tab()
        select_search_bar()
        type(Key.DOWN)

        expected = exists(amazon_search_bar_pattern, 3)
        assert expected is True, 'The search engine is restored.'

        new_private_window()
        select_search_bar()
        type(Key.DOWN)

        expected = exists(amazon_search_bar_pattern, 3)
        assert expected is True, 'The search engine is restored.'

        close_window()

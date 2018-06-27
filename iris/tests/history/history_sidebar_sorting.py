# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This is a test of the History sidebar.'

    def setup(self):
        """Test case setup

        This overrides the setup method in the BaseTest class, so that it can use a brand new profile.
        """
        BaseTest.setup(self)
        self.profile = Profile.BRAND_NEW
        return

    def run(self):
        youtube_logo = 'youtube_banner.png'
        google_search = 'google_search.png'
        amazon_logo = 'amazon_logo.png'
        wikipedia_logo = 'wikipedia.png'
        expand_button_history_sidebar = 'expand_button_history_sidebar.png'
        history_sidebar_view_button = 'history_sidebar_view_button.png'
        history_sidebar_sort_by_date = 'history_sidebar_sort_by_date.png'
        history_sidebar_items_sort_by_date = 'history_sidebar_items_sort_by_date.png'
        history_sidebar_sort_by_date_and_site = 'history_sidebar_sort_by_date_and_site.png'
        history_sidebar_items_sort_by_date_and_site = 'history_sidebar_items_sort_by_date_and_site.png'
        history_sidebar_sort_by_site = 'history_sidebar_sort_by_site.png'
        history_sidebar_items_sort_by_site = 'history_sidebar_items_sort_by_site.png'
        history_sidebar_sort_by_most_visited = 'history_sidebar_sort_by_most_visited.png'
        history_sidebar_items_sort_by_most_visited = 'history_sidebar_items_sort_by_most_visited.png'
        history_sidebar_sort_by_last_visited = 'history_sidebar_sort_by_last_visited.png'
        history_sidebar_items_sort_by_last_visited = 'history_sidebar_items_sort_by_last_visited.png'

        # Open some pages to create some history.
        navigate('https://www.youtube.com/')
        expected_1 = exists(youtube_logo, 10)
        assert_true(self, expected_1, 'Youtube loaded successfully.')

        new_tab()
        navigate('https://www.youtube.com/')
        expected_2 = exists(youtube_logo, 10)
        assert_true(self, expected_2, 'Youtube loaded successfully in new tab.')

        new_tab()
        navigate('https://www.google.com/?hl=EN')
        expected_3 = exists(google_search, 10)
        assert_true(self, expected_3, 'Google loaded successfully in new tab.')

        new_tab()
        navigate('https://www.amazon.com/')
        expected_4 = exists(amazon_logo, 10)
        assert_true(self, expected_4, 'Amazon loaded successfully in new tab.')

        new_tab()
        navigate('https://www.wikipedia.org/')
        expected_5 = exists(wikipedia_logo, 10)
        assert_true(self, expected_5, 'Wikipedia loaded successfully in new tab.')

        # Open the History sidebar.
        history_sidebar()
        expected_6 = exists(expand_button_history_sidebar, 10)
        assert_true(self, expected_6, 'Expand history sidebar button displayed properly.')
        click(expand_button_history_sidebar)

        # Sort by date.
        expected_7 = exists(history_sidebar_view_button, 10)
        assert_true(self, expected_7, 'View button displayed properly.')
        click(history_sidebar_view_button)
        expected_8 = exists(history_sidebar_sort_by_date, 10)
        assert_true(self, expected_8, 'Default sorting option - sort by date - is selected properly.')
        click(history_sidebar_sort_by_date)
        expected_9 = exists(history_sidebar_items_sort_by_date)
        assert_true(self, expected_9, 'History list is sorted properly by date.')

        # Sort by date and site.
        click(history_sidebar_view_button)
        expected_10 = exists(history_sidebar_sort_by_date_and_site, 10)
        assert_true(self, expected_10, 'Sort by date and site option is displayed properly.')
        click(history_sidebar_sort_by_date_and_site)
        expected_11 = exists(expand_button_history_sidebar, 10)
        assert_true(self, expected_11, 'Expand history sidebar button displayed properly.')
        click(expand_button_history_sidebar)
        expected_12 = exists(history_sidebar_items_sort_by_date_and_site)
        assert_true(self, expected_12, 'History list is sorted properly by date and site.')

        # Sort by site.
        click(history_sidebar_view_button)
        expected_13 = exists(history_sidebar_sort_by_site, 10)
        assert_true(self, expected_13, 'Sort by site option is displayed properly.')
        click(history_sidebar_sort_by_site)
        expected_14 = exists(history_sidebar_items_sort_by_site)
        assert_true(self, expected_14, 'History list is sorted properly by site.')

        # Sort by most visited.
        click(history_sidebar_view_button)
        expected_15 = exists(history_sidebar_sort_by_most_visited, 10)
        assert_true(self, expected_15, 'Sort by most visited option is displayed properly.')
        click(history_sidebar_sort_by_most_visited)
        expected_16 = exists(history_sidebar_items_sort_by_most_visited)
        assert_true(self, expected_16, 'History list is sorted properly by most visited.')

        # Sort by last visited.
        click(history_sidebar_view_button)
        expected_17 = exists(history_sidebar_sort_by_last_visited, 10)
        assert_true(self, expected_17, 'Sort by last visited option is displayed properly.')
        click(history_sidebar_sort_by_last_visited)
        expected_18 = exists(history_sidebar_items_sort_by_last_visited)
        assert_true(self, expected_18, 'History list is sorted properly by last visited.')

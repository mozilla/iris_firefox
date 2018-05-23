# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This is a test of the History sidebar.'

    def run(self):
        youtube_logo = 'youtube_banner.png'
        history_sidebar_youtube = 'history_sidebar_youtube.png'
        search_history_box = 'search_history_box.png'
        history_empty = 'history_empty.png'
        x_button_search_history_box = 'x_button_search_history_box.png'
        expand_button_history_sidebar = 'expand_button_history_sidebar.png'
        history_sidebar_items = 'history_sidebar_items.png'

        # Open a page to create some history.
        navigate('https://www.youtube.com/')
        expected_1 = exists(youtube_logo, 5)
        assert_true(self, expected_1, 'Page loaded successfully.')

        # Open the History sidebar.
        history_sidebar()
        expected_2 = exists(search_history_box, 5)
        assert_true(self, expected_2, 'Sidebar was opened successfully.')
        expected_3 = exists(expand_button_history_sidebar, 5)
        assert_true(self, expected_3, 'Expand history button displayed properly')
        click(expand_button_history_sidebar)
        click(search_history_box)

        # Check that Youtube is displayed in the History list.
        paste('youtube')
        expected_4 = exists(history_sidebar_youtube, 5)
        assert_true(self, expected_4, 'Youtube displayed in the History list successfully.')

        # Clear the History search box.
        expected_5 = exists(x_button_search_history_box, 5)
        assert_true(self, expected_5, 'Clear field button was displayed properly')
        click(x_button_search_history_box)
        time.sleep(0.5)
        expected_6 = exists(history_sidebar_items, 5)
        expected_7 = exists(search_history_box, 5)
        assert_true(self, expected_6 and expected_7, 'The expected items are displayed in the History list.')

        # Check that an unavailable page is not found in the History list.
        paste('test')
        expected_8 = exists(history_empty, 5)
        assert_true(self, expected_8, 'The page wasn\'t found in the History list.')

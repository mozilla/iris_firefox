# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This is a test of the History menu.'

    def run(self):
        history_items = 'history_items.png'
        youtube_logo = 'youtube_banner.png'
        google_search = 'google_search.png'
        amazon_logo = 'amazon_logo.png'
        history_youtube = 'history_youtube.png'
        wikipedia_logo = 'wikipedia.png'

        # Open a website in the current tab.
        navigate('https://www.youtube.com/')
        expected_1 = exists(youtube_logo, 5)
        assert_true(self, expected_1, 'Page loaded successfully.')

        # Open a website in a new tab.
        new_tab()
        time.sleep(1)
        navigate('https://www.google.com/?hl=EN')
        expected_2 = exists(google_search, 5)
        assert_true(self, expected_2, 'Page loaded successfully.')

        # Open a website in a new window.
        new_window()
        time.sleep(1)
        navigate('https://www.amazon.com/')
        expected_3 = exists(amazon_logo, 5)
        assert_true(self, expected_3, 'Page loaded successfully.')

        # Open a website from the History list.
        open_library_menu('History')
        expected_4 = exists(history_youtube, 5)
        assert_true(self, expected_4, 'Youtube displayed in the History list successfully.')
        click(history_youtube)
        expected_5 = exists(youtube_logo, 5)
        assert_true(self, expected_5, 'Page loaded successfully.')

        # Open a website in a private window.
        new_private_window()
        time.sleep(1)
        navigate('https://www.wikipedia.org/')
        expected_6 = exists(wikipedia_logo, 5)
        assert_true(self, expected_6, 'Page loaded successfully.')

        # Check the expected items are displayed in the History list.
        open_library_menu('History')
        expected_7 = exists(history_items, 5, 0.9)
        assert_true(self, expected_7, 'The expected items are displayed in the History list.')

        # Open a website from the History list in the private window.
        click(history_youtube)
        expected_8 = exists(youtube_logo, 5)
        assert_true(self, expected_8, 'Page loaded successfully.')

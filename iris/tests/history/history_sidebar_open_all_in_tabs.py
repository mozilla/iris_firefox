# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This is a test for the \'Open All in Tabs\' option from the History sidebar.'

    def setup(self):
        """Test case setup

        This overrides the setup method in the BaseTest class, so that it can use a brand new profile.
        """
        BaseTest.setup(self)
        self.profile = Profile.BRAND_NEW
        return

    def run(self):
        wikipedia_logo = 'wikipedia.png'
        google_search = 'google_search.png'
        firefox_privacy_logo = 'firefox_privacy_logo.png'
        search_history_box = 'search_history_box.png'
        expand_button_history_sidebar = 'expand_button_history_sidebar.png'

        # Open some pages to create some history.
        navigate('https://www.wikipedia.org/')
        expected_1 = exists(wikipedia_logo, 10)
        assert_true(self, expected_1, 'Wikipedia loaded successfully.')

        new_tab()
        navigate('https://www.google.com/?hl=EN')
        expected_2 = exists(google_search, 10)
        assert_true(self, expected_2, 'Google loaded successfully.')

        # Open the History sidebar.
        history_sidebar()
        expected_3 = exists(search_history_box, 10)
        assert_true(self, expected_3, 'Sidebar was opened successfully.')
        expected_4 = exists(expand_button_history_sidebar, 10)
        assert_true(self, expected_4, 'Expand history button displayed properly.')

        # 'Open All in Tabs' from the context menu.
        right_click(expand_button_history_sidebar)
        time.sleep(0.5)
        type(text='o')

        # Check that all the pages loaded successfully.
        expected_5 = exists(firefox_privacy_logo, 10)
        assert_true(self, expected_5, 'Firefox Privacy Notice loaded successfully.')
        next_tab()
        expected_6 = exists(google_search, 10)
        assert_true(self, expected_6, 'Google loaded successfully.')
        next_tab()
        expected_7 = exists(wikipedia_logo, 10)
        assert_true(self, expected_7, 'Wikipedia loaded successfully.')

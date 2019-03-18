# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Ctrl+Click/Command awesomebar entry with \'Switch to Tab\' doesn\'t open new tab.'
        self.test_case_id = '4265'
        self.test_suite_id = '83'
        self.locale = ['en-US']

    def run(self):
        mozilla_page_unfocused_pattern = Pattern('mozilla_page_unfocused.png')
        mozilla_suggestion_pattern = Pattern('mozilla_suggestion.png')

        navigate(LocalWeb.MOZILLA_TEST_SITE)

        expected = exists(LocalWeb.MOZILLA_LOGO, 10)
        assert_true(self, expected, 'Mozilla page loaded successfully.')

        new_tab()
        paste('127.0.0.1')

        expected = exists(mozilla_suggestion_pattern, 10)
        assert_true(self, expected, 'Search suggestions successfully displayed.')

        if Settings.get_os() == Platform.MAC:
            key_down(Key.COMMAND)
            click(mozilla_suggestion_pattern)
            key_up(Key.COMMAND)
        else:
            key_down(Key.CTRL)
            click(mozilla_suggestion_pattern)
            key_up(Key.CTRL)

        expected = exists(mozilla_page_unfocused_pattern, 10)
        assert_true(self, expected, 'Mozilla tab unfocused is visible.')

        expected = exists(LocalWeb.MOZILLA_LOGO, 10)
        assert_true(self, expected, 'Mozilla page is in focus.')

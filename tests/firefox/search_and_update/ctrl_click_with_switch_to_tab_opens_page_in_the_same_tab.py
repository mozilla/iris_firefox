# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Ctrl+Click/Command awesomebar entry with \'Switch to Tab\' doesn\'t open new tab.',
        locale=['en-US'],
        test_case_id='111374',
        test_suite_id='83',
    )
    def run(self, firefox):
        mozilla_page_unfocused_pattern = Pattern('mozilla_page_unfocused.png')
        mozilla_suggestion_pattern = Pattern('mozilla_suggestion.png')

        navigate(LocalWeb.MOZILLA_TEST_SITE)

        expected = exists(LocalWeb.MOZILLA_LOGO, 10)
        assert expected is True, 'Mozilla page loaded successfully.'

        new_tab()
        paste('127.0.0.1')

        expected = exists(mozilla_suggestion_pattern, 10)
        assert expected is True, 'Search suggestions successfully displayed.'

        if OSHelper.is_mac():
            key_down(Key.COMMAND)
            click(mozilla_suggestion_pattern)
            key_up(Key.COMMAND)
        else:
            key_down(Key.CTRL)
            click(mozilla_suggestion_pattern)
            key_up(Key.CTRL)

        expected = exists(mozilla_page_unfocused_pattern, 10)
        assert expected is True, 'Mozilla tab unfocused is visible.'

        expected = exists(LocalWeb.MOZILLA_LOGO, 10)
        assert expected is True, 'Mozilla page is in focus.'

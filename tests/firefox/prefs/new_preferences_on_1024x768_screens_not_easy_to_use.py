# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Test case: Bug 1363960 - New "Preferences" page on 1024x768 screens extends horizontally '
                    'off-screen (with horizontal scroll bar) doesn\'t look very good, and not very easy to use.',
        locales=['en-US'],
        test_case_id='145230',
        test_suite_id='2241',
        enabled=False
        # Blocked due to precondition: "Have screen resolution of 1024 x 768."
    )
    def run(self, firefox):
        type(Key.F11)

        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT)

        navigate('about:preferences')

        privacy_button_available = exists(AboutPreferences.PRIVACY_AND_SECURITY_BUTTON_NOT_SELECTED,
                                          FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert privacy_button_available, 'The page is successfully loaded. NOTE: The affected builds had ' \
                                         'this behaviour. ' \
                                         '[https://bug1363960.bmoattachments.org/attachment.cgi?id=8866625]'

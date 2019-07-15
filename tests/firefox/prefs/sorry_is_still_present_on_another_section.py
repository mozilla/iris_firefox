# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Bug 1450239 - "Sorry! There are no results in Options for..." is still present even after you '
                    'click on another section.',
        test_case_id='145690',
        test_suite_id='2241',
        locale=['en-US'],
    )
    def run(self, firefox):
        no_results_in_preferences_pattern = Pattern('no_results_in_preferences.png')

        navigate('about:preferences')

        page_loaded = exists(AboutPreferences.PRIVACY_AND_SECURITY_BUTTON_NOT_SELECTED,
                             FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert page_loaded, 'about:preferences page loaded'

        paste('asdasdasd')

        no_results_in_preferences = exists(no_results_in_preferences_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert no_results_in_preferences, '"Sorry! There are no results in Options for..." message is displayed'

        click(AboutPreferences.PRIVACY_AND_SECURITY_BUTTON_SELECTED)

        no_results_in_preferences = exists(no_results_in_preferences_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert no_results_in_preferences, 'The "Sorry! There are no results in Options for..." message disappears and' \
                                          ' only the content of the selected section is displayed. \nNOTE: In the ' \
                                          'builds affected by this bug the message "Sorry! There are no results in ' \
                                          'Options for..." still appeared and the options for the selected section' \
                                          ' was displayed underneath it. '

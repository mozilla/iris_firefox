# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Bug 1353862 - Performing a search then clicking on a category should remove '
                    'the \'Search Results\' category and clear the search',
        test_case_id='145723',
        test_suite_id='2241',
        locale=['en-US'],
    )
    def run(self, firefox):
        firefox_data_collection_and_use_pattern = Pattern('firefox_data_collection_and_use.png')

        navigate('about:preferences')

        page_loaded = exists(AboutPreferences.PRIVACY_AND_SECURITY_BUTTON_NOT_SELECTED)
        assert page_loaded, 'about:preferences page loaded.'

        paste('crash reports')

        firefox_data_collection_and_use = exists(firefox_data_collection_and_use_pattern,
                                                 FirefoxSettings.FIREFOX_TIMEOUT)
        assert firefox_data_collection_and_use, '"firefox data" Search Results are displayed'

        click(AboutPreferences.PRIVACY_AND_SECURITY_BUTTON_NOT_SELECTED)

        try:
            search_results_disappear = wait_vanish(firefox_data_collection_and_use_pattern)
        except FindError:
            raise FindError('Search results are still on page.')

        assert search_results_disappear, 'The Search Results disappear and the options for the selected section ' \
                                         'are displayed. -NOTE: In the builds affected by this bug, the Search Result' \
                                         ' remained on top of the page. '

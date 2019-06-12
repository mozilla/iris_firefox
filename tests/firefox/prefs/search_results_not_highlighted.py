# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Bug 1388745 - Some search results are not highlighted',
        locale=['en-US'],
        test_case_id='145065',
        test_suite_id='2241',
    )
    def run(self, firefox):
        find_more_highlighted_pattern = Pattern('find_more_highlighted.png')

        navigate('about:preferences')

        paste('find more')

        find_more_highlighted = exists(find_more_highlighted_pattern.similar(0.9 if OSHelper.is_linux() else 0.99),
                                       FirefoxSettings.FIREFOX_TIMEOUT)

        assert find_more_highlighted, '"Find more (search engine)" link is highlighted.'

        # -NOTE: In the builds affected by this bug the one-click Search Engines section was shown, but
        #  the searched text was not highlighted.

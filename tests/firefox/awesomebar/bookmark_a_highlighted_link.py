# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='This test case checks the position of the bookmark drop down for a highlighted link.',
        locale=['en-US'],
        test_case_id='117526',
        test_suite_id='1902'
    )
    def run(self, firefox):
        url = LocalWeb.FIREFOX_TEST_SITE
        bookmark_button_pattern = LocationBar.STAR_BUTTON_UNSTARRED

        navigate(url)
        expected = exists(LocalWeb.FIREFOX_LOGO, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, 'Page successfully loaded, firefox logo found.'

        select_location_bar()

        click(bookmark_button_pattern)

        expected = exists(Bookmarks.StarDialog.NEW_BOOKMARK, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, 'The bookmark drop down is displayed under the bookmark icon.'

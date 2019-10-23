# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    @pytest.mark.details(
        description=" Bug 1396059 - Open a URL in new tab when browser.search.openintab set to true ",
        locale=["en-US"],
        test_case_id="117527",
        test_suite_id="1902",
    )
    def run(self, firefox):
        change_preference("browser.search.openintab", "true")

        select_location_bar()
        paste("about:newtab")
        type(Key.ENTER)

        expected = exists(Tabs.NEW_TAB_HIGHLIGHTED, 10)
        assert expected, "The 'about:newtab' page successfully loaded."

        select_location_bar()
        paste(LocalWeb.FIREFOX_TEST_SITE)
        type(Key.ENTER)

        time.sleep(Settings.DEFAULT_UI_DELAY)

        # Link is opened in the same tab.
        expected = not exists(Tabs.NEW_TAB_NOT_HIGHLIGHTED)
        assert expected, "No extra tabs are displayed"

        expected = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert expected, "Page successfully loaded, firefox logo found."

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='"Edit this bookmark" panel appears after a page is already bookmarked',
        locale=['en-US'],
        test_case_id='163399',
        test_suite_id='2525',
        profile=Profiles.TEN_BOOKMARKS
    )
    def run(self, firefox):
        navigate(LocalWeb.MOZILLA_TEST_SITE)

        test_site_opened = exists(LocalWeb.MOZILLA_LOGO, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert test_site_opened is True, 'Previously bookmarked Mozilla website is opened'

        star_button_exists = exists(LocationBar.STAR_BUTTON_STARRED)
        assert star_button_exists is True, 'Star button is displayed'

        click(LocationBar.STAR_BUTTON_STARRED)

        edit_stardialog_displayed = exists(Bookmarks.StarDialog.EDIT_THIS_BOOKMARK, FirefoxSettings.FIREFOX_TIMEOUT)
        assert edit_stardialog_displayed is True, 'The Edit This Bookmark popup is displayed under the star-shaped' \
                                                  ' icon.'

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Remove a bookmark using star-shaped button',
        locale=['en-US'],
        test_case_id='163407',
        test_suite_id='2525',
        profile=Profiles.TEN_BOOKMARKS
    )
    def run(self, firefox):
        firefox_logo_pattern = LocalWeb.FIREFOX_LOGO
        blue_star_button_pattern = LocationBar.STAR_BUTTON_STARRED
        white_star_button_pattern = LocationBar.STAR_BUTTON_UNSTARRED
        edit_bookmark_pattern = Bookmarks.StarDialog.EDIT_THIS_BOOKMARK
        remove_button_pattern = Bookmarks.StarDialog.REMOVE_BOOKMARK

        navigate(LocalWeb.FIREFOX_TEST_SITE)

        firefox_logo_assert = exists(firefox_logo_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert firefox_logo_assert is True, 'Previously bookmarked page loaded.'

        blue_star_button_assert = exists(blue_star_button_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert blue_star_button_assert is True, 'Star button is blue.'

        click(blue_star_button_pattern)

        edit_bookmark_assert = exists(edit_bookmark_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert edit_bookmark_assert is True, 'Edit bookmark panel opened.'

        remove_button_assert = exists(remove_button_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert remove_button_assert is True, 'Remove button is present.'

        click(remove_button_pattern)

        white_star_button_assert = exists(white_star_button_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert white_star_button_assert is True, 'Star button turned white.'


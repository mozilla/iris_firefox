# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='"Choose..." another destination folder using star-shaped button',
        locale=['en-US'],
        test_case_id='163403',
        test_suite_id='2525',
        profile=Profiles.TEN_BOOKMARKS
    )
    def run(self, firefox):
        destination_folders_pattern = Pattern('destination_folders.png')

        navigate(LocalWeb.FOCUS_TEST_SITE)

        test_site_opened = exists(LocalWeb.FOCUS_LOGO, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert test_site_opened is True, 'Previously bookmarked Focus website is opened'

        stardialog_region = Region(Screen.SCREEN_WIDTH / 2, 0, Screen.SCREEN_WIDTH / 2, Screen.SCREEN_HEIGHT)

        star_button_exists = exists(LocationBar.STAR_BUTTON_STARRED)
        assert star_button_exists is True, 'Star button is displayed'

        click(LocationBar.STAR_BUTTON_STARRED, region=stardialog_region)

        edit_stardialog_displayed = exists(Bookmarks.StarDialog.EDIT_THIS_BOOKMARK, FirefoxSettings.FIREFOX_TIMEOUT,
                                           region=stardialog_region)
        assert edit_stardialog_displayed is True, 'The Edit This Bookmark popup is displayed under the star-shaped ' \
                                                  'icon.'

        click(Bookmarks.StarDialog.PANEL_FOLDER_DEFAULT_OPTION.similar(.6), 0, stardialog_region)

        choose_option_displayed = exists(Bookmarks.StarDialog.PANEL_OPTION_CHOOSE.similar(.6), region=stardialog_region)
        assert choose_option_displayed is True, 'Bookmark toolbar folder displayed'

        click(Bookmarks.StarDialog.PANEL_OPTION_CHOOSE.similar(.6), region=stardialog_region)

        destination_folders_displayed = exists(destination_folders_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert destination_folders_displayed, 'Edit This Bookmark panel is displayed with all the destination folders.'

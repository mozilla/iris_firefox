# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Bookmark folders can be changed in Bookmarks Toolbar',
        locale=['en-US'],
        test_case_id='163401',
        test_suite_id='2525',
        profile=Profiles.TEN_BOOKMARKS,
    )
    def run(self, firefox):
        navigate(LocalWeb.FOCUS_TEST_SITE)

        test_site_opened = exists(LocalWeb.FOCUS_LOGO, FirefoxSettings.FIREFOX_TIMEOUT*3)
        assert test_site_opened is True, 'Previously bookmarked Focus website is opened'

        stardialog_region = Rectangle(Screen.SCREEN_WIDTH / 2, 0, Screen.SCREEN_WIDTH / 2, Screen.SCREEN_HEIGHT)

        star_button_exists = exists(LocationBar.STAR_BUTTON_STARRED)
        assert star_button_exists is True, 'Star button is displayed'

        click(LocationBar.STAR_BUTTON_STARRED, region=stardialog_region)

        edit_stardialog_displayed = exists(Bookmarks.StarDialog.EDIT_THIS_BOOKMARK, FirefoxSettings.FIREFOX_TIMEOUT,
                                           region=stardialog_region)
        assert edit_stardialog_displayed is True, 'The Edit This Bookmark popup is displayed under the star-shaped ' \
                                                  'icon.'

        panel_folder_default_option_exists = exists(Bookmarks.StarDialog.PANEL_FOLDER_DEFAULT_OPTION.similar(.6),
                                                    region=stardialog_region)
        assert panel_folder_default_option_exists is True, 'Panel folder default option exists'

        click(Bookmarks.StarDialog.PANEL_FOLDER_DEFAULT_OPTION.similar(.6), region=stardialog_region)

        bookmark_toolbar_folder_displayed = exists(Bookmarks.StarDialog.PANEL_OPTION_BOOKMARK_TOOLBAR.similar(.6),
                                                   region=stardialog_region)
        assert bookmark_toolbar_folder_displayed is True, 'Bookmark toolbar folder displayed'

        click(Bookmarks.StarDialog.PANEL_OPTION_BOOKMARK_TOOLBAR.similar(.6), region=stardialog_region)

        stardialog_done_button_displayed = exists(Bookmarks.StarDialog.DONE, region=stardialog_region)
        assert stardialog_done_button_displayed is True, 'Stardialog Done button is displayed'

        click(Bookmarks.StarDialog.DONE)

        home_button_displayed = exists(NavBar.HOME_BUTTON)
        assert home_button_displayed is True, 'Home button is displayed'

        home_width, home_height = NavBar.HOME_BUTTON.get_size()
        bookmarks_toolbar_location = find(NavBar.HOME_BUTTON)
        bookmarks_toolbar_region = Rectangle(0, bookmarks_toolbar_location.y, Screen.SCREEN_WIDTH, home_height * 4)

        test_bookmark_folder_changed = exists(LocalWeb.FOCUS_BOOKMARK.similar(0.6), FirefoxSettings.FIREFOX_TIMEOUT*3,
                                              bookmarks_toolbar_region)
        assert test_bookmark_folder_changed is True, 'The Bookmarks Toolbar is enabled and the saved bookmark ' \
                                                     'is correctly displayed.'


# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = '"Choose..." another destination folder using star-shaped button '
        self.test_case_id = '163403'
        self.test_suite_id = '2525'
        self.locales = ['en-US']

    def run(self):
        soap_wiki_tab_pattern = Pattern('soap_wiki_tab.png')
        destination_folders_pattern = Pattern('destination_folders.png')

        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)

        soap_wiki_opened = exists(soap_wiki_tab_pattern, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, soap_wiki_opened, 'Soap wiki page opened')

        stardialog_region = Region(SCREEN_WIDTH / 2, 0, SCREEN_WIDTH / 2, SCREEN_HEIGHT)

        bookmark_page()

        stardialog_displayed = exists(Bookmarks.StarDialog.DONE, DEFAULT_FIREFOX_TIMEOUT, stardialog_region)
        assert_true(self, stardialog_displayed, 'Bookmark page dialog displayed')

        click(Bookmarks.StarDialog.DONE, in_region=stardialog_region)

        restore_firefox_focus()

        click(LocationBar.STAR_BUTTON_STARRED, in_region=stardialog_region)

        edit_stardialog_displayed = exists(Bookmarks.StarDialog.EDIT_THIS_BOOKMARK, DEFAULT_FIREFOX_TIMEOUT,
                                           in_region=stardialog_region)
        assert_true(self, edit_stardialog_displayed, 'The Edit This Bookmark popup is displayed under the star-shaped '
                                                     'icon.')

        click(Bookmarks.StarDialog.PANEL_FOLDER_DEFAULT_OPTION.similar(.6), 0, stardialog_region)
        choose_option_displayed = exists(Bookmarks.StarDialog.PANEL_OPTION_CHOOSE.similar(.6),
                                         in_region=stardialog_region)
        assert_true(self, choose_option_displayed, 'Bookmark toolbar folder displayed')
        click(Bookmarks.StarDialog.PANEL_OPTION_CHOOSE.similar(.6), in_region=stardialog_region)

        destination_folders_displayed = exists(destination_folders_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, destination_folders_displayed, 'Edit This Bookmark panel is displayed with all the '
                                                         'destination folders.')

        time.sleep(20)






# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Remove a tag from a bookmark'
        self.test_case_id = '163406'
        self.test_suite_id = '2525'
        self.locales = ['en-US']

    def setup(self):
        BaseTest.setup(self)
        self.profile = Profile.TEN_BOOKMARKS
        return

    def run(self):
        iris_tag_pattern = Pattern('iris_tag.png')
        if Settings.is_mac():
            tags_expander_closed_pattern = Pattern('tags_expander_closed.png').similar(.95)
        else:
            tags_expander_closed_pattern = Bookmarks.StarDialog.PANEL_TAGS_EXPANDER

        navigate(LocalWeb.FOCUS_TEST_SITE)

        test_site_opened = exists(LocalWeb.FOCUS_LOGO, Settings.SITE_LOAD_TIMEOUT)
        assert_true(self, test_site_opened, 'Previously bookmarked Focus website is opened')

        stardialog_region = Region(SCREEN_WIDTH / 2, 0, SCREEN_WIDTH / 2, SCREEN_HEIGHT)

        star_button_exists = exists(LocationBar.STAR_BUTTON_STARRED, in_region=stardialog_region)
        assert_true(self, star_button_exists, 'Star button is displayed')

        click(LocationBar.STAR_BUTTON_STARRED, in_region=stardialog_region)

        edit_stardialog_displayed = exists(Bookmarks.StarDialog.EDIT_THIS_BOOKMARK, Settings.FIREFOX_TIMEOUT,
                                           in_region=stardialog_region)
        assert_true(self, edit_stardialog_displayed, 'The Edit This Bookmark popup is displayed under the star-shaped '
                                                     'icon.')

        tags_field_exists = exists(Bookmarks.StarDialog.TAGS_FIELD)
        assert_true(self, tags_field_exists, 'The Tags field exists')

        click(Bookmarks.StarDialog.TAGS_FIELD)

        paste('iris')

        done_button_exists = exists(Bookmarks.StarDialog.DONE)
        assert_true(self, done_button_exists, 'The Done button exists')

        click(Bookmarks.StarDialog.DONE)

        click(LocationBar.STAR_BUTTON_STARRED)

        tags_expander_exists = exists(tags_expander_closed_pattern, Settings.FIREFOX_TIMEOUT,
                                      in_region=stardialog_region)
        assert_true(self, tags_expander_exists, 'Tags expander exists')

        click(tags_expander_closed_pattern)

        iris_tag_exists = exists(iris_tag_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, iris_tag_exists, 'The Iris tag exists')

        click(iris_tag_pattern)

        click(Bookmarks.StarDialog.DONE)

        click(LocationBar.STAR_BUTTON_STARRED)

        tags_expander_exists_second = exists(tags_expander_closed_pattern, Settings.FIREFOX_TIMEOUT,
                                             in_region=stardialog_region)
        assert_true(self, tags_expander_exists_second, 'Tags expander exists')

        click(tags_expander_closed_pattern)

        iris_tag_removed = exists(iris_tag_pattern)
        assert_false(self, iris_tag_removed, 'The tag is successfully removed from that bookmark.')

        restore_firefox_focus()

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Remove a tag from a bookmark',
        locale=['en-US'],
        test_case_id='163406',
        test_suite_id='2525',
        profile=Profiles.TEN_BOOKMARKS
    )
    def run(self, firefox):
        iris_tag_pattern = Pattern('iris_tag.png')
        if OSHelper.is_mac():
            tags_expander_closed_pattern = Pattern('tags_expander_closed.png').similar(.95)
        else:
            tags_expander_closed_pattern = Bookmarks.StarDialog.PANEL_TAGS_EXPANDER

        navigate(LocalWeb.FOCUS_TEST_SITE)

        test_site_opened = exists(LocalWeb.FOCUS_LOGO, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert test_site_opened is True, 'Previously bookmarked Focus website is opened'

        stardialog_region = Region(Screen.SCREEN_WIDTH / 2, 0, Screen.SCREEN_WIDTH / 2, Screen.SCREEN_HEIGHT)

        star_button_exists = exists(LocationBar.STAR_BUTTON_STARRED, region=stardialog_region)
        assert star_button_exists is True, 'Star button is displayed'

        click(LocationBar.STAR_BUTTON_STARRED, region=stardialog_region)

        edit_stardialog_displayed = exists(Bookmarks.StarDialog.EDIT_THIS_BOOKMARK, FirefoxSettings.FIREFOX_TIMEOUT,
                                           region=stardialog_region)
        assert edit_stardialog_displayed is True, 'The Edit This Bookmark popup is displayed under the star-shaped ' \
                                                  'icon.'

        tags_field_exists = exists(Bookmarks.StarDialog.TAGS_FIELD)
        assert tags_field_exists is True, 'The Tags field exists'

        click(Bookmarks.StarDialog.TAGS_FIELD)

        paste('iris')

        done_button_exists = exists(Bookmarks.StarDialog.DONE)
        assert done_button_exists is True, 'The Done button exists'

        click(Bookmarks.StarDialog.DONE)

        click(LocationBar.STAR_BUTTON_STARRED)

        tags_expander_exists = exists(tags_expander_closed_pattern, FirefoxSettings.FIREFOX_TIMEOUT,
                                      region=stardialog_region)
        assert tags_expander_exists is True, 'Tags expander exists'

        click(tags_expander_closed_pattern)

        iris_tag_exists = exists(iris_tag_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert iris_tag_exists is True, 'The Iris tag exists'

        click(iris_tag_pattern)

        click(Bookmarks.StarDialog.DONE)

        click(LocationBar.STAR_BUTTON_STARRED)

        tags_expander_exists_second = exists(tags_expander_closed_pattern, FirefoxSettings.FIREFOX_TIMEOUT,
                                             region=stardialog_region)
        assert tags_expander_exists_second is True, 'Tags expander exists'

        click(tags_expander_closed_pattern)

        iris_tag_removed = exists(iris_tag_pattern)
        assert iris_tag_removed is False, 'The tag is successfully removed from that bookmark.'

        restore_firefox_focus()

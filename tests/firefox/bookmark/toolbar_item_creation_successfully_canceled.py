# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='[win & linux] Bug 1397387 - No longer able to edit bookmark item after closing New Bookmark ' \
                    'or New Bookmark Folder dialog by [x] button',
        locale=['en-US'],
        test_case_id='171452',
        test_suite_id='2525',
        profile=Profiles.TEN_BOOKMARKS,
        exclude=OSPlatform.MAC
    )
    def run(self, firefox):
        getting_started_toolbar_bookmark_pattern = Pattern('getting_started_in_toolbar.png')
        new_bookmark_option_pattern = Pattern('new_bookmark_option.png')
        new_bookmark_window_pattern = Pattern('new_bookmark_window.png').similar(.6)
        toolbar_new_bookmark_pattern = Pattern('new_bookmark.png')
        delete_option_pattern = Pattern('delete_bookmark.png')

        open_bookmarks_toolbar()

        toolbar_opened = exists(getting_started_toolbar_bookmark_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert toolbar_opened is True, 'The Bookmarks Toolbar is successfully enabled.'

        getting_started_bookmark_location = find(getting_started_toolbar_bookmark_pattern)
        click_location_x_offset = Screen.SCREEN_WIDTH // 2
        click_location_y_offset = getting_started_toolbar_bookmark_pattern.get_size()[1] // 2

        getting_started_bookmark_location.offset(click_location_x_offset, click_location_y_offset)

        right_click(getting_started_bookmark_location)

        new_bookmark_option_available = exists(new_bookmark_option_pattern)
        assert new_bookmark_option_available is True, '\'New Bookmark\' option available in context ' \
                                                      'menu after right click at toolbar.'

        click(new_bookmark_option_pattern)

        new_bookmark_popup_opened = exists(new_bookmark_window_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert new_bookmark_popup_opened is True, 'The \'New Bookmark\' popup window is displayed.'

        close_window_control('auxiliary')

        try:
            popup_opened = wait_vanish(new_bookmark_window_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
            assert popup_opened is True, 'The popup window closes instantly.'
        except FindError:
            raise FindError('The popup window is not closes')

        try:
            new_bookmark_not_created = wait_vanish(toolbar_new_bookmark_pattern)
            assert new_bookmark_not_created is True, 'New Bookmark is not saved as bookmarked inside' \
                                                     ' the Bookmarks Toolbar.'
        except FindError:
            raise FindError('\'New bookmark\' pattern did not vanish')

        right_click(getting_started_toolbar_bookmark_pattern)

        delete_option_available = exists(delete_option_pattern)
        assert delete_option_available is True, '\'Delete\' option available in context menu after' \
                                                ' right click at bookmark from toolbar.'

        click(delete_option_pattern)

        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT/3)

        getting_started_bookmark_available = exists(getting_started_toolbar_bookmark_pattern)
        assert getting_started_bookmark_available is False, 'Delete bookmark action is successfully performed. ' \
                                                            '- Note: In the affected build, ' \
                                                            'New Bookmark/ New Folder was displayed as bookmarked ' \
                                                            'inside the Bookmarks Toolbar once the popup window was ' \
                                                            'dismissed. No action (delete/rename/move) could be done ' \
                                                            'either, as a consequence of closing the popup window' \
                                                            ' via [x] button. '

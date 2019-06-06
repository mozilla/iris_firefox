# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Bookmarks can be loaded inside the Bookmarks Sidebar.',

        # This feature was removed from Firefox 63 and beyond in bug 1452645.
        fx_version='<=62',
        locale=['en-US'],
        test_case_id='4162',
        test_suite_id='2525',
        profile=Profiles.TEN_BOOKMARKS
    )
    def run(self, firefox):
        moz_bookmark_pattern = Pattern('moz_sidebar_bookmark.png')
        save_pattern = Pattern('save_bookmark_name.png')
        access_sidebar_moz_pattern = Pattern('moz_sidebar_bookmark_location_changed.png')
        load_sidebar_bookmark = Pattern('load_sidebar_bookmark.png')
        properties_option_pattern = Pattern('properties_option.png')

        navigate('about:blank')

        bookmarks_sidebar('open')

        paste('mozilla')

        sidebar_bookmark_assert = exists(moz_bookmark_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert sidebar_bookmark_assert is True, 'Moz bookmark is present in the sidebar.'

        right_click(moz_bookmark_pattern)

        click(properties_option_pattern)

        properties_window_assert = exists(save_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert properties_window_assert is True, 'Properties window is present on the page.'

        click(load_sidebar_bookmark)

        try:
            wait(save_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
            logger.debug('Changes can be saved.')
            click(save_pattern)
        except FindError:
            raise FindError('Can\'t find save button, aborting.')

        amazon_sidebar_assert = exists(access_sidebar_moz_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert amazon_sidebar_assert is True, 'Moz bookmark can be accessed.'

        click(access_sidebar_moz_pattern)

        bookmark_load_in_sidebar_assert = exists(Pattern('moz_bookmark_sidebar_page_title.png'),
                                                 FirefoxSettings.FIREFOX_TIMEOUT)
        assert bookmark_load_in_sidebar_assert is True, 'Moz bookmark is successfully loaded inside the ' \
                                                        'Bookmarks Sidebar.'

        sidebar_scroll_assert = exists(Pattern('sidebar_scroll.png'), FirefoxSettings.FIREFOX_TIMEOUT)
        assert sidebar_scroll_assert is True, 'Horizontal scrollbar is available for the sidebar.'

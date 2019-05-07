# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Dark theme warnings.'
        self.test_case_id = '171347'
        self.test_suite_id = '1902'
        self.locales = ['en-US']

    def run(self):
        url = LocalWeb.FIREFOX_TEST_SITE
        themes_pattern = Pattern('themes.png')
        dark_theme_pattern = Pattern('dark_theme.png')
        wear_theme_pattern = Pattern('wear_theme.png')
        warning_message_tracking_protection_pattern = Pattern('warning_message_tracking_protection.png')

        navigate(url)

        expected = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert_true(self, expected, 'Page successfully loaded, firefox logo found.')

        open_addons()

        expected = exists(themes_pattern, 10)
        assert_true(self, expected, 'Add-ons page successfully loaded.')

        click(themes_pattern)

        expected = exists(dark_theme_pattern, 10)
        assert_true(self, expected, 'Dark theme option found in the page.')

        right_click(dark_theme_pattern)

        expected = exists(wear_theme_pattern, 10)
        assert_true(self, expected, 'The \'Wear theme\' option found in the page.')

        # Select the 'Wear theme' option.
        click(wear_theme_pattern)

        # Check that 'Wear theme' option successfully selected.
        right_click(dark_theme_pattern)

        try:
            expected = wait_vanish(wear_theme_pattern, 10)
            assert_true(self, expected, 'The \'Wear theme\' option not found in the page.')
        except FindError:
            raise FindError('The \'Wear theme\' option found in the page.')

        type(Key.ESC)

        new_private_window()
        navigate('https://hsts.badssl.com/')

        expected = exists(LocationBar.INSECURE_CONNECTION_LOCK_DARK_THEME, 10)
        assert_true(self, expected, 'The insecure connection lock is present in the page.')

        click(LocationBar.INSECURE_CONNECTION_LOCK_DARK_THEME)

        expected = exists(warning_message_tracking_protection_pattern.similar(0.92), 10)
        assert_true(self, expected, 'The warning message from Tracking Protection is readable.')

        close_window()

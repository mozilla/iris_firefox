# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Check for Dark and Light themes.',
        locale=['en-US'],
        test_case_id='15266',
        test_suite_id='494'
    )
    def run(self, firefox):
        for i in range(2):
            if i == 1:
                new_private_window()
            open_addons()

            expected = exists(AboutAddons.THEMES, 10)
            assert expected is True, 'Add-ons page successfully loaded.'

            click(AboutAddons.THEMES)

            expected = exists(AboutAddons.Themes.DARK_THEME, 10)
            assert expected is True, 'Dark theme option found in the page.'

            expected = exists(AboutAddons.Themes.LIGHT_THEME, 10)
            assert expected is True, 'Dark theme option found in the page.'

            expected = exists(AboutAddons.Themes.DEFAULT_THEME, 10)
            assert expected is True, 'Dark theme option found in the page.'

        close_window()

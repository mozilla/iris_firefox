# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='This is a test case that checks the default zoom level from the url bar.',
        locale=['en-US'],
        test_case_id='7442',
        test_suite_id='242',
    )
    def run(self, firefox):
        url = LocalWeb.FIREFOX_TEST_SITE
        url_bar_default_zoom_level_pattern = LocationBar.URL_BAR_DEFAULT_ZOOM_LEVEL
        edit_buttons_below_zoom_buttons_pattern = HamburgerMenu.EDIT_BUTTONS_BELOW_ZOOM_BUTTONS

        navigate(url)

        expected = exists(LocalWeb.FIREFOX_LOGO, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, 'Page successfully loaded, firefox logo found.'

        region = create_region_for_url_bar()

        expected = exists(url_bar_default_zoom_level_pattern, FirefoxSettings.FIREFOX_TIMEOUT, region=region)
        assert expected, 'Zoom indicator not displayed by default in the url bar.'

        new_region = create_region_for_hamburger_menu()

        expected = exists('100%', FirefoxSettings.FIREFOX_TIMEOUT, region=new_region)
        assert expected, 'By default zoom indicator is 100% in hamburger menu.'

        expected = exists(edit_buttons_below_zoom_buttons_pattern.similar(0.25),
                          FirefoxSettings.FIREFOX_TIMEOUT, region=new_region)
        assert expected, 'Control buttons for zooming appear above the Cut/Copy/Paste buttons.'

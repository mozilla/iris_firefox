# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description="Scrolling works properly on image-rich websites.",
        test_case_id="4661",
        test_suite_id="102",
        locale=["en-US"],
    )
    def run(self, firefox):
        image_site_loaded_pattern = Pattern('image_site_loaded.png').similar(0.7)
        pixbay_site_loaded_pattern = Pattern('pixbay_site_loaded.png').similar(0.7)

        mouse_wheel_steps = 200
        if OSHelper.is_windows():
            mouse_wheel_steps = 1600

        navigate('https://pixabay.com/images/search/pages/')

        image_site_loaded = exists(image_site_loaded_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert image_site_loaded is True, 'Pixabay images site is properly loaded'

        time.sleep(Settings.DEFAULT_UI_DELAY_LONG * 4)  # wait until image content loaded

        screen_centre = Location(Screen.SCREEN_WIDTH/2, Screen.SCREEN_HEIGHT/2)
        hover(screen_centre)

        # Scroll by mouse wheel
        bottom_page_button_destinated = scroll_until_pattern_found(pixbay_site_loaded_pattern,
                                                                   Mouse().scroll, (0, -mouse_wheel_steps,), 100,
                                                                   FirefoxSettings.TINY_FIREFOX_TIMEOUT/3)
        assert bottom_page_button_destinated is True, 'Successfully scrolled to footer by mouse scroll'

        top_page_button_destibated = scroll_until_pattern_found(image_site_loaded_pattern,
                                                                Mouse().scroll, (0, mouse_wheel_steps,), 100,
                                                                FirefoxSettings.TINY_FIREFOX_TIMEOUT/3)
        assert top_page_button_destibated is True, 'Successfully scrolled from footer to header by mouse scroll'

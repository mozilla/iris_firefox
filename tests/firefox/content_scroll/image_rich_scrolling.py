# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description="Scrolling works properly on image-rich websites.",
        test_case_id="C4661",
        test_suite_id="102",
        locale=["en-US"],
    )
    def run(self, firefox):
        show_more_results_button_pattern = Pattern('show_more_results_button.png')
        google_images_page_mark_pattern = Pattern('google_images_page_mark.png')
        google_save_button_pattern = Pattern('google_save_button.png')

        mouse_wheel_steps = 200
        if OSHelper.is_windows():
            mouse_wheel_steps = 1600

        navigate('https://www.google.com/preferences?hl=en#languages')

        google_save_button_exists = exists(google_save_button_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert google_save_button_exists is True, 'Google language preferences page is opened'

        click(google_save_button_pattern)

        navigate('http://images.google.com/?gws_rd=ssl')

        google_images_page_opened = exists(google_images_page_mark_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert google_images_page_opened is True, 'Google images site is properly loaded'

        paste('cute kittens:3')
        type(Key.ENTER)

        # Scroll by mouse wheel
        show_more_results_button_destinated = scroll_until_pattern_found(show_more_results_button_pattern,
                                                                         Mouse().scroll, (0, -mouse_wheel_steps,), 100,
                                                                         FirefoxSettings.TINY_FIREFOX_TIMEOUT/3)
        assert show_more_results_button_destinated is True, 'Successfully scrolled to footer by mouse scroll'

        google_images_page_mark_destinated = scroll_until_pattern_found(google_images_page_mark_pattern,
                                                                        Mouse().scroll, (0, mouse_wheel_steps,), 100,
                                                                        FirefoxSettings.TINY_FIREFOX_TIMEOUT/3)
        assert google_images_page_mark_destinated is True, 'Successfully scrolled from footer to header by mouse scroll'

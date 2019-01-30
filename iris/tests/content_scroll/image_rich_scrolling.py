# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = "Scrolling works properly on image-rich websites."
        self.test_case_id = "C4661"
        self.test_suite_id = "102"
        self.locale = ["en-US"]

    def run(self):
        show_more_results_button_pattern = Pattern('show_more_results_button.png')
        google_images_page_mark_pattern = Pattern('google_images_page_mark.png')
        google_save_button_pattern = Pattern('google_save_button.png')

        mouse_wheel_steps = 100
        if Settings.is_windows():
            mouse_wheel_steps = 1600

        navigate('https://www.google.com/preferences?hl=en#languages')

        google_save_button_exists = exists(google_save_button_pattern, 20)
        assert_true(self, google_save_button_exists, 'Google language preferences page is opened')

        click(google_save_button_pattern)

        navigate('https://images.google.com/?gws_rd=ssl')

        google_images_page_opened = exists(google_images_page_mark_pattern, 20)
        assert_true(self, google_images_page_opened, 'Google images site is properly loaded')

        paste('cute kittens:3')
        type(Key.ENTER)

        # Scroll by mouse wheel
        show_more_results_button_destinated = scroll_until_pattern_found(show_more_results_button_pattern,
                                                                         scroll, (-mouse_wheel_steps,), 20)
        assert_true(self, show_more_results_button_destinated, 'Successfully scrolled to footer by mouse scroll')

        google_images_page_mark_destinated = scroll_until_pattern_found(google_images_page_mark_pattern,
                                                                        scroll, (mouse_wheel_steps,), 20)
        assert_true(self, google_images_page_mark_destinated, 'Successfully scrolled from footer to '
                                                              'header by mouse scroll')

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
        home_button_pattern = Pattern('home_button.png')
        google_save_button_pattern = Pattern('google_save_button.png')

        mouse_wheel_steps = 100
        if Settings.is_windows():
            mouse_wheel_steps = 1600

        navigate('https://www.google.com/preferences?hl=en#languages')

        google_save_button_exists = exists(google_save_button_pattern, 20)
        assert_true(self, google_save_button_exists, 'The Soap Wiki test site is properly loaded')

        click(google_save_button_pattern)

        navigate('https://images.google.com/')

        google_images_page_opened = exists(google_images_page_mark_pattern, 20)
        assert_true(self, google_images_page_opened, 'The Soap Wiki test site is properly loaded')

        paste('kittens:3')
        type(Key.ENTER)

        home_button_location = find(home_button_pattern)
        click_inside_the_page_location = Location.below(home_button_location, away_y=50)

        click(click_inside_the_page_location)

        # Scroll by mouse wheel
        for times_scroll_down in range(20):
            scroll(-mouse_wheel_steps)
            show_more_results_button_destinated = exists(show_more_results_button_pattern)
            if show_more_results_button_destinated:
                assert_true(self, show_more_results_button_destinated, 'Successfully scrolled to footer by mouse '
                                                                       'scroll')
                break

        for times_scroll_up in range(20):
            scroll(mouse_wheel_steps)
            google_images_page_mark_destinated = exists(google_images_page_mark_pattern)
            if google_images_page_mark_destinated:
                assert_true(self, google_images_page_mark_destinated, 'Successfully scrolled from footer to '
                                                                      'header by mouse scroll')
                break



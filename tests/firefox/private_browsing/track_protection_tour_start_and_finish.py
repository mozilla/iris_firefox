# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Tracking protection tour can be successfully started and finished',
        test_case_id='107112',
        test_suite_id='1826',
        locales=['en-US'],
        fx_version='<=65',
        profile=Profiles.BRAND_NEW
    )
    def run(self, firefox):
        see_how_it_works_button_pattern = PrivateWindow.SEE_HOW_IT_WORKS_BUTTON
        next_button_first_tour_step_pattern = LocationBar.NEXT_BUTTON_TOUR_FIRST_STEP
        next_button_second_tour_step_pattern = ContentBlockingTour.NEXT_BUTTON_SECOND_TOUR_STEP
        got_it_button_pattern = ContentBlockingTour.GOT_IT_BUTTON

        # Open a new Private window tab.
        new_private_window()
        private_browsing_tab_logo_displayed = exists(PrivateWindow.private_window_pattern,
                                                     FirefoxSettings.FIREFOX_TIMEOUT)
        assert private_browsing_tab_logo_displayed is True, "New private window is displayed"

        #  Click the "See how it works" button.
        see_how_it_works_button_displayed = exists(see_how_it_works_button_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        if see_how_it_works_button_displayed:
            click(see_how_it_works_button_pattern)
        else:
            raise FindError('Can not find the "See how it works" button')

        new_firefox_content_blocking_label_displayed = exists(LocationBar.NEW_FIREFOX_CONTENT_BLOCKING_LABEL,
                                                              FirefoxSettings.FIREFOX_TIMEOUT)
        assert new_firefox_content_blocking_label_displayed is True, 'The "See how it works" was successfully clicked'

        next_button_first_tour_step_displayed = exists(next_button_first_tour_step_pattern, )
        if next_button_first_tour_step_displayed:
            click(next_button_first_tour_step_pattern)
        else:
            raise FindError('Can not find the "Next" button on the first tour step')

        differences_to_expect_label_displayed = exists(ContentBlockingTour.DIFFERENCES_TO_EXPECT_LABEL,
                                                       FirefoxSettings.FIREFOX_TIMEOUT)
        assert differences_to_expect_label_displayed is True, 'The first step of tour is successfully passed'

        next_button_second_tour_step_displayed = exists(next_button_second_tour_step_pattern,
                                                        FirefoxSettings.FIREFOX_TIMEOUT)
        if next_button_second_tour_step_displayed:
            click(next_button_second_tour_step_pattern)
        else:
            raise FindError('Can not find the "Next" button on the second tour step')

        turn_off_blocking_label_displayed = exists(ContentBlockingTour.TURN_OFF_BLOCKING_LABEL,
                                                   FirefoxSettings.FIREFOX_TIMEOUT)
        assert turn_off_blocking_label_displayed is True, 'The second step of tour is successfully passed'

        got_it_button_displayed = exists(got_it_button_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        if got_it_button_displayed:
            click(got_it_button_pattern)
        else:
            raise FindError('Can not find the "Got it!" button')

        restart_tour_button_displayed = exists(ContentBlockingTour.RESTART_TOUR_BUTTON, FirefoxSettings.FIREFOX_TIMEOUT)
        assert restart_tour_button_displayed is True, 'The tracking protection tour is successfully finished'

        close_window()


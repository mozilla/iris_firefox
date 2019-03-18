# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from iris.api.core.pattern import Pattern


class ContentBlockingTour(object):
    DIFFERENCES_TO_EXPECT_LABEL = Pattern('differences_to_expect_label.png')
    NEXT_BUTTON_SECOND_TOUR_STEP = Pattern('next_button_second_tour_step.png')
    TURN_OFF_BLOCKING_LABEL = Pattern('ui_tour_tooltip_title_turn_off_blocking.png')
    GOT_IT_BUTTON = Pattern('got_it_button.png')
    RESTART_TOUR_BUTTON = Pattern('restart_tour_button.png')

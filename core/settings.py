# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from core.arg_parser import parse_args
from core.enums import Color


class _Settings:
    """Class that holds general Iris settings.

    wait_scan_rate              -   The number of times actual pattern search operations are performed per second.
                                    (default - 3)
    type_delay                  -   The number of seconds between each keyboard press. (default - 0)
    move_mouse_delay            -   duration of mouse movement from current location to target location. (default - 0.5
                                    or value selected from Control Center)
    click_delay                 -   The number of seconds a click event is executed after the mouse moves to the target
                                    location. (default - 0)
    min_similarity              -   The default minimum similarity of find operations. While using a Region.find()
                                    operation. Iris searches the region using a default minimum similarity of 0.8.
    auto_wait_timeout           -   The maximum waiting time for all subsequent find operations. (default - 3)
    delay_before_mouse_down     -   Delay before the mouse is put in a held down state.
    delay_before_drag           -   Delay before the drag operation takes place.
    delay_before_drop           -   Delay before the drop operation takes place.
    slow_motion_delay           -   Controls the duration of the visual effect (seconds).
    observe_scan_rate           -   The number of times actual search operations are performed per second while waiting
                                    for a pattern to appear or vanish.
    observe_min_changed_pixels  -   The minimum size in pixels of a change to trigger a change event.
    highlight_duration          -   The duration of the highlight effect.
    highlight_color             -   The rectangle/circle border color for the highlight effect.
    highlight_thickness         -   The rectangle/circle border thickness for the highlight effect.
    mouse_scroll_step           -   The number of pixels for a vertical/horizontal scroll event.
    """

    DEFAULT_MIN_SIMILARITY = 0.8
    DEFAULT_SLOW_MOTION_DELAY = 2
    DEFAULT_OBSERVE_MIN_CHANGED_PIXELS = 50
    DEFAULT_TYPE_DELAY = 0
    DEFAULT_MOVE_MOUSE_DELAY = parse_args().mouse
    DEFAULT_CLICK_DELAY = 0
    DEFAULT_WAIT_SCAN_RATE = 3
    DEFAULT_OBSERVE_SCAN_RATE = 3
    DEFAULT_AUTO_WAIT_TIMEOUT = 3
    DEFAULT_DELAY_BEFORE_MOUSE_DOWN = 0.3
    DEFAULT_DELAY_BEFORE_DRAG = 0.3
    DEFAULT_DELAY_BEFORE_DROP = 0.3
    DEFAULT_HIGHLIGHT_DURATION = 2
    DEFAULT_HIGHLIGHT_COLOR = Color.RED
    DEFAULT_HIGHLIGHT_THICKNESS = 2
    DEFAULT_MOUSE_SCROLL_STEP = 100
    UI_DELAY = 1

    def __init__(self, wait_scan_rate=DEFAULT_WAIT_SCAN_RATE, type_delay=DEFAULT_TYPE_DELAY,
                 move_mouse_delay=DEFAULT_MOVE_MOUSE_DELAY, click_delay=DEFAULT_CLICK_DELAY,
                 min_similarity=DEFAULT_MIN_SIMILARITY, auto_wait_timeout=DEFAULT_AUTO_WAIT_TIMEOUT,
                 delay_before_mouse_down=DEFAULT_DELAY_BEFORE_MOUSE_DOWN,
                 delay_before_drag=DEFAULT_DELAY_BEFORE_DRAG,
                 delay_before_drop=DEFAULT_DELAY_BEFORE_DROP,
                 slow_motion_delay=DEFAULT_SLOW_MOTION_DELAY,
                 observe_scan_rate=DEFAULT_OBSERVE_SCAN_RATE,
                 observe_min_changed_pixels=DEFAULT_OBSERVE_MIN_CHANGED_PIXELS,
                 highlight_duration=DEFAULT_HIGHLIGHT_DURATION,
                 highlight_color=DEFAULT_HIGHLIGHT_COLOR,
                 highlight_thickness=DEFAULT_HIGHLIGHT_THICKNESS,
                 mouse_scroll_step=DEFAULT_MOUSE_SCROLL_STEP):

        self.wait_scan_rate = wait_scan_rate
        self._type_delay = type_delay
        self.move_mouse_delay = move_mouse_delay
        self._click_delay = click_delay
        self._min_similarity = min_similarity
        self.auto_wait_timeout = auto_wait_timeout
        self.delay_before_mouse_down = delay_before_mouse_down
        self.delay_before_drag = delay_before_drag
        self.delay_before_drop = delay_before_drop
        self.slow_motion_delay = slow_motion_delay
        self.observe_scan_rate = observe_scan_rate
        self.observe_min_changed_pixels = observe_min_changed_pixels
        self.highlight_duration = highlight_duration
        self.highlight_color = highlight_color.value
        self.highlight_thickness = highlight_thickness
        self.mouse_scroll_step = mouse_scroll_step

    @property
    def type_delay(self):
        return self._type_delay

    @type_delay.setter
    def type_delay(self, value):
        if value > 1:
            self._type_delay = 1
        else:
            self._type_delay = value

    @property
    def click_delay(self):
        return self._click_delay

    @click_delay.setter
    def click_delay(self, value):
        if value > 1:
            self._click_delay = 1
        else:
            self._click_delay = value

    @property
    def min_similarity(self):
        return self._min_similarity

    @min_similarity.setter
    def min_similarity(self, value):
        if value > 1:
            self._min_similarity = 1
        else:
            self._min_similarity = value


Settings = _Settings()

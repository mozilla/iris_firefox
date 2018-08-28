# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from errors import FindError
from key import type
from settings import DEFAULT_CLICK_DELAY
from util.color import Color
from util.highlight_circle import HighlightCircle
from util.highlight_rectangle import HighlightRectangle
from util.image_search import *
from util.ocr_search import *
from util.save_debug_image import save_debug_image
from util.screen_highlight import ScreenHighlight
from pynput.mouse import Button,Controller

try:
    import Image
except ImportError:
    from PIL import Image

pyautogui.FAILSAFE = False
logger = logging.getLogger(__name__)


class Region(object):
    def __init__(self, x=0, y=0, width=0, height=0):
        self._x = x
        self._y = y
        self._width = width
        self._height = height

    def debug(self):
        save_debug_image(None, self, None)

    def debug_ocr(self, with_image_processing=True):
        return self.text(with_image_processing, True)

    def show(self):
        region_screen = get_region(self)
        region_screen.show()

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        if isinstance(x, int):
            self._x = x
        else:
            raise ValueError(INVALID_NUMERIC_INPUT)

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        if isinstance(y, int):
            self._y = y
        else:
            raise ValueError(INVALID_NUMERIC_INPUT)

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, width):
        if isinstance(width, int):
            self._width = width
        else:
            raise ValueError(INVALID_NUMERIC_INPUT)

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, height):
        if isinstance(height, int):
            self._height = height
        else:
            raise ValueError(INVALID_NUMERIC_INPUT)

    def get_center(self):
        center_x = int(self._x + self._width) / 2
        center_y = int(self._y + self._height) / 2
        return Location(center_x, center_y)

    def move_to(self, location):
        self._x = location.x
        self._y = location.y

    def get_top_left(self):
        return Location(self._x, self._y)

    def get_top_right(self):
        top_right_x = self._x + self._width
        return Location(top_right_x, self._y)

    def get_bottom_left(self):
        bottom_left_y = self._y + self._height
        return Location(self._x, bottom_left_y)

    def get_bottom_right(self):
        bottom_right_x = self._x + self._width
        bottom_right_y = self._y + self._height
        return Location(bottom_right_x, bottom_right_y)

    def hover(self, where=None, duration=0):
        return hover(where, duration, self)

    def find(self, what=None):
        return find(what, self)

    def find_all(self, what=None):
        return find_all(what, self)

    def wait(self, what=None, timeout=None):
        wait(what, timeout, self)

    def wait_vanish(self, what=None, timeout=None):
        return wait_vanish(what, timeout, self)

    def exists(self, what=None, timeout=None):
        return exists(what, timeout, self)

    def click(self, where=None, duration=None):
        return click(where, duration, self)

    def text(self, with_image_processing=True, with_debug=False):
        return text(with_image_processing, self, with_debug)

    def highlight(self, seconds=None, color=None):
        highlight(self, seconds, color)

    @staticmethod
    def type(txt, modifier, interval):
        return type(txt, modifier, interval)

    @staticmethod
    def drag_drop(drag_from, drop_to, duration=None):
        return drag_drop(drag_from, drop_to, duration)

    def double_click(self, where, duration):
        return double_click(where, duration, self)

    def right_click(self, where, duration):
        return right_click(where, duration, self)


def highlight(region=None, seconds=None, color=None, pattern=None, location=None):

    if color is None:
        color = Settings.highlight_color

    if seconds is None:
        seconds = Settings.highlight_duration

    hl = ScreenHighlight()
    if region is not None:
        hl.draw_rectangle(HighlightRectangle(region.x, region.y, region.width, region.height, color))
        i = hl.canvas.create_text(region.x, region.y, anchor='nw', text='Region', font=("Arial", 12), fill=Color.WHITE)
        r = hl.canvas.create_rectangle(hl.canvas.bbox(i), fill=color, outline=color)
        hl.canvas.tag_lower(r, i)

    if pattern is not None:
        width, height = get_image_size(pattern)
        hl.draw_rectangle(HighlightRectangle(location.x, location.y, width, height, color))

    hl.render(seconds)
    time.sleep(seconds)


def generate_region_by_markers(top_left_marker_img=None, bottom_right_marker_img=None):
    try:
        wait(top_left_marker_img, 10)
        exists(bottom_right_marker_img, 10)
    except FindError:
        raise FindError('Unable to find page markers')

    top_left_pos = find(top_left_marker_img)
    hover(top_left_pos, 0)
    bottom_right_pos = find(bottom_right_marker_img)
    hover(bottom_right_pos, 0)

    marker_width, marker_height = get_image_size(bottom_right_marker_img)

    return Region(top_left_pos.x,
                  top_left_pos.y,
                  (bottom_right_pos.x + marker_width),
                  bottom_right_pos.y - top_left_pos.y + marker_height)


def create_region_from_patterns(top=None, bottom=None, left=None, right=None, padding_top=None, padding_bottom=None,
                                padding_left=None, padding_right=None):
    """
    Returns a region created from combined area of one or more patterns.
    Argument names are just for convenience and don't influence outcome.
    """
    patterns = []
    if top:
        patterns.append(top)
    if bottom:
        patterns.append(bottom)
    if left:
        patterns.append(left)
    if right:
        patterns.append(right)

    if len(patterns) == 0:
        raise ValueError('One or more patterns required.')

    logger.debug('Creating region from %s pattern(s).' % len(patterns))

    a, b = pyautogui.size()
    p1 = Location(a, b)
    p2 = Location(0, 0)

    for pattern in patterns:
        if exists(pattern, 5):
            current_pattern = find(pattern)
            if current_pattern.x < p1.x:
                p1.x = current_pattern.x
            if current_pattern.y < p1.y:
                p1.y = current_pattern.y

            w, h = get_image_size(pattern)

            if current_pattern.x + w > p2.x:
                p2.x = current_pattern.x + w
            if current_pattern.y + h > p2.y:
                p2.y = current_pattern.y + h
        else:
            raise FindError('Pattern not found: %s ' % pattern)

    found_region = Region(p1.x, p1.y, p2.x - p1.x, p2.y - p1.y)

    if padding_top or padding_bottom or padding_left or padding_right:
        logger.debug('Adding padding to region.')

    if padding_top:
        found_region.y -= padding_top
        found_region.height += padding_top

    if padding_bottom:
        found_region.height += padding_bottom

    if padding_left:
        found_region.x -= padding_left
        found_region.width += padding_left

    if padding_right:
        found_region.width += padding_right

    return found_region


def _click_at(location=None, clicks=None, duration=None, button=None):
    """Click on Location coordinates

    :param location: Location , image name or Pattern
    :param clicks: Number of mouse clicks
    :param duration: speed of hovering from current location to target
    :param button: Mouse button clicked (can be left, right, middle, 1, 2, 3)
    :return: None
    """

    if duration is None:
        duration = Settings.move_mouse_delay

    if location is None:
        location = Location(0, 0)

    pyautogui.moveTo(location.x, location.y, duration)
    if parse_args().highlight:
        hl = ScreenHighlight()
        hl.draw_circle(HighlightCircle(location.x, location.y, 15))
        hl.render()
    if clicks > 1:
        mouse = Controller()
        mouse.position = (location.x, location.y)
        mouse.click(Button.left, 2)
    else:
        pyautogui.click(clicks=clicks, interval=Settings.click_delay, button=button)

    if Settings.click_delay != DEFAULT_CLICK_DELAY:
        Settings.click_delay = DEFAULT_CLICK_DELAY


def _click_pattern(pattern, clicks=None, duration=None, in_region=None, button=None):
    """Click on center or offset of a Pattern

    :param pattern: Input Pattern
    :param clicks: Number of mouse clicks
    :param duration: Speed of hovering from current location to target
    :param in_region: Region object in order to minimize the area
    :param button: Mouse button clicked (can be left, right, middle, 1, 2, 3)
    :return: None
    """

    if duration is None:
        duration = Settings.move_mouse_delay

    needle = cv2.imread(pattern.get_file_path())
    height, width, channels = needle.shape

    p_top = positive_image_search(pattern=pattern, region=in_region)

    if p_top is None:
        raise FindError('Unable to click on: %s' % pattern.get_file_path())

    possible_offset = pattern.get_target_offset()

    if possible_offset is not None:
        _click_at(Location(p_top.x + possible_offset.x, p_top.y + possible_offset.y), clicks, duration, button)
    else:
        _click_at(Location(p_top.x + width / 2, p_top.y + height / 2), clicks, duration, button)


def _general_click(where=None, clicks=None, duration=None, in_region=None, button=None):
    """General Mouse Click

    :param where: Location , image name or Pattern
    :param clicks: Number of mouse clicks
    :param duration: speed of hovering from current location to target
    :param in_region: Region object in order to minimize the area
    :param button: Mouse button clicked (can be left, right, middle, 1, 2, 3)
    :return: None
    """

    if duration is None:
        duration = Settings.move_mouse_delay

    if isinstance(where, Pattern):
        _click_pattern(where, clicks, duration, in_region, button)

    elif isinstance(where, str):
        a_match = text_search_by(where, True, in_region)
        if a_match is not None:
            click_location = Location(a_match['x'] + a_match['width'] / 2, a_match['y'] + a_match['height'] / 2)
            _click_at(click_location, clicks, duration, button)

    elif isinstance(where, Location):
        _click_at(where, clicks, duration, button)

    else:
        raise ValueError(INVALID_GENERIC_INPUT)


def click(where=None, duration=None, in_region=None):
    """Mouse left click

    :param where: Location , image name or Pattern
    :param duration: speed of hovering from current location to target
    :param in_region: Region object in order to minimize the area
    :return: None
    """

    if duration is None:
        duration = Settings.move_mouse_delay

    _general_click(where, 1, duration, in_region, 'left')


def right_click(where=None, duration=None, in_region=None):
    """Mouse right click

    :param where: Location , image name or Pattern
    :param duration: speed of hovering from current location to target
    :param in_region: Region object in order to minimize the area
    :return: None
    """

    if duration is None:
        duration = Settings.move_mouse_delay

    _general_click(where, 1, duration, in_region, 'right')


def double_click(where=None, duration=None, in_region=None):
    """Mouse double click

    :param where: Location , image name or Pattern
    :param duration: speed of hovering from current location to target
    :param in_region: Region object in order to minimize the area
    :return: None
    """

    if duration is None:
        duration = Settings.move_mouse_delay

    _general_click(where, 2, duration, in_region, 'left')


def to_location(ps=None, in_region=None, align='top_left'):
    """Transform pattern or string to location

    :param ps: Pattern or string input
    :param in_region: Region object in order to minimize the area
    :param align: Alignment could be top_left, center
    :return: Location object
    """

    # TODO: Add multiple alignments if needed
    if isinstance(ps, Location):
        return ps

    elif isinstance(ps, Pattern):
        location = image_search(ps, in_region)
        if align == 'center':
            width, height = get_image_size(ps)
            return Location(location.x + width / 2, location.y + height / 2)
        else:
            return location


def drag_drop(drag_from, drop_to, duration=None):
    """Mouse drag and drop

    :param drag_from: Starting point for drag and drop. Can be pattern, string or location
    :param drop_to: Ending point for drag and drop. Can be pattern, string or location
    :param duration: speed of drag and drop
    :return: None
    """

    if duration is None:
        duration = Settings.move_mouse_delay

    from_location = to_location(ps=drag_from, align='center')
    _to_location = to_location(ps=drop_to, align='center')
    pyautogui.moveTo(from_location.x, from_location.y, 0)

    time.sleep(Settings.delay_before_mouse_down)
    pyautogui.mouseDown(button='left', _pause=False)

    time.sleep(Settings.delay_before_drag)
    pyautogui._mouseMoveDrag('drag', _to_location.x, _to_location.y, 0, 0, duration, pyautogui.linear, 'left')

    time.sleep(Settings.delay_before_drop)
    pyautogui.mouseUp(button='left', _pause=False)


def text(with_image_processing=True, in_region=None, debug=False):
    """Get all text from a Region or full screen

    :param bool with_image_processing: With extra dpi and contrast image processing
    :param Region in_region: In certain Region or full screen
    :param debug: boolean for saving ocr images
    :return: list of matches
    """
    all_text, debug_img, debug_data = text_search_all(with_image_processing, in_region)
    if debug and debug_img is not None:
        save_ocr_debug_image(debug_img, debug_data)
        logger.debug('> Found message: %s' % ocr_matches_to_string(all_text))
    return ocr_matches_to_string(all_text)


def hover(where=None, duration=0, in_region=None):
    """Hover over a Location, Pattern or image

    :param where: Location, Pattern or image name for hover target
    :param duration: speed of hovering from current location to target
    :param in_region: Region object in order to minimize the area
    :return: None
    """
    if isinstance(where, Pattern):
        pos = image_search(where, region=in_region)
        if pos.x != -1:
            needle_width, needle_height = get_image_size(where.get_filename())
            if isinstance(where, Pattern):
                possible_offset = where.get_target_offset()
                if possible_offset is not None:
                    move_to = Location(pos.x + possible_offset.x, pos.y + possible_offset.y)
                    pyautogui.moveTo(move_to.x, move_to.y)
                else:
                    move_to = Location(pos.x, pos.y)
                    pyautogui.moveTo(move_to.x + needle_width / 2, move_to.y + needle_height / 2)
            else:
                pyautogui.moveTo(pos.x + needle_width / 2, pos.y + needle_height / 2)
        else:
            raise FindError('Unable to find image %s' % where.get_filename())

    elif isinstance(where, str):
        a_match = text_search_by(where, True, in_region)
        if a_match is not None:
            pyautogui.moveTo(a_match['x'] + a_match['width'] / 2, a_match['y'] + a_match['height'] / 2)
        else:
            raise FindError('Unable to find text %s' % where)

    elif isinstance(where, Location):
        pyautogui.moveTo(where.x, where.y, duration)

    else:
        raise ValueError(INVALID_GENERIC_INPUT)


def find(image_name, region=None):
    """Look for a single match of a Pattern or image

    :param image_name: String or Pattern
    :param region: Region object in order to minimize the area
    :return: Location
    """
    if isinstance(image_name, Pattern):

        image_found = image_search(image_name, region)
        if (image_found.x != -1) & (image_found.y != -1):
            if parse_args().highlight:
                highlight(region=region, pattern=image_name, location=image_found)
            return image_found
        else:
            raise FindError('Unable to find image %s' % image_name.get_filename())

    elif isinstance(image_name, str):
        a_match = text_search_by(image_name, True, region)
        if a_match is not None:
            return Location(a_match['x'] + a_match['width'] / 2, a_match['y'] + a_match['height'] / 2)
        else:
            raise FindError('Unable to find text %s' % image_name)

    else:
        raise ValueError(INVALID_GENERIC_INPUT)


def find_all(what, in_region=None):
    """Look for multiple matches of a Pattern or image

    :param what: String or Pattern
    :param in_region: Region object in order to minimize the area
    :return:
    """
    if isinstance(what, Pattern):
        return image_search_multiple(what, in_region)

    elif isinstance(what, str):
        all_matches = text_search_by(what, True, in_region, True)
        list_of_locations = []
        for match in all_matches:
            list_of_locations.append(Location(match['x'] + match['width'] / 2, match['y'] + match['height'] / 2))
        if len(list_of_locations) > 0:
            return list_of_locations
        else:
            raise FindError('Unable to find text %s' % what)

    else:
        raise ValueError(INVALID_GENERIC_INPUT)


def wait(image_name, timeout=None, region=None):
    """Wait for a Pattern or image to appear

    :param image_name: String or Pattern
    :param timeout: Number as maximum waiting time in seconds.
    :param region: Region object in order to minimize the area
    :return: True if found
    """
    if isinstance(image_name, Pattern):
        if timeout is None:
            timeout = Settings.auto_wait_timeout

        image_found = positive_image_search(image_name, timeout, region)

        if image_found is not None:
            if parse_args().highlight:
                highlight(region=region, pattern=image_name, location=image_found)
            return True
        else:
            raise FindError('Unable to find image %s' % image_name.get_filename())

    elif isinstance(image_name, str):
        a_match = text_search_by(image_name, True, region)
        if a_match is not None:
            return True
        else:
            raise FindError('Unable to find text %s' % image_name)

    else:
        raise ValueError(INVALID_GENERIC_INPUT)


def exists(pattern, timeout=None, in_region=None):
    """Check if Pattern or image exists

    :param pattern: String or Pattern
    :param timeout: Number as maximum waiting time in seconds.
    :param in_region: Region object in order to minimize the area
    :return: True if found
    """

    if timeout is None:
        timeout = Settings.auto_wait_timeout

    try:
        wait(pattern, timeout, in_region)
        return True
    except FindError:
        return False


def wait_vanish(pattern, timeout=None, in_region=None):
    """Wait until a Pattern disappears

    :param pattern: Pattern
    :param timeout:  Number as maximum waiting time in seconds.
    :param in_region: Region object in order to minimize the area
    :return: True if vanished
    """

    if timeout is None:
        timeout = Settings.auto_wait_timeout

    image_found = negative_image_search(pattern, timeout, in_region)

    if image_found is not None:
        return True
    else:
        raise FindError('%s did not vanish' % pattern.get_filename())

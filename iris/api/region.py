# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from errors import FindError
from image_search import *
from location import Location
from ocr_search import *
from pattern import Pattern
from save_debug_image import save_debug_image
from settings import Settings, DEFAULT_CLICK_DELAY

try:
    import Image
except ImportError:
    from PIL import Image

pyautogui.FAILSAFE = False
logger = logging.getLogger(__name__)


class Region(object):
    def __init__(self, x=0, y=0, w=0, h=0):
        self._x = x
        self._y = y
        self._w = w
        self._h = h

    def debug(self):
        pass
        save_debug_image(None, self, None)

    def debug_ocr(self, with_image_processing=True):
        return self.text(with_image_processing, True)

    def show(self):
        region_screen = get_region(self)
        region_screen.show()

    def getX(self):
        return self._x

    def setX(self, new_x):
        if isinstance(new_x, int):
            self._x = new_x
        else:
            raise ValueError(INVALID_NUMERIC_INPUT)

    x = property(getX, setX)

    def getY(self):
        return self._y

    def setY(self, new_y):
        if isinstance(new_y, int):
            self._y = new_y
        else:
            raise ValueError(INVALID_NUMERIC_INPUT)

    y = property(getY, setY)

    def getW(self):
        return self._w

    def setW(self, new_w):
        if isinstance(new_w, int):
            self._w = new_w
        else:
            raise ValueError(INVALID_NUMERIC_INPUT)

    w = property(getW, setW)

    def getH(self):
        return self._h

    def setH(self, new_h):
        if isinstance(new_h, int):
            self._h = new_h
        else:
            raise ValueError(INVALID_NUMERIC_INPUT)

    h = property(getH, setH)

    def getCenter(self):
        center_x = int(self.x + self.w) / 2
        center_y = int(self.y + self.h) / 2
        return Location(center_x, center_y)

    def moveTo(self, new_location):
        self.x = new_location.getX()
        self.y = new_location.getY()

    def getTopLeft(self):
        return Location(self.x, self.y)

    def getTopRight(self):
        top_right_x = self.x + self.w
        return Location(top_right_x, self.y)

    def getBottomLeft(self):
        bottom_left_y = self.y + self.h
        return Location(self.x, bottom_left_y)

    def getBottomRight(self):
        bottom_right_x = self.x + self.w
        bottom_right_y = self.y + self.h
        return Location(bottom_right_x, bottom_right_y)

    def hover(self, where=None, duration=0):
        return hover(where, duration, self)

    def find(self, what=None, precision=None):
        return find(what, precision, self)

    def findAll(self, what=None, precision=None):
        return findAll(what, precision, self)

    def wait(self, what=None, timeout=None, precision=None):
        wait(what, timeout, precision, self)

    def waitVanish(self, what=None, timeout=None, precision=None):
        return waitVanish(what, timeout, precision, self)

    def exists(self, what=None, timeout=None, precision=None):
        return exists(what, timeout, precision, self)

    def click(self, where=None, duration=None):
        return click(where, duration, self)

    def text(self, with_image_processing=True, with_debug=False):
        return text(with_image_processing, self, with_debug)

    def type(self, text, modifier, interval):
        return type(text, modifier, interval)

    def dragDrop(self, drag_from, drop_to, duration=None):
        return dragDrop(drag_from, drop_to, duration)

    def doubleClick(self, where, duration):
        return doubleClick(where, duration, self)

    def rightClick(self, where, duration):
        return rightClick(where, duration, self)


def generate_region_by_markers(top_left_marker_img=None, bottom_right_marker_img=None):
    try:
        wait(top_left_marker_img, 10)
        exists(bottom_right_marker_img, 10)
    except Exception as err:
        logger.error('Unable to find page markers')
        raise err

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
        found_region.h += padding_top

    if padding_bottom:
        found_region.h += padding_bottom

    if padding_left:
        found_region.x -= padding_left
        found_region.w += padding_left

    if padding_right:
        found_region.w += padding_right

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
        duration = Settings.MoveMouseDelay

    if location is None:
        location = Location(0, 0)

    pyautogui.moveTo(location.x, location.y, duration)
    pyautogui.click(clicks=clicks, interval=Settings.ClickDelay, button=button)

    if Settings.ClickDelay != DEFAULT_CLICK_DELAY:
        Settings.ClickDelay = DEFAULT_CLICK_DELAY


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
        duration = Settings.MoveMouseDelay

    needle = cv2.imread(pattern.image_path)
    height, width, channels = needle.shape

    p_top = positive_image_search(pattern=pattern, precision=Settings.MinSimilarity, region=in_region)

    if p_top is None:
        raise FindError('Unable to click on: %s' % pattern.image_path)

    possible_offset = pattern.getTargetOffset()

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
        duration = Settings.MoveMouseDelay

    if isinstance(where, str) and is_ocr_text(where):
        a_match = text_search_by(where, True, in_region)
        if a_match is not None:
            click_location = Location(a_match['x'] + a_match['width'] / 2, a_match['y'] + a_match['height'] / 2)
            _click_at(click_location, clicks, duration, button)

    elif isinstance(where, Location):
        _click_at(where, clicks, duration, button)

    elif isinstance(where, str) or isinstance(where, Pattern):
        try:
            pattern = Pattern(where)
        except Exception:
            pattern = where

        _click_pattern(pattern, clicks, duration, in_region, button)

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
        duration = Settings.MoveMouseDelay

    _general_click(where, 1, duration, in_region, 'left')


def rightClick(where=None, duration=None, in_region=None):
    """Mouse right click

    :param where: Location , image name or Pattern
    :param duration: speed of hovering from current location to target
    :param in_region: Region object in order to minimize the area
    :return: None
    """

    if duration is None:
        duration = Settings.MoveMouseDelay

    _general_click(where, 1, duration, in_region, 'right')


def doubleClick(where=None, duration=None, in_region=None):
    """Mouse double click

    :param where: Location , image name or Pattern
    :param duration: speed of hovering from current location to target
    :param in_region: Region object in order to minimize the area
    :return: None
    """

    if duration is None:
        duration = Settings.MoveMouseDelay

    _general_click(where, 2, duration, in_region, 'left')


def _to_location(ps=None, in_region=None, align='top_left'):
    """Transform pattern or string to location

    :param ps: Pattern or string input
    :param in_region: Region object in order to minimize the area
    :param align: Alignment could be top_left, center
    :return: Location object
    """

    # TODO: Add multiple alignments if needed

    # TODO fix this (isinstance str or Pattern)

    if isinstance(ps, Location):
        return ps

    elif isinstance(Pattern(ps), Pattern):
        location = image_search(Pattern(ps), Settings.MinSimilarity, in_region)
        if align == 'center':
            width, height = get_image_size(Pattern(ps))
            return Location(location.getX() + width / 2, location.getY() + height / 2)
        else:
            return location


def dragDrop(drag_from, drop_to, duration=None):
    """Mouse drag and drop

    :param drag_from: Starting point for drag and drop. Can be pattern, string or location
    :param drop_to: Ending point for drag and drop. Can be pattern, string or location
    :param duration: speed of drag and drop
    :return: None
    """

    if duration is None:
        duration = Settings.MoveMouseDelay

    from_location = _to_location(ps=drag_from, align='center')
    to_location = _to_location(ps=drop_to, align='center')
    pyautogui.moveTo(from_location.x, from_location.y, 0)

    time.sleep(Settings.DelayBeforeMouseDown)
    pyautogui.mouseDown(button='left', _pause=False)

    time.sleep(Settings.DelayBeforeDrag)
    pyautogui._mouseMoveDrag('drag', to_location.x, to_location.y, 0, 0, duration, pyautogui.linear, 'left')

    time.sleep(Settings.DelayBeforeDrop)
    pyautogui.mouseUp(button='left', _pause=False)


def text(with_image_processing=True, in_region=None, debug=False):
    """Get all text from a Region or full screen

    :param bool with_image_processing: With extra dpi and contrast image processing
    :param Region in_region: In certain Region or full screen
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
    if isinstance(where, str) and is_ocr_text(where):
        a_match = text_search_by(where, True, in_region)
        if a_match is not None:
            pyautogui.moveTo(a_match['x'] + a_match['width'] / 2, a_match['y'] + a_match['height'] / 2)
        else:
            raise FindError('Unable to find text %s' % where)

    elif isinstance(where, Location):
        pyautogui.moveTo(where.x, where.y, duration)

    elif isinstance(where, str) or isinstance(where, Pattern):

        try:
            pattern = Pattern(where)
        except Exception:
            pattern = where

        pos = image_search(pattern, region=in_region)
        if pos.x != -1:
            needle_width, needle_height = get_image_size(pattern.getFilename())
            if isinstance(where, Pattern):
                possible_offset = where.getTargetOffset()
                if possible_offset is not None:
                    move_to = Location(pos.getX() + possible_offset.getX(), pos.getY() + possible_offset.getY())
                    pyautogui.moveTo(move_to.getX(), move_to.y)
                else:
                    move_to = Location(pos.x, pos.y)
                    pyautogui.moveTo(move_to.getX() + needle_width / 2, move_to.getY() + needle_height / 2)
            else:
                pyautogui.moveTo(pos.x + needle_width / 2, pos.y + needle_height / 2)
        else:
            raise FindError('Unable to find image %s' % pattern.getFilename())

    else:
        raise ValueError(INVALID_GENERIC_INPUT)


def find(image_name, precision=None, in_region=None):
    """Look for a single match of a Pattern or image

    :param image_name: String or Pattern
    :param precision: Matching similarity
    :param in_region: Region object in order to minimize the area
    :return: Location
    """

    if isinstance(image_name, str) and is_ocr_text(image_name):
        a_match = text_search_by(image_name, True, in_region)
        if a_match is not None:
            return Location(a_match['x'] + a_match['width'] / 2, a_match['y'] + a_match['height'] / 2)
        else:
            raise FindError('Unable to find text %s' % image_name)

    elif isinstance(image_name, str) or isinstance(image_name, Pattern):

        if precision is None:
            precision = Settings.MinSimilarity

        try:
            pattern = Pattern(image_name)
        except Exception:
            pattern = image_name

        image_found = image_search(pattern, precision, in_region)
        if (image_found.x != -1) & (image_found.y != -1):
            return image_found
        else:
            raise FindError('Unable to find image %s' % image_name)

    else:
        raise ValueError(INVALID_GENERIC_INPUT)


def findAll(what, precision=None, in_region=None):
    """Look for multiple matches of a Pattern or image

    :param what: String or Pattern
    :param precision: Matching similarity
    :param in_region: Region object in order to minimize the area
    :return:
    """

    if isinstance(what, str) and is_ocr_text(what):
        all_matches = text_search_by(what, True, in_region, True)
        list_of_locations = []
        for match in all_matches:
            list_of_locations.append(Location(match['x'] + match['width'] / 2, match['y'] + match['height'] / 2))
        if len(list_of_locations) > 0:
            return list_of_locations
        else:
            raise FindError('Unable to find text %s' % what)

    elif isinstance(what, str) or isinstance(what, Pattern):
        try:
            pattern = Pattern(what)
        except Exception:
            pattern = what

        if precision is None:
            precision = Settings.MinSimilarity

        return image_search_multiple(pattern, precision, in_region)
    else:
        raise ValueError(INVALID_GENERIC_INPUT)


def wait(image_name, timeout=None, precision=None, in_region=None):
    """Wait for a Pattern or image to appear

    :param image_name: String or Pattern
    :param timeout: Number as maximum waiting time in seconds.
    :param precision: Matching similarity
    :param in_region: Region object in order to minimize the area
    :return: True if found
    """
    if isinstance(image_name, str) and is_ocr_text(image_name):
        a_match = text_search_by(image_name, True, in_region)
        if a_match is not None:
            return True
        else:
            raise FindError('Unable to find text %s' % image_name)

    elif isinstance(image_name, str) or isinstance(image_name, Pattern):
        if timeout is None:
            timeout = Settings.AutoWaitTimeout

        if precision is None:
            precision = Settings.MinSimilarity

        try:
            pattern = Pattern(image_name)
        except Exception:
            pattern = image_name

        image_found = positive_image_search(pattern, timeout, precision, in_region)

        if image_found is not None:
            return True
        else:
            raise FindError('Unable to find image %s' % image_name)

    else:
        raise ValueError(INVALID_GENERIC_INPUT)


def exists(pattern, timeout=None, precision=None, in_region=None):
    """Check if Pattern or image exists

    :param pattern: String or Pattern
    :param timeout: Number as maximum waiting time in seconds.
    :param precision: Matching similarity
    :param in_region: Region object in order to minimize the area
    :return: True if found
    """

    if timeout is None:
        timeout = Settings.AutoWaitTimeout

    if precision is None:
        precision = Settings.MinSimilarity

    try:
        wait(pattern, timeout, precision, in_region)
        return True
    except FindError:
        return False


def waitVanish(image_name, timeout=None, precision=None, in_region=None):
    """Wait until a Pattern or image disappears

    :param image_name: Image, Pattern or string
    :param timeout:  Number as maximum waiting time in seconds.
    :param precision: Matching similarity
    :param in_region: Region object in order to minimize the area
    :return: True if vanished
    """

    if timeout is None:
        timeout = Settings.AutoWaitTimeout

    if precision is None:
        precision = Settings.MinSimilarity

    pattern = Pattern(image_name)
    image_found = negative_image_search(pattern, timeout, precision, in_region)

    if image_found is not None:
        return True
    else:
        raise FindError('%s did not vanish' % image_name)

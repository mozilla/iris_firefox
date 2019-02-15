# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from errors import FindError
from key import key_up, key_down, paste
from key import type
from mouse import click, double_click, right_click, drag_drop, mouse_move, mouse_press, mouse_release
from util.color import Color
from util.highlight_rectangle import HighlightRectangle
from util.image_search import *
from util.ocr_search import *
from util.save_debug_image import save_debug_image
from util.screen_highlight import ScreenHighlight

try:
    import Image
except ImportError:
    from PIL import Image

pyautogui.FAILSAFE = False
logger = logging.getLogger(__name__)


class Region(object):
    """Region is a rectangular area on a screen, which is defined by its upper left corner (x, y) as a distance relative
     to the upper left corner of the screen (0, 0) and its dimension (w, h) as its width and height.

     Coordinates are based on screen coordinates.

     origin                               top
        +-----> x increases                |
        |                           left  -+-  right
        v                                  |
     y increases                         bottom
     """

    def __init__(self, x=0, y=0, width=0, height=0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def __str__(self):
        return '(%s, %s, %s, %s)' % (self.x, self.y, self.width, self.height)

    def __repr__(self):
        return '%s(%r, %r, %r, %r)' % (self.__class__.__name__, self.x, self.y, self.width, self.height)

    def top_half(self):
        return Region.screen_regions(self, 'TOP_HALF')

    def bottom_half(self):
        return Region.screen_regions(self, 'BOTTOM_HALF')

    def left_half(self):
        return Region.screen_regions(self, 'LEFT_HALF')

    def right_half(self):
        return Region.screen_regions(self, 'RIGHT_HALF')

    def top_third(self):
        return Region.screen_regions(self, 'TOP_THIRD')

    def middle_third_horizontal(self):
        return Region.screen_regions(self, 'MIDDLE_THIRD_HORIZONTAL')

    def bottom_third(self):
        return Region.screen_regions(self, 'BOTTOM_THIRD')

    def left_third(self):
        return Region.screen_regions(self, 'LEFT_THIRD')

    def middle_third_vertical(self):
        return Region.screen_regions(self, 'MIDDLE_THIRD_VERTICAL')

    def right_third(self):
        return Region.screen_regions(self, 'RIGHT_THIRD')

    def upper_left_corner(self):
        return Region.screen_regions(self, 'UPPER_LEFT_CORNER')

    def upper_right_corner(self):
        return Region.screen_regions(self, 'UPPER_RIGHT_CORNER')

    def lower_left_corner(self):
        return Region.screen_regions(self, 'LOWER_LEFT_CORNER')

    def lower_right_corner(self):
        return Region.screen_regions(self, 'LOWER_RIGHT_CORNER')

    def get_center(self):
        """Returns a Location object for the center of te screen."""
        return Location(int(self.x + self.width) / 2, int(self.y + self.height) / 2)

    def move_to(self, location):
        """Set the position of this region regarding it's top left corner to the given location"""
        self.x = location.x
        self.y = location.y

    def get_top_left_coordinates(self):
        """Returns a Location object for the top left of te screen."""
        return Location(self.x, self.y)

    def get_top_right_coordinates(self):
        """Returns a Location object for the top right of te screen."""
        return Location(self.x + self.width, self.y)

    def get_bottom_left_coordinates(self):
        """Returns a Location object for the bottom left of te screen."""
        return Location(self.x, self.y + self.height)

    def get_bottom_right_coordinates(self):
        """Returns a Location object for the bottom right of te screen."""
        return Location(self.x + self.width, self.y + self.height)

    def debug(self):
        """Saves input image for debug. """
        save_debug_image(None, self, None)

    def debug_ocr(self, image_processing=True):
        """
        :param with_image_processing: With extra dpi and contrast image processing.
        :return: Call the text() method.
        """
        return self.text(image_processing, True)

    def show(self):
        """Displays the screen region. This method is mainly intended for debugging purposes."""
        region_screen = IrisCore.get_region(self)
        region_screen.show()

    def hover(self, where=None, duration=0):
        """Hover over a Location, Pattern or image.

        :param where: Location, Pattern or image name for hover target.
        :param duration: Speed of hovering from current location to target.
        :return: Call the hover() method.
        """
        return hover(where, duration, self)

    def find(self, what=None):
        """Look for a single match of a Pattern or image.

        :param what: String or Pattern.
        :return: Call the find() method.
        """
        return find(what, self)

    def find_all(self, what=None):
        """Look for multiple matches of a Pattern or image.

        :param what: String or Pattern.
        :return: Call the find_all() method.
        """
        return find_all(what, self)

    def wait(self, what=None, timeout=None):
        """Wait for a Pattern or image to appear.

        :param what: String or Pattern.
        :param timeout: Number as maximum waiting time in seconds.
        :return: None.
        """
        wait(what, timeout, self)

    def wait_vanish(self, what=None, timeout=None):
        """Wait until a Pattern disappears.

        :param what: Pattern.
        :param timeout: Number as maximum waiting time in seconds.
        :return: Call the wait_vanish() method.
        """
        return wait_vanish(what, timeout, self)

    def exists(self, what=None, timeout=None):
        """Check if Pattern or image exists.

        :param what: String or Pattern.
        :param timeout: Number as maximum waiting time in seconds.
        :return: Call the exists() method.
        """
        return exists(what, timeout, self)

    def click(self, where=None, duration=None):
        """Mouse left click.

        :param where: Location , image name or Pattern.
        :param duration: Speed of hovering from current location to target.
        :return: Call the click() method.
        """
        return click(where, duration, self)

    def text(self, image_processing, with_debug=False):
        """
        :param bool with_image_processing: With extra dpi and contrast image processing.
        :param bool with_debug: Boolean for saving ocr images.
        :return: Call the text() method.
        """
        return text(image_processing, self, with_debug)

    def highlight(self, seconds=None, color=None):
        """
        :param seconds: How many seconds the region is highlighted. By default the region is highlighted for 2 seconds.
        :param color: Color used to highlight the region. Default color is red.
        :return: None.
        """
        highlight(self, seconds, color)

    @staticmethod
    def type(txt, modifier, interval):
        """Performs a keyboard key press down, followed by a release, for each of the characters in message.

        :param str || list txt: If a string, then the characters to be pressed. If a list, then the key names of the
                                keys to press in order.
        :param modifier: Key modifier.
        :param interval: Type delay. By default it is 0 seconds.
        :return: Call the type() method.
        """
        return type(txt, modifier, interval)

    @staticmethod
    def drag_drop(drag_from, drop_to, duration=None):
        """Mouse drag and drop.

        :param drag_from: Starting point for drag and drop. Can be pattern, string or location.
        :param drop_to: Ending point for drag and drop. Can be pattern, string or location.
        :param duration: Speed of drag and drop.
        :return: Call the drag_drop() method.
        """
        return drag_drop(drag_from, drop_to, duration)

    def double_click(self, where, duration):
        """Mouse double click.

        :param where: Location , image name or Pattern.
        :param duration: Speed of hovering from current location to target.
        :return: Call the double_click() method.
        """
        return double_click(where, duration, self)

    def right_click(self, where, duration):
        """Mouse right click.

        :param where: Location , image name or Pattern.
        :param duration: Speed of hovering from current location to target.
        :return: Call the right_click() method.
        """
        return right_click(where, duration, self)

    @staticmethod
    def key_up(key):
        """Performs a keyboard key release (without the press down beforehand).

        :param key: The key to be released up.
        :return: Call the key_up() method.
        """
        return key_up(key)

    @staticmethod
    def key_down(key):
        """Performs a keyboard key press without the release. This will put that key in a held down state.

        :param key: The key to be pressed down.
        :return: Call the key_down() method.
        """
        return key_down(key)

    @staticmethod
    def paste(clipboard):
        """Paste from clipboard.

        :param clipboard: Content of clipboard.
        :return: Call the paste() method.
        """
        return paste(clipboard)

    def mouse_move(self, where=None, duration=None):
        """Move mouse location.

        :param where: Location , image name or Pattern.
        :param duration: Speed of hovering from current location to target.
        :return: Call the mouse_move() method.
        """
        return mouse_move(where, duration, self)

    def mouse_press(self, where, button=None):
        """Mouse press.

        :param where: Location , image name or Pattern.
        :param button: 'left','right' or 'middle'.
        :return: Call the mouse_press() method.
        """
        return mouse_press(where, button, self)

    def mouse_release(self, where, button=None):
        """Mouse release.

        :param where: Location , image name or Pattern.
        :param button: 'left','right' or 'middle'.
        :return: Call the mouse_release() method.
        """

        return mouse_release(where, button, self)

    @staticmethod
    def get_matrix(number_of_columns, number_of_lines, in_region=None):
        """Returns a "matrix" object(a list of lists) containing new Region objects representing that Region's
        subdivisions."""

        list_of_lists = []
        regions = []

        start_x = in_region.x
        start_y = in_region.y
        width = in_region.width
        height = in_region.height

        sub_region_width = width / number_of_columns
        sub_region_height = height / number_of_lines

        for i in range(number_of_lines):
            for j in range(number_of_columns):
                sub_region_x = (j * sub_region_width) + start_x
                sub_region_y = (i * sub_region_height) + start_y
                regions.append(Region(sub_region_x, sub_region_y, sub_region_width, sub_region_height))

            list_of_lists.append(regions)
            regions = []

        return list_of_lists

    @staticmethod
    def screen_regions(region, caption):
        captions = {
            'TOP_HALF': Region.get_matrix(1, 2, region)[0][0],
            'BOTTOM_HALF': Region.get_matrix(1, 2, region)[1][0],

            'LEFT_HALF': Region.get_matrix(2, 1, region)[0][0],
            'RIGHT_HALF': Region.get_matrix(2, 1, region)[0][1],

            'TOP_THIRD': Region.get_matrix(1, 3, region)[0][0],
            'MIDDLE_THIRD_HORIZONTAL': Region.get_matrix(1, 3, region)[1][0],
            'BOTTOM_THIRD': Region.get_matrix(1, 3, region)[2][0],

            'LEFT_THIRD': Region.get_matrix(3, 1, region)[0][0],
            'MIDDLE_THIRD_VERTICAL': Region.get_matrix(3, 1, region)[0][1],
            'RIGHT_THIRD': Region.get_matrix(3, 1, region)[0][2],

            'UPPER_LEFT_CORNER': Region.get_matrix(2, 2, region)[0][0],
            'UPPER_RIGHT_CORNER': Region.get_matrix(2, 2, region)[0][1],
            'LOWER_LEFT_CORNER': Region.get_matrix(2, 2, region)[1][0],
            'LOWER_RIGHT_CORNER': Region.get_matrix(2, 2, region)[1][1],
        }
        return captions.get(caption)


def highlight(region=None, seconds=None, color=None, pattern=None, location=None):
    """
    :param region: Screen region to be highlighted.
    :param seconds: How many seconds the region is highlighted. By default the region is highlighted for 2 seconds.
    :param color: Color used to highlight the region. Default color is red.
    :param pattern: Pattern.
    :param location: Location.
    :return: None.
    """
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
        width, height = pattern.get_size()
        hl.draw_rectangle(HighlightRectangle(location.x, location.y, width, height, color))

    hl.render(seconds)
    time.sleep(seconds)


def generate_region_by_markers(top_left_marker_img=None, bottom_right_marker_img=None):
    """Generate a region starting from 2 markers.

    :param top_left_marker_img: Top left pattern used to generate the region.
    :param bottom_right_marker_img: Bottom right pattern used to generate the region.
    :return: Screen region generated.
    """
    try:
        wait(top_left_marker_img, 10)
        exists(bottom_right_marker_img, 10)
    except FindError:
        raise FindError('Unable to find page markers.')

    top_left_pos = find(top_left_marker_img)
    hover(top_left_pos, 0)
    bottom_right_pos = find(bottom_right_marker_img)
    hover(bottom_right_pos, 0)

    marker_width, marker_height = bottom_right_marker_img.get_size()

    return Region(top_left_pos.x,
                  top_left_pos.y,
                  (bottom_right_pos.x + marker_width),
                  bottom_right_pos.y - top_left_pos.y + marker_height)


def create_region_from_patterns(top=None, bottom=None, left=None, right=None, padding_top=None, padding_bottom=None,
                                padding_left=None, padding_right=None):
    """Returns a region created from combined area of one or more patterns. Argument names are just for convenience and
    don't influence outcome.

    :param top: Top pattern used to generate the region.
    :param bottom: Bottom pattern used to generate the region.
    :param left: Left pattern used to generate the region.
    :param right: Right pattern used to generate the region.
    :param padding_top: Padding to be added to the pattern's top.
    :param padding_bottom: Padding to be added to the pattern's bottom.
    :param padding_left: Padding to be added to the pattern's left.
    :param padding_right: Padding to be added to the pattern's right.
    :return: region created from combined area of one or more patterns.
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

            w, h = pattern.get_size()

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


def text(image_processing, in_region=None, debug=False):
    """Get all text from a Region or full screen.

    :param bool with_image_processing: With extra dpi and contrast image processing.
    :param Region in_region: In certain Region or full screen.
    :param debug: Boolean for saving ocr images.
    :return: List of matches.
    """

    ocr_search = OCRSearch()
    all_text, debug_img, debug_data = ocr_search.text_search_all(image_processing, in_region)
    if debug and debug_img is not None:
        ocr_search.save_ocr_debug_image(debug_img, debug_data)
        logger.debug('> Found message: %s' % ocr_search.ocr_matches_to_string(all_text))
    return ocr_search.ocr_matches_to_string(all_text)


def hover(where=None, duration=0, in_region=None):
    """Hover over a Location, Pattern or image.

    :param where: Location, Pattern or image name for hover target.
    :param duration: Speed of hovering from current location to target.
    :param in_region: Region object in order to minimize the area.
    :return: None.
    """
    if isinstance(where, Pattern):
        pos = image_search(where, region=in_region)
        if pos.x != -1:
            needle_width, needle_height = where.get_size()
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
        ocr_search = OCRSearch()
        a_match = ocr_search.text_search_by(where, True, in_region)
        if a_match is not None:
            pyautogui.moveTo(a_match['x'] + a_match['width'] / 2, a_match['y'] + a_match['height'] / 2)
        else:
            raise FindError('Unable to find text %s' % where)

    elif isinstance(where, Location):
        pyautogui.moveTo(where.x, where.y, duration)

    else:
        raise ValueError(INVALID_GENERIC_INPUT)


def find(image_name, region=None):
    """Look for a single match of a Pattern or image.

    :param image_name: String or Pattern.
    :param region: Region object in order to minimize the area.
    :return: Location object.
    """
    if parse_args().highlight:
        highlight(region=region)

    if isinstance(image_name, Pattern):
        image_found = image_search(image_name, region)
        if (image_found.x != -1) & (image_found.y != -1):
            if parse_args().highlight:
                highlight(region=region, pattern=image_name, location=image_found)
            return image_found
        else:
            raise FindError('Unable to find image %s' % image_name.get_filename())

    elif isinstance(image_name, str):
        ocr_search = OCRSearch()
        a_match = ocr_search.text_search_by(image_name, True, region)
        if a_match is not None:
            return Location(a_match['x'] + a_match['width'] / 2, a_match['y'] + a_match['height'] / 2)
        else:
            raise FindError('Unable to find text %s' % image_name)

    else:
        raise ValueError(INVALID_GENERIC_INPUT)


def find_all(what, in_region=None):
    """Look for multiple matches of a Pattern or image.

    :param what: String or Pattern.
    :param in_region: Region object in order to minimize the area.
    :return: List[Location].
    """
    if isinstance(what, Pattern):
        return image_search_multiple(what, in_region)

    elif isinstance(what, str):
        ocr_search = OCRSearch()
        all_matches = ocr_search.text_search_by(what, True, in_region, True)
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
    """Wait for a Pattern or image to appear.

    :param image_name: String or Pattern.
    :param timeout: Number as maximum waiting time in seconds.
    :param region: Region object in order to minimize the area.
    :return: True if found.
    """
    if parse_args().highlight:
        highlight(region=region)

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
        ocr_search = OCRSearch()
        a_match = ocr_search.text_search_by(image_name, True, region)
        if a_match is not None:
            return True
        else:
            raise FindError('Unable to find text %s' % image_name)

    else:
        raise ValueError(INVALID_GENERIC_INPUT)


def exists(pattern, timeout=None, in_region=None):
    """Check if Pattern or image exists.

    :param pattern: String or Pattern.
    :param timeout: Number as maximum waiting time in seconds.
    :param in_region: Region object in order to minimize the area.
    :return: True if found.
    """

    if timeout is None:
        timeout = Settings.auto_wait_timeout

    try:
        wait(pattern, timeout, in_region)
        return True
    except FindError:
        return False


def wait_vanish(pattern, timeout=None, in_region=None):
    """Wait until a Pattern disappears.

    :param pattern: Pattern.
    :param timeout:  Number as maximum waiting time in seconds.
    :param in_region: Region object in order to minimize the area.
    :return: True if vanished.
    """

    if timeout is None:
        timeout = Settings.auto_wait_timeout

    image_found = negative_image_search(pattern, timeout, in_region)

    if image_found is not None:
        return True
    else:
        raise FindError('%s did not vanish' % pattern.get_filename())

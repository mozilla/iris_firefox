# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import Queue
import time

import cv2
import numpy as np

try:
    import Image
except ImportError:
    from PIL import Image

from core_helper import *
from iris.api.core.pattern import Pattern
from iris.api.core.settings import Settings
from iris.api.core.location import Location
from save_debug_image import save_debug_image

logger = logging.getLogger(__name__)

FIND_METHOD = cv2.TM_CCOEFF_NORMED


def _calculate_interval_max_attempts(timeout=None):
    if timeout is None:
        timeout = Settings.auto_wait_timeout

    wait_scan_rate = float(Settings.wait_scan_rate)
    interval = 1 / wait_scan_rate
    max_attempts = int(timeout * wait_scan_rate)
    return interval, max_attempts


def is_pattern_size_correct(pattern, region):
    p_width, p_height = pattern.get_size()
    r_width = region.width if region else SCREEN_WIDTH
    r_height = region.height if region else SCREEN_HEIGHT
    is_correct = True

    if p_width > r_width:
        logger.warning('Pattern Width (%s) greater than Region/Screenshot Width (%s)' % (p_width, r_width))
        is_correct = False
    if p_height > r_height:
        logger.warning('Pattern Height (%s) greater than Region/Screenshot Height (%s)' % (p_height, r_height))
        is_correct = False
    return is_correct


def iris_image_match_template(needle, haystack, precision, threshold=None):
    """Finds a match or a list of matches.

    :param needle:  Image details (needle).
    :param haystack: Region as Image (haystack).
    :param float precision: Min allowed similarity.
    :param float || None threshold:  Max threshold.
    :return: A location or a list of locations.
    """
    is_multiple = threshold is not None

    try:
        res = cv2.matchTemplate(np.array(needle), np.array(haystack), FIND_METHOD)
    except Exception:
        res = Location(-1, -1)

    if not is_multiple:
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        logger.debug('Match score: %s. Desired precision: %s' % (max_val, precision))
        if max_val < precision:
            return Location(-1, -1)
        else:
            position = Location(max_loc[0], max_loc[1])
            return position
    else:
        if precision > threshold:
            precision = threshold

        w, h = needle.size
        points = []
        while True:
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            if FIND_METHOD in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
                top_left = min_loc
            else:
                top_left = max_loc

            if max_val > precision:
                sx, sy = top_left
                for x in range(sx - w / 2, sx + w / 2):
                    for y in range(sy - h / 2, sy + h / 2):
                        try:
                            res[y][x] = np.float32(-10000)
                        except IndexError:
                            pass
                new_match_point = Location(top_left[0], top_left[1])
                points.append(new_match_point)
            else:
                break

        return points


def _match_template_multiple(needle, haystack, threshold=0.99):
    """Search for needle in stack (multiple matches).

    :param Pattern needle:  Image details (needle).
    :param Image.Image haystack: Region as Image (haystack).
    :param float threshold:  Max threshold.
    :return: List of Location.
    """

    precision = needle.similarity

    if precision < 0.99:
        needle = needle.get_gray_image()
        haystack = haystack.convert('L')
    elif precision == 0.99:
        needle = needle.get_color_image()

    found_list = iris_image_match_template(needle, haystack, precision, threshold)
    save_debug_image(needle, haystack, found_list)

    return found_list


def image_search_multiple(pattern, region=None):
    """ Wrapper over _match_template_multiple. Search image (multiple) in a Region or full screen.

    :param Pattern pattern: Image details (needle).
    :param Region region: Region object.
    :return: List[Location].
    """

    stack_image = IrisCore.get_region(region=region)
    return _match_template_multiple(pattern, stack_image)


def _match_template(needle, haystack):
    """Search for needle in stack (single match).

    :param Pattern needle: Image details (needle).
    :param Image.Image haystack: Region as Image (haystack).
    :return: Location.
    """

    precision = needle.similarity

    if precision < 0.99:
        needle = needle.get_gray_image()
        haystack = haystack.convert('L')
    elif precision == 0.99:
        needle = needle.get_color_image()

    position = iris_image_match_template(needle, haystack, precision, None)

    if position.x == -1:
        save_debug_image(needle, np.array(haystack), None, True)
    else:
        save_debug_image(needle, haystack, position)

    return position


def image_search(pattern, region=None):
    """ Wrapper over _match_template. Search image in a Region or full screen

    :param Pattern pattern: Image details (needle).
    :param Region region: Region object.
    :return: Location.
    """
    logger.debug('Searching for pattern: %s' % pattern.get_filename())
    try:
        stack_image = IrisCore.get_region(region=region)
        location = _match_template(pattern, stack_image)
    except ScreenshotError:
        logger.warning('Screenshot failed.')
        location = Location(-1, -1)

    if location.x == -1 or location.y == -1:
        return location
    elif region is not None:
        return Location(location.x + region.x, location.y + region.y)
    else:
        return location


def _add_positive_image_search_result_in_queue(queue, pattern, region=None):
    """Puts result in a queue if image is found.

    :param Queue.Queue queue: Queue where the result of the search is added.
    :param Pattern pattern: name of the searched image.
    :param Region region: Region object.
    """
    result = image_search(pattern, region)
    if result.x != -1:
        queue.put(result)


def _positive_image_search_multiprocess(pattern, timeout=None, region=None):
    """Checks if image is found using multiprocessing.

    :param Pattern pattern: Name of the searched image.
    :param timeout: Number as maximum waiting time in seconds.
    :param Region region: Region object.
    :return: Found image from queue.
    """

    out_q = multiprocessing.Queue()

    interval, max_attempts = _calculate_interval_max_attempts(timeout)

    process_list = []
    for i in range(max_attempts):
        p = multiprocessing.Process(target=_add_positive_image_search_result_in_queue,
                                    args=(out_q, pattern, region))
        process_list.append(p)
        p.start()
        try:
            return out_q.get(False)
        except Queue.Empty:
            pass
        time.sleep(interval)
        p.join()

        try:
            for process in process_list:
                process.terminate()
        except Exception:
            pass
    return None


def _positive_image_search_loop(pattern, timeout=None, region=None):
    """ Search for an image (in loop) in a Region or full screen.

    :param Pattern pattern: Name of the searched image.
    :param timeout: Number as maximum waiting time in seconds.
    :param Region region: Region object.
    :return: Location.
    """

    if timeout is None:
        timeout = Settings.auto_wait_timeout

    start_time = datetime.datetime.now()
    end_time = start_time + datetime.timedelta(seconds=timeout)

    while start_time < end_time:
        time_remaining = end_time - start_time
        logger.debug("Searching for image %s - %s seconds remaining" % (pattern.get_filename(), time_remaining))
        pos = image_search(pattern, region)
        start_time = datetime.datetime.now()
        if pos.x != -1:
            return pos
    return None


def positive_image_search(pattern, timeout=None, region=None):
    if not is_pattern_size_correct(pattern, region):
        return None

    if is_multiprocessing_enabled():
        return _positive_image_search_multiprocess(pattern, timeout, region)
    else:
        return _positive_image_search_loop(pattern, timeout, region)


def _add_negative_image_search_result_in_queue(queue, pattern, region=None):
    """Puts result in a queue if image is NOT found.

    :param Queue.Queue queue: Queue where the result of the search is added.
    :param Pattern pattern: Name of the searched image.
    :param Region region: Region object
    """

    result = image_search(pattern, region)
    if result.x == -1:
        queue.put(result)


def _negative_image_search_multiprocess(pattern, timeout=None, region=None):
    """Checks if image is NOT found or it vanished using multiprocessing.

    :param Pattern pattern: Name of the searched image.
    :param timeout: Number as maximum waiting time in seconds.
    :param Region region: Region object.
    :return: Found image from queue.
    """
    out_q = multiprocessing.Queue()

    interval, max_attempts = _calculate_interval_max_attempts(timeout)

    process_list = []
    for i in range(max_attempts):
        p = multiprocessing.Process(target=_add_negative_image_search_result_in_queue,
                                    args=(out_q, pattern, region))
        process_list.append(p)
        p.start()
        try:
            return out_q.get(False)
        except Queue.Empty:
            pass
        time.sleep(interval)
        p.join()

        try:
            for process in process_list:
                process.terminate()
        except Exception:
            pass
    return None


def _negative_image_search_loop(pattern, timeout=None, region=None):
    """ Search if an image (in loop) is NOT in a Region or full screen.

    :param Pattern pattern: Name of the searched image.
    :param timeout: Number as maximum waiting time in seconds.
    :param Region region: Region object.
    :return: Location.
    """

    pattern_found = True

    start_time = datetime.datetime.now()
    end_time = start_time + datetime.timedelta(seconds=timeout)

    while pattern_found is True and start_time < end_time:
        image_found = image_search(pattern, region)
        if (image_found.x != -1) & (image_found.y != -1):
            pattern_found = True
        else:
            pattern_found = False
        start_time = datetime.datetime.now()

    return None if pattern_found else True


def negative_image_search(pattern, timeout=None, region=None):
    if not is_pattern_size_correct(pattern, region):
        return None
    if is_multiprocessing_enabled():
        return _negative_image_search_multiprocess(pattern, timeout, region)
    else:
        return _negative_image_search_loop(pattern, timeout, region)

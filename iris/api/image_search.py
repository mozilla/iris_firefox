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
from pattern import Pattern
from settings import Settings
from location import Location
from save_debug_image import save_debug_image

logger = logging.getLogger(__name__)

FIND_METHOD = cv2.TM_CCOEFF_NORMED


def get_image_size(of_what):
    """Get image size of asset image

    :param str || Pattern of_what: Image name or Pattern object
    :return: width, height as tuple
    """
    needle_path = None
    scale_factor = 1

    if isinstance(of_what, str):
        pattern = Pattern(of_what)
        needle_path = pattern.image_path
        scale_factor = pattern.scale_factor

    elif isinstance(of_what, Pattern):
        needle_path = of_what.image_path
        scale_factor = of_what.scale_factor

    needle = cv2.imread(needle_path)
    height, width, channels = needle.shape
    return int(width / scale_factor), int(height / scale_factor)


def _calculate_interval_max_attempts(timeout=None):
    if timeout is None:
        timeout = Settings.AutoWaitTimeout

    wait_scan_rate = float(Settings.WaitScanRate)
    interval = 1 / wait_scan_rate
    max_attempts = int(timeout * wait_scan_rate)
    return interval, max_attempts


def iris_image_match_template(needle, haystack, precision, threshold=None):
    """Finds a match or a list of matches

    :param needle:  Image details (needle)
    :param haystack: Region as Image (haystack)
    :param float precision: Min allowed similarity
    :param float || None threshold:  Max threshold
    :return: A location or a list of locations
    """
    is_multiple = threshold is not None

    try:
        res = cv2.matchTemplate(np.array(needle), np.array(haystack), FIND_METHOD)
    except Exception:
        res = Location(-1, -1)

    if not is_multiple:
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        if max_val < precision:
            return Location(-1, -1)
        else:
            position = Location(max_loc[0], max_loc[1])
            return position
    else:
        if precision > threshold:
            precision = threshold

        w, h = needle.shape[::-1]
        points = []
        while True:
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            if FIND_METHOD in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
                top_left = min_loc
            else:
                top_left = max_loc

            if threshold > max_val > precision:
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


def _match_template_multiple(needle, haystack, precision=None, threshold=0.99):
    """Search for needle in stack (multiple matches)

    :param Pattern needle:  Image details (needle)
    :param Image.Image haystack: Region as Image (haystack)
    :param float precision: Min allowed similarity
    :param float threshold:  Max threshold
    :return: List of Location
    """

    if precision is None:
        precision = Settings.MinSimilarity

    if precision is None:
        precision = Settings.MinSimilarity

    haystack_img_gray = haystack.convert('L')
    needle_img_gray = needle.gray_image

    found_list = iris_image_match_template(needle_img_gray, haystack_img_gray, precision, threshold)

    if is_image_save_enabled():
        save_debug_image(needle, haystack, found_list)

    return found_list


def image_search_multiple(pattern, precision=None, region=None):
    """ Wrapper over _match_template_multiple. Search image (multiple) in a Region or full screen

    :param Pattern pattern: Image details (needle)
    :param float precision: Min allowed similarity
    :param Region region: Region object
    :return: List[Location]
    """

    if precision is None:
        precision = Settings.MinSimilarity

    stack_image = get_region(region=region)
    return _match_template_multiple(pattern, stack_image, precision)


def _match_template(needle, haystack, precision=None):
    """Search for needle in stack (single match).

    :param Pattern needle: Image details (needle)
    :param Image.Image haystack: Region as Image (haystack)
    :param float precision: Min allowed similarity
    :return: Location
    """

    if precision is None:
        precision = Settings.MinSimilarity

    haystack_img_gray = haystack.convert('L')
    needle_img_gray = needle.gray_image

    position = iris_image_match_template(needle_img_gray, haystack_img_gray, precision, None)

    if is_image_save_enabled():
        if position.getX() == -1:
            save_debug_image(needle_img_gray, np.array(haystack_img_gray), None, True)
        else:
            save_debug_image(needle_img_gray, haystack_img_gray, position)

    return position


def image_search(pattern, precision=None, region=None):
    """ Wrapper over _match_template. Search image in a Region or full screen

    :param Pattern pattern: Image details (needle)
    :param float precision: Min allowed similarity
    :param Region region: Region object
    :return: Location
    """

    if precision is None:
        precision = Settings.MinSimilarity

    stack_image = get_region(region=region)
    location = _match_template(pattern, stack_image, precision)

    if location.x == -1 or location.y == -1:
        return location
    elif region is not None:
        return Location(location.x + region.x, location.y + region.y)
    else:
        return location


def _add_positive_image_search_result_in_queue(queue, pattern, precision=None, region=None):
    """Puts result in a queue if image is found

    :param Queue.Queue queue: Queue where the result of the search is added
    :param Pattern pattern: name of the searched image
    :param float precision: Min allowed similarity
    :param Region region: Region object
    :return:
    """

    if precision is None:
        precision = Settings.MinSimilarity

    result = image_search(pattern, precision, region)
    if result.getX() != -1:
        queue.put(result)


def _positive_image_search_multiprocess(pattern, timeout=None, precision=None, region=None):
    """Checks if image is found using multiprocessing

    :param Pattern pattern: name of the searched image
    :param timeout: Number as maximum waiting time in seconds.
    :param float precision: Min allowed similarity
    :param Region region: Region object
    :return: Found image from queue
    """

    out_q = multiprocessing.Queue()

    interval, max_attempts = _calculate_interval_max_attempts(timeout)

    if precision is None:
        precision = Settings.MinSimilarity

    process_list = []
    for i in range(max_attempts):
        p = multiprocessing.Process(target=_add_positive_image_search_result_in_queue,
                                    args=(out_q, pattern, precision, region))
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


def _positive_image_search_loop(pattern, timeout=None, precision=None, region=None):
    """ Search for an image (in loop) in a Region or full screen

    :param Pattern pattern: name of the searched image
    :param timeout: Number as maximum waiting time in seconds.
    :param float precision: Min allowed similarity
    :param Region region: Region object
    :return: Location
    """

    interval, max_attempts = _calculate_interval_max_attempts(timeout)

    if precision is None:
        precision = Settings.MinSimilarity

    pos = image_search(pattern, precision, region)
    tries = 0
    while pos.getX() == -1 and tries < max_attempts:
        logger.debug("Searching for image %s" % pattern)
        time.sleep(interval)
        pos = image_search(pattern, precision, region)
        tries += 1

    return None if pos.getX() == -1 else pos


def positive_image_search(pattern, timeout=None, precision=None, region=None):
    if is_multiprocessing_enabled():
        return _positive_image_search_multiprocess(pattern, timeout, precision, region)
    else:
        return _positive_image_search_loop(pattern, timeout, precision, region)


def _add_negative_image_search_result_in_queue(queue, pattern, precision=None, region=None):
    """Puts result in a queue if image is NOT found

    :param Queue.Queue queue: Queue where the result of the search is added
    :param Pattern pattern: name of the searched image
    :param float precision: Min allowed similarity
    :param Region region: Region object
    :return:
    """

    if precision is None:
        precision = Settings.MinSimilarity

    result = image_search(pattern, precision, region)
    if result.getX() == -1:
        queue.put(result)


def _negative_image_search_multiprocess(pattern, timeout=None, precision=None, region=None):
    """Checks if image is NOT found or it vanished using multiprocessing

    :param Pattern pattern: name of the searched image
    :param timeout: Number as maximum waiting time in seconds.
    :param float precision: Min allowed similarity
    :param Region region: Region object
    :return: Found image from queue
    """
    out_q = multiprocessing.Queue()

    interval, max_attempts = _calculate_interval_max_attempts(timeout)

    if precision is None:
        precision = Settings.MinSimilarity

    process_list = []
    for i in range(max_attempts):
        p = multiprocessing.Process(target=_add_negative_image_search_result_in_queue,
                                    args=(out_q, pattern, precision, region))
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


def _negative_image_search_loop(pattern, timeout=None, precision=None, region=None):
    """ Search if an image (in loop) is NOT in a Region or full screen

    :param Pattern pattern: name of the searched image
    :param timeout: Number as maximum waiting time in seconds.
    :param float precision: Min allowed similarity
    :param Region region: Region object
    :return: Location
    """

    interval, max_attempts = _calculate_interval_max_attempts(timeout)

    if precision is None:
        precision = Settings.MinSimilarity

    pattern_found = True
    tries = 0

    while pattern_found is True and tries < max_attempts:
        image_found = image_search(pattern, precision, region)
        if (image_found.x != -1) & (image_found.y != -1):
            pattern_found = True
        else:
            pattern_found = False
        tries += 1
        time.sleep(interval)

    return None if pattern_found else True


def negative_image_search(pattern, timeout=None, precision=None, region=None):
    if is_multiprocessing_enabled():
        return _negative_image_search_multiprocess(pattern, timeout, precision, region)
    else:
        return _negative_image_search_loop(pattern, timeout, precision, region)

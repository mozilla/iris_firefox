import time

from src.core.api.errors import APIHelperError
from src.core.api.finder.finder import wait, exists
from src.core.api.finder.pattern import Pattern
from src.core.api.keyboard.key import Key
from src.core.api.keyboard.keyboard_api import paste
from src.core.api.keyboard.keyboard_api import type
from targets.firefox.firefox_ui.helpers.keyboard_shortcuts import select_location_bar
from targets.firefox.firefox_ui.nav_bar import NavBar



INVALID_GENERIC_INPUT = 'Invalid input'
INVALID_NUMERIC_INPUT = 'Expected numeric value'


def confirm_firefox_launch(image=None):
    """Waits for firefox to exist by waiting for the iris logo to be present.
    :param image: Pattern to confirm Firefox launch
    :return: None.
    """
    if image is None:
        image = NavBar.HOME_BUTTON

    try:
        wait(image, 60)
    except Exception:
        raise APIHelperError('Can\'t launch Firefox - aborting test run.')
def repeat_key_down(num):
    """Repeat DOWN keystroke a given number of times.

    :param num: Number of times to repeat DOWN key stroke.
    :return: None.
    """
    for i in range(num):
        type(Key.DOWN)


def repeat_key_down_until_image_found(image_pattern, num_of_key_down_presses=10, delay_between_presses=3):
    """
    Press the Key Down button until specified image pattern is found.

    :param image_pattern: Image Pattern to search.
    :param num_of_key_down_presses: Number of presses of the Key Down button.
    :param delay_between_presses: Number of seconds to wait between the Key Down presses
    :return: Boolean. True if image pattern found during Key Down button pressing, False otherwise
    """

    if not isinstance(image_pattern, Pattern):
        raise ValueError(INVALID_GENERIC_INPUT)

    pattern_found = False

    for _ in range(num_of_key_down_presses):
        pattern_found = exists(image_pattern)
        if pattern_found:
            break

        type(Key.DOWN)
        time.sleep(delay_between_presses)

    return pattern_found


def repeat_key_up(num):
    """Repeat UP keystroke a given number of times.

    :param num: Number of times to repeat UP key stroke.
    :return: None.
    """
    for i in range(num):
        type(Key.UP)


def repeat_key_up_until_image_found(image_pattern, num_of_key_up_presses=10, delay_between_presses=3):
    """
    Press the Key Up button until specified image pattern is found.

    :param image_pattern: Image Pattern to search.
    :param num_of_key_up_presses: Number of presses of the Key Up button.
    :param delay_between_presses: Number of seconds to wait between the Key Down presses
    :return: Boolean. True if image pattern found during the Key Up button pressing, False otherwise
    """

    if not isinstance(image_pattern, Pattern):
        raise ValueError(INVALID_GENERIC_INPUT)

    pattern_found = False

    for _ in range(num_of_key_up_presses):
        pattern_found = exists(image_pattern)
        if pattern_found:
            break

        type(Key.UP)
        time.sleep(delay_between_presses)

    return pattern_found


def navigate(url):
    """Navigates, via the location bar, to a given URL.

    :param url: The string to type into the location bar.
    :return: None.
    """
    try:
        select_location_bar()
        paste(url)
        type(Key.ENTER)
    except Exception:
        raise APIHelperError(
            'No active window found, cannot navigate to page.')

import time

from src.core.api.errors import APIHelperError, FindError
from src.core.api.finder.finder import wait, exists, find
from src.core.api.finder.pattern import Pattern
from src.core.api.keyboard.key import *
from src.core.api.keyboard.keyboard_api  import type
from src.core.api.keyboard.keyboard_api import paste
from src.core.api.mouse.mouse import click
from src.core.api.screen.region import Region
from src.core.api.screen.screen import Screen
from src.core.api.settings import Settings
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

def key_to_one_off_search(highlighted_pattern, direction='left'):
    """Iterate through the one of search engines list until the given one is
    highlighted.

    param: highlighted_pattern: The pattern image to search for.
    param: direction: direction to key to: right or left (default)
    return: None.
    """
    max_attempts = 7
    while max_attempts > 0:
        if exists(highlighted_pattern, 1):
            max_attempts = 0
        else:
            if direction == 'right':
                type(Key.RIGHT)
            else:
                type(Key.LEFT)
            max_attempts -= 1


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


def open_library_menu(option):
    """Open the Library menu with an option as argument.

    :param option: Library menu option.
    :return: Custom region created for a more efficient and accurate image
    pattern search.
    """

    library_menu_pattern = NavBar.LIBRARY_MENU

    try:
        wait(library_menu_pattern, 10)
        region = Region(find(library_menu_pattern).x - Screen().width / 4,
                        find(library_menu_pattern).y, Screen().width / 4,
                        Screen().height / 4)
        logger.debug('Library menu found.')
    except FindError:
        raise APIHelperError(
            'Can\'t find the library menu in the page, aborting test.')
    else:
        time.sleep(Settings.UI_DELAY_LONG)
        click(library_menu_pattern)
        time.sleep(Settings.FX_DELAY)
        try:
            time.sleep(Settings.FX_DELAY)
            region.wait(option, 10)
            logger.debug('Option found.')
            region.click(option)
            return region
        except FindError:
            raise APIHelperError(
                'Can\'t find the option in the page, aborting test.')



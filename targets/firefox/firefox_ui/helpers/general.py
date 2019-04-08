# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
import json
import time

from src.core.api.errors import APIHelperError
from src.core.api.errors import FindError
from src.core.api.finder.finder import find
from src.core.api.finder.finder import wait, exists
from src.core.api.finder.image_search import image_find
from src.core.api.finder.pattern import Pattern
from src.core.api.keyboard.key import *
from src.core.api.keyboard.key import Key
from src.core.api.keyboard.keyboard import type
from src.core.api.keyboard.keyboard_api import paste
from src.core.api.keyboard.keyboard_util import get_clipboard
from src.core.api.mouse.mouse import click
from src.core.api.os_helpers import OSHelper, OSPlatform
from src.core.api.screen.region import Region
from src.core.api.screen.screen import Screen
from src.core.api.settings import Settings
from src.core.util.arg_parser import get_core_args
from src.core.util.logger_manager import logger
from targets.firefox.firefox_ui.content_blocking import ContentBlocking
from targets.firefox.firefox_ui.helpers.keyboard_shortcuts import new_tab, close_tab, edit_select_all, edit_copy
from targets.firefox.firefox_ui.helpers.keyboard_shortcuts import select_location_bar
from targets.firefox.firefox_ui.nav_bar import NavBar

INVALID_GENERIC_INPUT = 'Invalid input'
INVALID_NUMERIC_INPUT = 'Expected numeric value'
args = get_core_args()


def change_preference(pref_name, value):
    """Change the value for a specific preference.

    :param pref_name: Preference to be changed.
    :param value: Preference's value after the change.
    :return: None.
    """
    try:
        new_tab()
        navigate('about:config')
        time.sleep(Settings.DEFAULT_UI_DELAY)

        type(Key.SPACE)
        time.sleep(Settings.DEFAULT_UI_DELAY)

        type(Key.ENTER)
        time.sleep(Settings.DEFAULT_UI_DELAY)

        paste(pref_name)
        time.sleep(Settings.DEFAULT_UI_DELAY)
        type(Key.TAB)
        time.sleep(Settings.DEFAULT_UI_DELAY)
        type(Key.TAB)
        time.sleep(Settings.DEFAULT_UI_DELAY)

        try:
            retrieved_value = copy_to_clipboard()
        except Exception:
            raise APIHelperError(
                'Failed to retrieve preference value.')

        if retrieved_value == value:
            logger.debug('Flag is already set to value:' + value)
            return None
        else:
            type(Key.ENTER)
            dialog_box_pattern = Pattern('preference_dialog_icon.png')
            try:
                wait(dialog_box_pattern, 3)
                paste(value)
                type(Key.ENTER)
            except FindError:
                pass

        close_tab()
    except Exception:
        raise APIHelperError(
            'Could not set value: %s to preference: %s' % (value, pref_name))


def copy_to_clipboard():
    """Return the value copied to clipboard."""
    time.sleep(Settings.DEFAULT_UI_DELAY)
    edit_select_all()
    time.sleep(Settings.DEFAULT_UI_DELAY)
    edit_copy()
    time.sleep(Settings.DEFAULT_UI_DELAY)
    value = get_clipboard()
    time.sleep(Settings.DEFAULT_UI_DELAY)
    logger.debug("Copied to clipboard: %s" % value)
    return value


def close_content_blocking_pop_up():
    """Closes the content blocking pop up"""

    pop_up_region = Screen().new_region(0, 50, Screen.SCREEN_WIDTH / 2, Screen.SCREEN_HEIGHT / 2)

    try:
        pop_up_region.wait(ContentBlocking.POP_UP_ENABLED, 5)
        logger.debug('Content blocking is present on the page and can be closed.')
        pop_up_region.click(ContentBlocking.CLOSE_CB_POP_UP)
    except FindError:
        logger.debug('Couldn\'t find the Content blocking pop up.')
        pass


def click_hamburger_menu_option(option):
    """Click on a specific option from the hamburger menu.

    :param option: Hamburger menu option to be clicked.
    :return: The region created starting from the hamburger menu pattern.
    """
    hamburger_menu_pattern = NavBar.HAMBURGER_MENU
    try:
        wait(hamburger_menu_pattern, 10)
        logger.debug('Hamburger menu found.')
    except FindError:
        raise APIHelperError(
            'Can\'t find the "hamburger menu" in the page, aborting test.')
    else:
        click(hamburger_menu_pattern)
        time.sleep(Settings.DEFAULT_UI_DELAY)
        try:
            region = create_region_from_image(hamburger_menu_pattern)
            region.click(option)
            return region
        except FindError:
            raise APIHelperError(
                'Can\'t find the option in the page, aborting test.')


def confirm_firefox_launch(image=None):
    """Waits for firefox to exist by waiting for the iris logo to be present.
    :param image: Pattern to confirm Firefox launch
    :return: None.
    """
    if image is None:
        image = Pattern('iris_logo.png')

    try:
        wait(image, 60)
    except Exception:
        raise APIHelperError('Can\'t launch Firefox - aborting test run.')


def create_region_from_image(image):
    """Create region starting from a pattern.

    :param image: Pattern used to create a region.
    :return: None.
    """
    try:
        from src.core.api.rectangle import Rectangle
        from src.core.api.enums import Alignment
        m = image_find(image)
        if m:
            sync_pattern = Pattern('sync_hamburger_menu.png')
            sync_width, sync_height = sync_pattern.get_size()
            sync_image = image_find(sync_pattern)
            top_left = Rectangle(sync_image.x, sync_image.y, sync_width, sync_width).\
                apply_alignment(Alignment.TOP_RIGHT)
            if OSHelper.is_mac():
                exit_pattern = Pattern('help_hamburger_menu.png')
            else:
                exit_pattern = Pattern('exit_hamburger_menu.png')
            exit_width, exit_height = exit_pattern.get_size()
            exit_image = image_find(exit_pattern)
            bottom_left = Rectangle(exit_image.x, exit_image.y, exit_width, exit_height).\
                apply_alignment(Alignment.BOTTOM_RIGHT)

            x0 = top_left.x + 2
            y0 = top_left.y
            height = bottom_left.y - top_left.y
            width = Screen().width - top_left.x - 2
            region = Region(x0, y0, width, height)
            return region
        else:
            raise APIHelperError('No matching found.')
    except FindError:
        raise APIHelperError('Image not present.')


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


def select_location_bar_option(option_number):
    """Select option from the location bar menu.

    :param option_number: Option number.
    :return: None.
    """
    if OSHelper.get_os() == OSPlatform.WINDOWS:
        for i in range(option_number + 1):
            type(Key.DOWN)
        type(Key.ENTER)
    else:
        for i in range(option_number - 1):
            type(Key.DOWN)
        type(Key.ENTER)


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
        time.sleep(Settings.DEFAULT_UI_DELAY_LONG)
        click(library_menu_pattern)
        time.sleep(Settings.DEFAULT_UI_DELAY_SHORT)
        try:
            time.sleep(Settings.DEFAULT_UI_DELAY_SHORT)
            region.wait(option, 10)
            logger.debug('Option found.')
            region.click(option)
            return region
        except FindError:
            raise APIHelperError(
                'Can\'t find the option in the page, aborting test.')


def open_about_firefox():
    """Open the 'About Firefox' window."""
    if OSHelper.get_os() == OSPlatform.MAC:
        type(Key.F3, modifier=KeyModifier.CTRL)
        type(Key.F2, modifier=KeyModifier.CTRL)

        time.sleep(0.5)
        type(Key.RIGHT)
        type(Key.DOWN)
        type(Key.DOWN)
        type(Key.ENTER)

    elif OSHelper.get_os() == OSPlatform.WINDOWS:
        type(Key.ALT)
        if args.locale != 'ar':
            type(Key.LEFT)
        else:
            type(Key.RIGHT)
        type(Key.ENTER)
        type(Key.UP)
        type(Key.ENTER)

    else:
        type(Key.F10)
        if args.locale != 'ar':
            type(Key.LEFT)
        else:
            type(Key.RIGHT)
        type(Key.UP)
        type(Key.ENTER)


def get_telemetry_info():
    """Returns telemetry information as a JSON object from 'about:telemetry'
    page.
    """

    copy_raw_data_to_clipboard_pattern = Pattern(
        'copy_raw_data_to_clipboard.png')
    raw_json_pattern = Pattern('raw_json.png')
    raw_data_pattern = Pattern('raw_data.png')

    new_tab()

    paste('about:telemetry')
    type(Key.ENTER)

    try:
        wait(raw_json_pattern, 10)
        logger.debug('\'RAW JSON\' button is present on the page.')
        click(raw_json_pattern)
    except (FindError, ValueError):
        raise APIHelperError('\'RAW JSON\' button not present in the page.')

    try:
        wait(raw_data_pattern, 10)
        logger.debug('\'Raw Data\' button is present on the page.')
        click(raw_data_pattern)
    except (FindError, ValueError):
        close_tab()
        raise APIHelperError('\'Raw Data\' button not present in the page.')

    try:
        click(copy_raw_data_to_clipboard_pattern)
        time.sleep(Settings.DEFAULT_UI_DELAY)
        json_text = get_clipboard()
        return json.loads(json_text)
    except Exception as e:
        raise APIHelperError(
            'Failed to retrieve raw message information value. %s' % e.message)
    finally:
        close_tab()


class RightClickLocationBar(object):
    """Class with location bar members."""

    UNDO = 0
    CUT = 1
    COPY = 2
    PASTE = 3
    PASTE_GO = 4
    DELETE = 5
    SELECT_ALL = 6

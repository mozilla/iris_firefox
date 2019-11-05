# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


import json
import time
import os

from moziris.api.enums import Alignment
from moziris.api.errors import APIHelperError
from moziris.api.errors import FindError
from moziris.api.finder.finder import wait, exists, wait_vanish
from moziris.api.finder.image_search import image_find
from moziris.api.finder.pattern import Pattern
from moziris.api.keyboard.key import *
from moziris.api.keyboard.key import Key
from moziris.api.keyboard.keyboard import type, key_up, key_down
from moziris.api.keyboard.keyboard_api import paste
from moziris.api.keyboard.keyboard_util import get_clipboard
from moziris.api.location import Location
from moziris.api.mouse.mouse import click, hover, Mouse, scroll_down, right_click
from moziris.api.os_helpers import OSHelper, OSPlatform
from moziris.api.rectangle import Rectangle
from moziris.api.screen.region import Region
from moziris.api.screen.screen import Screen
from moziris.api.settings import Settings
from moziris.util.arg_parser import get_core_args
from moziris.util.logger_manager import logger
from moziris.util.region_utils import RegionUtils
from targets.firefox.firefox_ui.content_blocking import ContentBlocking
from targets.firefox.firefox_ui.helpers.keyboard_shortcuts import (
    new_tab,
    close_tab,
    edit_select_all,
    edit_copy,
)
from targets.firefox.firefox_ui.helpers.keyboard_shortcuts import select_location_bar
from targets.firefox.firefox_ui.library_menu import LibraryMenu
from targets.firefox.firefox_ui.nav_bar import NavBar
from targets.firefox.firefox_ui.window_controls import MainWindow, AuxiliaryWindow
from targets.firefox.firefox_ui.location_bar import LocationBar
from targets.firefox.settings import FirefoxSettings

INVALID_GENERIC_INPUT = "Invalid input"
INVALID_NUMERIC_INPUT = "Expected numeric value"
args = get_core_args()


def access_bookmarking_tools(option):
    """Access option from 'Bookmarking Tools'.

    :param option: Option from 'Bookmarking Tools'.
    :return: None.
    """

    bookmarking_tools_pattern = LibraryMenu.BookmarksOption.BOOKMARKING_TOOLS
    open_library_menu(LibraryMenu.BOOKMARKS_OPTION)

    try:
        wait(bookmarking_tools_pattern, 10)
        logger.debug("Bookmarking Tools option has been found.")
        click(bookmarking_tools_pattern)
    except FindError:
        raise APIHelperError("Can't find the Bookmarking Tools option, aborting.")
    try:
        wait(option, 15)
        logger.debug("%s option has been found." % option)
        click(option)
    except FindError:
        raise APIHelperError("Can't find the %s option, aborting." % option)


def change_preference(pref_name, value):
    """Change the value for a specific preference.

    :param pref_name: Preference to be changed.
    :param value: Preference's value after the change.
    :return: None.
    """
    if not isinstance(value, str):
        value = str(value).lower()
    try:
        new_tab()
        navigate("about:config")
        time.sleep(Settings.DEFAULT_UI_DELAY_LONG)

        type(Key.SPACE)
        time.sleep(Settings.DEFAULT_UI_DELAY)

        paste(pref_name)
        time.sleep(Settings.DEFAULT_UI_DELAY)
        type(Key.TAB)
        time.sleep(Settings.DEFAULT_UI_DELAY)

        try:
            retrieved_value = copy_to_clipboard().split("\t")[1]
        except Exception:
            raise APIHelperError("Failed to retrieve preference value.")

        if retrieved_value == value:
            logger.debug("Flag is already set to value:" + value)
            return None
        else:
            type(Key.ENTER)
            if not (value == "true" or value == "false"):
                try:
                    paste(value)
                    type(Key.ENTER)
                except FindError:
                    pass

        close_tab()
    except Exception:
        raise APIHelperError(
            "Could not set value: %s to preference: %s" % (value, pref_name)
        )


def check_preference(pref_name, value):
    """Check the value for a specific preference.

    :param pref_name: Preference to be searched.
    :param value: Preference's value to be checked.
    :return: None.
    """

    new_tab()
    select_location_bar()

    paste("about:config")
    time.sleep(Settings.DEFAULT_UI_DELAY)
    type(Key.ENTER)
    time.sleep(Settings.DEFAULT_UI_DELAY)

    type(Key.SPACE)
    time.sleep(Settings.DEFAULT_UI_DELAY)

    paste(pref_name)

    time.sleep(Settings.DEFAULT_UI_DELAY_LONG)
    type(Key.TAB)
    time.sleep(Settings.DEFAULT_UI_DELAY_LONG)

    try:
        retrieved_value = copy_to_clipboard().split("\t")[1]

    except Exception as e:
        raise APIHelperError("Failed to retrieve preference value. %s" % e.message)

    if retrieved_value == value:
        return True
    else:
        return False


def click_cancel_button():
    """Click cancel button."""
    cancel_button_pattern = Pattern("cancel_button.png").similar(0.7)
    try:
        wait(cancel_button_pattern, 10)
        logger.debug("Cancel button found.")
        click(cancel_button_pattern)
    except FindError:
        raise APIHelperError("Can't find the cancel button, aborting.")


def click_hamburger_menu_option(option):
    """Click on a specific option from the hamburger menu.

    :param option: Hamburger menu option to be clicked.
    :return: The region created starting from the hamburger menu pattern.
    """
    hamburger_menu_pattern = NavBar.HAMBURGER_MENU
    region = Screen.UPPER_RIGHT_CORNER
    try:
        region.wait(hamburger_menu_pattern, 5)
        logger.debug("Hamburger menu found.")
    except FindError:
        raise APIHelperError(
            'Can\'t find the "hamburger menu" in the page, aborting test.'
        )
    else:
        try:
            ham_region = create_region_for_hamburger_menu()
            ham_region.click(option)
        except FindError:
            raise APIHelperError(
                "Can't find the option: "
                + option
                + " in the hamburger menu. Aborting test."
            )


def click_window_control(button, window_type="auxiliary"):
    """Click window with options: close, minimize, maximize, restore, full_screen.

    :param button: Auxiliary or main window options.
    :param window_type: Type of window that need to be controlled.
    :return: None.
    """
    if button == "close":
        close_window_control(window_type)
    elif button == "minimize":
        minimize_window_control(window_type)
    elif button == "maximize":
        maximize_window_control(window_type)
    elif button == "restore":
        restore_window_control(window_type)
    elif button == "full_screen":
        full_screen_control(window_type)
    else:
        raise APIHelperError("Button option is not supported.")


def close_content_blocking_pop_up():
    """Closes the content blocking pop up"""

    pop_up_region = Screen().new_region(
        0, 50, Screen.SCREEN_WIDTH / 2, Screen.SCREEN_HEIGHT / 2
    )

    try:
        pop_up_region.wait(ContentBlocking.POP_UP_ENABLED, 5)
        logger.debug("Content blocking is present on the page and can be closed.")
        pop_up_region.click(ContentBlocking.CLOSE_CB_POP_UP)
    except FindError:
        logger.debug("Couldn't find the Content blocking pop up.")
        pass


def close_customize_page():
    """Close the 'Customize...' page by pressing the 'Done' button."""
    customize_done_button_pattern = Pattern("customize_done_button.png").similar(0.7)
    try:
        wait(customize_done_button_pattern, 10)
        logger.debug("Done button found.")
        click(customize_done_button_pattern)
        time.sleep(Settings.DEFAULT_UI_DELAY_LONG)
    except FindError:
        raise APIHelperError("Can't find the Done button in the page, aborting.")


def close_window_control(window_type):
    """Click on close window control.

    :param window_type: Type of window that need to be closed.
    :return: None.
    """
    find_window_controls(window_type)

    if window_type == "auxiliary":
        if OSHelper.is_mac():
            hover(AuxiliaryWindow.RED_BUTTON_PATTERN)
            click(AuxiliaryWindow.HOVERED_RED_BUTTON)
        else:
            click(AuxiliaryWindow.CLOSE_BUTTON)
    else:
        if OSHelper.is_mac():
            hover(MainWindow.UNHOVERED_MAIN_RED_CONTROL)
            click(MainWindow.HOVERED_MAIN_RED_CONTROL)
        else:
            click(MainWindow.CLOSE_BUTTON)


def confirm_close_multiple_tabs():
    """Click confirm 'Close all tabs' for warning popup when multiple tabs are
    opened.
    """
    close_all_tabs_button_pattern = Pattern("close_all_tabs_button.png")

    try:
        wait(close_all_tabs_button_pattern, 5)
        logger.debug('"Close all tabs" warning popup found.')
        type(Key.ENTER)
    except FindError:
        logger.debug('Couldn\'t find the "Close all tabs" warning popup.')
        pass


def confirm_firefox_launch(image=None):
    """Waits for firefox to exist by waiting for the iris logo to be present.
    :param image: Pattern to confirm Firefox launch
    :return: None.
    """
    if image is None:
        image = Pattern("iris_logo.png")

    try:
        wait(image, 60)
    except Exception:
        raise APIHelperError("Can't launch Firefox - aborting test run.")


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


def create_region_for_awesome_bar():
    """Create region for the awesome bar."""

    try:
        identity_icon_pattern = LocationBar.IDENTITY_ICON
        page_action_pattern = LocationBar.PAGE_ACTION_BUTTON
        return RegionUtils.create_region_from_patterns(
            left=page_action_pattern, right=identity_icon_pattern
        )
    except FindError:
        raise APIHelperError("Could not create region for awesome bar.")


def create_region_for_hamburger_menu():
    """Create region for hamburger menu pop up."""

    hamburger_menu_pattern = NavBar.HAMBURGER_MENU
    region = Screen.UPPER_RIGHT_CORNER
    try:
        region.wait(hamburger_menu_pattern, 5)
        region.click(hamburger_menu_pattern)
        sign_in_to_firefox_pattern = Pattern("sign_in_to_firefox.png")
        region.wait(sign_in_to_firefox_pattern, 10)
        if OSHelper.is_linux():
            quit_menu_pattern = Pattern("quit.png")
            wait(quit_menu_pattern, 5)
            return RegionUtils.create_region_from_patterns(
                None,
                sign_in_to_firefox_pattern,
                quit_menu_pattern,
                None,
                padding_right=20,
            )
        elif OSHelper.is_mac():
            help_menu_pattern = Pattern("help.png")
            wait(help_menu_pattern, 5)
            return RegionUtils.create_region_from_patterns(
                None,
                sign_in_to_firefox_pattern,
                help_menu_pattern,
                None,
                padding_right=20,
            )
        else:
            exit_menu_pattern = Pattern("exit.png")
            wait(exit_menu_pattern, 5)
            return RegionUtils.create_region_from_patterns(
                None,
                sign_in_to_firefox_pattern,
                exit_menu_pattern,
                None,
                padding_right=20,
            )
    except (FindError, ValueError):
        raise APIHelperError(
            "Can't create a region for the hamburger menu, aborting test."
        )


def create_region_for_url_bar():
    """Create region for the right side of the url bar."""

    try:
        hamburger_menu_pattern = NavBar.HAMBURGER_MENU
        show_history_pattern = LocationBar.HISTORY_DROPMARKER
        select_location_bar()
        return RegionUtils.create_region_from_patterns(
            show_history_pattern,
            hamburger_menu_pattern,
            padding_top=20,
            padding_bottom=20,
        )
    except FindError:
        raise APIHelperError("Could not create region for URL bar.")


def find_window_controls(window_type):
    """Find window controls for main and auxiliary windows.

    :param window_type: Controls for a specific window type.
    :return: None.
    """
    if window_type == "auxiliary":
        Mouse().move(Location(1, 300))
        if OSHelper.is_mac():
            try:
                wait(AuxiliaryWindow.RED_BUTTON_PATTERN.similar(0.9), 5)
                logger.debug("Auxiliary window control found.")
            except FindError:
                raise APIHelperError(
                    "Can't find the auxiliary window controls, aborting."
                )
        else:
            if OSHelper.is_linux():
                Mouse().move(Location(80, 0))
            try:
                wait(AuxiliaryWindow.CLOSE_BUTTON, 5)
                logger.debug("Auxiliary window control found.")
            except FindError:
                raise APIHelperError(
                    "Can't find the auxiliary window controls, aborting."
                )

    elif window_type == "main":
        if OSHelper.is_mac():
            try:
                wait(MainWindow.MAIN_WINDOW_CONTROLS.similar(0.9), 5)
                logger.debug("Main window controls found.")
            except FindError:
                raise APIHelperError("Can't find the Main window controls, aborting.")
        else:
            try:
                if OSHelper.is_linux():
                    reset_mouse()
                wait(MainWindow.CLOSE_BUTTON, 5)
                logger.debug("Main window control found.")
            except FindError:
                raise APIHelperError("Can't find the Main window controls, aborting.")
    else:
        raise APIHelperError("Window Type not supported.")


def full_screen_control(window_type):
    """Click on full screen window mode (Applicable only for MAC system).

    :param window_type: Type of window that need to be maximized in full screen mode.
    :reurn: None.
    """
    if OSHelper.is_mac():
        find_window_controls(window_type)

        if window_type == "auxiliary":
            width, height = AuxiliaryWindow.AUXILIARY_WINDOW_CONTROLS.get_size()
            click(
                AuxiliaryWindow.AUXILIARY_WINDOW_CONTROLS.target_offset(
                    width - 10, height / 2
                ),
                align=Alignment.TOP_LEFT,
            )
        else:
            width, height = MainWindow.MAIN_WINDOW_CONTROLS.get_size()
            click(
                MainWindow.MAIN_WINDOW_CONTROLS.target_offset(width - 10, height / 2),
                align=Alignment.TOP_LEFT,
            )
    else:
        raise APIHelperError("Full screen mode applicable only for MAC")


def get_firefox_build_id_from_about_config():
    """Returns the Firefox build id from 'about:config' page."""
    pref_1 = "browser.startup.homepage_override.buildID"
    pref_2 = "extensions.lastAppBuildId"

    try:
        return get_pref_value(pref_1)
    except APIHelperError:
        try:
            return get_pref_value(pref_2)
        except APIHelperError:
            raise APIHelperError(
                "Could not retrieve firefox build id information from about:config page."
            )


def get_firefox_channel_from_about_config():
    """Returns the Firefox channel from 'about:config' page."""
    try:
        return get_pref_value("app.update.channel")
    except APIHelperError:
        raise APIHelperError(
            "Could not retrieve firefox channel information from about:config page."
        )


def get_firefox_locale_from_about_config():
    """Returns the Firefox locale from 'about:config' page."""
    try:
        value_str = get_pref_value(
            "browser.newtabpage.activity-stream.feeds.section.topstories.options"
        )
        logger.debug(value_str)
        temp = json.loads(value_str)
        return str(temp["stories_endpoint"]).split("&locale_lang=")[1].split("&")[0]
    except (APIHelperError, KeyError):
        raise APIHelperError("Pref format to determine locale has changed.")


def get_firefox_version_from_about_config():
    """Returns the Firefox version from 'about:config' page."""

    try:
        return get_pref_value("extensions.lastAppVersion")
    except APIHelperError:
        raise APIHelperError(
            "Could not retrieve firefox version information from about:config page."
        )


def get_pref_value(pref_name):
    """Returns the value of a provided preference from 'about:config' page.

    :param pref_name: Preference's name.
    :return: Preference's value.
    """

    new_tab()
    select_location_bar()
    paste("about:config")
    type(Key.ENTER)
    time.sleep(Settings.DEFAULT_UI_DELAY)

    type(Key.SPACE)
    time.sleep(Settings.DEFAULT_UI_DELAY)

    paste(pref_name)
    time.sleep(Settings.DEFAULT_UI_DELAY_LONG)
    type(Key.TAB)
    time.sleep(Settings.DEFAULT_UI_DELAY_LONG)

    try:
        value = copy_to_clipboard().split("\t")[1]
    except Exception as e:
        raise APIHelperError("Failed to retrieve preference value.\n{}".format(e))

    close_tab()
    return value


def get_support_info():
    """Returns support information as a JSON object from 'about:support' page."""
    copy_raw_data_to_clipboard = Pattern("about_support_copy_raw_data_button.png")

    new_tab()
    select_location_bar()
    paste("about:support")
    type(Key.ENTER)
    time.sleep(Settings.DEFAULT_UI_DELAY)

    try:
        click(copy_raw_data_to_clipboard)
        time.sleep(Settings.DEFAULT_UI_DELAY_LONG)
        json_text = get_clipboard()
        return json.loads(json_text)
    except Exception as e:
        raise APIHelperError(
            "Failed to retrieve support information value.\n{}".format(e)
        )
    finally:
        close_tab()


def get_telemetry_info():
    """Returns telemetry information as a JSON object from 'about:telemetry'
    page.
    """

    copy_raw_data_to_clipboard_pattern = Pattern("copy_raw_data_to_clipboard.png")
    raw_json_pattern = Pattern("raw_json.png")
    raw_data_pattern = Pattern("raw_data.png")

    new_tab()

    paste("about:telemetry")
    type(Key.ENTER)

    try:
        wait(raw_json_pattern, 10)
        logger.debug("'RAW JSON' button is present on the page.")
        click(raw_json_pattern)
    except (FindError, ValueError):
        raise APIHelperError("'RAW JSON' button not present in the page.")

    try:
        wait(raw_data_pattern, 10)
        logger.debug("'Raw Data' button is present on the page.")
        click(raw_data_pattern)
    except (FindError, ValueError):
        close_tab()
        raise APIHelperError("'Raw Data' button not present in the page.")

    try:
        click(copy_raw_data_to_clipboard_pattern)
        time.sleep(Settings.DEFAULT_UI_DELAY)
        json_text = get_clipboard()
        return json.loads(json_text)
    except Exception:
        raise APIHelperError("Failed to retrieve raw message information value.")
    finally:
        close_tab()


def key_to_one_off_search(highlighted_pattern, direction="left"):
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
            if direction == "right":
                type(Key.RIGHT)
            else:
                type(Key.LEFT)
            max_attempts -= 1


def minimize_window_control(window_type):
    """Click on minimize window control.

    :param window_type: Type of window that need to be minimized.
    :return: None.
    """
    find_window_controls(window_type)

    if window_type == "auxiliary":
        if OSHelper.is_mac():
            width, height = AuxiliaryWindow.AUXILIARY_WINDOW_CONTROLS.get_size()
            click(
                AuxiliaryWindow.AUXILIARY_WINDOW_CONTROLS.target_offset(
                    width / 2, height / 2
                ),
                align=Alignment.TOP_LEFT,
            )
        else:
            click(AuxiliaryWindow.MINIMIZE_BUTTON)
    else:
        if OSHelper.is_mac():
            width, height = MainWindow.MAIN_WINDOW_CONTROLS.get_size()
            click(
                MainWindow.MAIN_WINDOW_CONTROLS.target_offset(width / 2, height / 2),
                align=Alignment.TOP_LEFT,
            )
        else:
            click(MainWindow.MINIMIZE_BUTTON)


def maximize_window_control(window_type):
    """Click on maximize window control.

    :param window_type: Type of window that need to be maximized.
    :return: None.
    """
    find_window_controls(window_type)

    if window_type == "auxiliary":
        if OSHelper.is_mac():
            key_down(Key.ALT)
            width, height = AuxiliaryWindow.AUXILIARY_WINDOW_CONTROLS.get_size()
            click(
                AuxiliaryWindow.AUXILIARY_WINDOW_CONTROLS.target_offset(
                    width - 10, height / 2
                ),
                align=Alignment.TOP_LEFT,
            )
            key_up(Key.ALT)
        else:
            click(AuxiliaryWindow.MAXIMIZE_BUTTON)
            if OSHelper.is_linux():
                reset_mouse()
    else:
        if OSHelper.is_mac():
            key_down(Key.ALT)
            width, height = MainWindow.MAIN_WINDOW_CONTROLS.get_size()
            click(
                MainWindow.MAIN_WINDOW_CONTROLS.target_offset(width - 10, height / 2),
                align=Alignment.TOP_LEFT,
            )
            key_up(Key.ALT)
        else:
            click(MainWindow.MAXIMIZE_BUTTON)


def navigate(url):
    """Navigates, via the location bar, to a given URL.

    :param url: The string to type into the location bar.
    :return: None.
    """
    try:
        select_location_bar()
        paste(url)
        time.sleep(Settings.DEFAULT_UI_DELAY_SHORT)
        type(Key.ENTER)
    except Exception:
        raise APIHelperError("No active window found, cannot navigate to page.")


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
        if args.locale != "ar":
            type(Key.LEFT)
        else:
            type(Key.RIGHT)
        type(Key.ENTER)
        type(Key.UP)
        type(Key.ENTER)

    else:
        type(Key.F10)
        time.sleep(Settings.DEFAULT_UI_DELAY_SHORT)
        if args.locale != "ar":
            type(Key.LEFT)
        else:
            type(Key.RIGHT)
        type(Key.UP)
        type(Key.ENTER)


def open_bookmarks_toolbar():
    """ Open the Bookmarks Toolbar using the context menu from the navigation bar """

    home_button = NavBar.HOME_BUTTON
    w, h = home_button.get_size()
    horizontal_offset = w * 1.7
    navbar_context_menu = home_button.target_offset(horizontal_offset, 0)

    try:
        right_click(navbar_context_menu)
        click(NavBar.ContextMenu.BOOKMARKS_TOOLBAR)
        logger.debug(
            "Click is performed successfully on Bookmarks Toolbar option from navigation bar context menu."
        )
    except FindError:
        raise APIHelperError(
            "Could not open the Bookmarks Toolbar using context menu from the navigation bar."
        )

    restore_firefox_focus()


def open_directory(directory):
    if OSHelper.is_windows():
        os.startfile(directory)
    elif OSHelper.is_linux():
        os.system('xdg-open "' + directory + '"')
    else:
        os.system('open "' + directory + '"')


def open_library_menu(option):
    """Open the Library menu with an option as argument.

    :param option: Library menu option.
    :return: Custom region created for a more efficient and accurate image
    pattern search.
    """

    library_menu_pattern = NavBar.LIBRARY_MENU

    if OSHelper.is_windows():
        value = 5
    else:
        value = 4

    try:
        wait(library_menu_pattern, 10)
        region = Region(
            image_find(library_menu_pattern).x - Screen().width / value,
            image_find(library_menu_pattern).y,
            Screen().width / value,
            Screen().height / value,
        )
        logger.debug("Library menu found.")
    except FindError:
        raise APIHelperError("Can't find the library menu in the page, aborting test.")
    else:
        time.sleep(Settings.DEFAULT_UI_DELAY_LONG)
        click(library_menu_pattern)
        time.sleep(Settings.DEFAULT_UI_DELAY_SHORT)
        try:
            time.sleep(Settings.DEFAULT_UI_DELAY_SHORT)
            region.wait(option, 10)
            logger.debug("Option found.")
            region.click(option)
            return region
        except FindError:
            raise APIHelperError("Can't find the option in the page, aborting test.")


def open_zoom_menu():
    """Open the 'Zoom' menu from the 'View' menu."""

    if OSHelper.is_mac():
        view_menu_pattern = Pattern("view_menu.png")

        click(view_menu_pattern)

        repeat_key_down(3)
        type(text=Key.ENTER)
    else:
        type(text="v", modifier=KeyModifier.ALT)

        repeat_key_down(2)
        type(text=Key.ENTER)


def remove_zoom_indicator_from_toolbar():
    """Remove the zoom indicator from toolbar by clicking on the 'Remove from
    Toolbar' button.
    """

    zoom_control_toolbar_decrease_pattern = NavBar.ZOOM_OUT
    remove_from_toolbar_pattern = Pattern("remove_from_toolbar.png")

    try:
        wait(zoom_control_toolbar_decrease_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        logger.debug("'Decrease' zoom control found.")
        right_click(zoom_control_toolbar_decrease_pattern)
    except FindError:
        raise APIHelperError(
            "Can't find the 'Decrease' zoom control button in the page, \
            aborting."
        )

    try:
        wait(remove_from_toolbar_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        logger.debug("'Remove from Toolbar' option found.")
        click(remove_from_toolbar_pattern)
    except FindError:
        raise APIHelperError(
            "Can't find the 'Remove from Toolbar' option in the page, \
            aborting."
        )

    try:
        wait_vanish(
            zoom_control_toolbar_decrease_pattern, FirefoxSettings.FIREFOX_TIMEOUT
        )
    except FindError:
        raise APIHelperError("Zoom indicator not removed from toolbar, aborting.")


def repeat_key_down(num):
    """Repeat DOWN keystroke a given number of times.

    :param num: Number of times to repeat DOWN key stroke.
    :return: None.
    """
    for i in range(num):
        type(Key.DOWN)
        time.sleep(Settings.DEFAULT_UI_DELAY_SHORT)


def repeat_key_down_until_image_found(
    image_pattern, num_of_key_down_presses=10, delay_between_presses=1
):
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
        time.sleep(1)


def repeat_key_up_until_image_found(
    image_pattern, num_of_key_up_presses=10, delay_between_presses=1
):
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


def reset_mouse():
    """Reset mouse position to location (0, 0)."""
    Mouse().move(Location(0, 0))


def restore_firefox_focus():
    """Restore Firefox focus by clicking the panel near HOME or REFRESH button."""

    try:
        if exists(NavBar.HOME_BUTTON, Settings.DEFAULT_UI_DELAY):
            target_pattern = NavBar.HOME_BUTTON
        else:
            target_pattern = NavBar.RELOAD_BUTTON
        w, h = target_pattern.get_size()
        horizontal_offset = w * 1.7
        click_area = target_pattern.target_offset(horizontal_offset, 0)
        click(click_area)
    except FindError:
        raise APIHelperError("Could not restore firefox focus.")


def restore_window_control(window_type):
    """Click on restore window control.

    :param window_type: Type of window that need to be restored.
    :return: None.
    """
    find_window_controls(window_type)

    if window_type == "auxiliary":
        if OSHelper.is_mac():
            key_down(Key.ALT)
            width, height = AuxiliaryWindow.AUXILIARY_WINDOW_CONTROLS.get_size()
            click(
                AuxiliaryWindow.AUXILIARY_WINDOW_CONTROLS.target_offset(
                    width - 10, height / 2
                ),
                align=Alignment.TOP_LEFT,
            )
            key_up(Key.ALT)
        else:
            if OSHelper.is_linux():
                reset_mouse()
            click(AuxiliaryWindow.ZOOM_RESTORE_BUTTON)
    else:
        if OSHelper.is_mac():
            key_down(Key.ALT)
            width, height = MainWindow.MAIN_WINDOW_CONTROLS.get_size()
            click(
                MainWindow.MAIN_WINDOW_CONTROLS.target_offset(width - 10, height / 2),
                align=Alignment.TOP_LEFT,
            )
            key_up(Key.ALT)
        else:
            if OSHelper.is_linux():
                reset_mouse()
            click(MainWindow.RESIZE_BUTTON)


def restore_window_from_taskbar(option=None):
    """Restore firefox from task bar."""
    if OSHelper.is_mac():
        try:
            click(Pattern("main_menu_window.png"))
            if option == "browser_console":
                click(Pattern("window_browser_console.png"))
            else:
                click(Pattern("window_firefox.png"))
        except FindError:
            raise APIHelperError("Restore window from taskbar unsuccessful.")
    elif OSHelper.get_os_version() == "win7":
        try:
            click(Pattern("firefox_start_bar.png"))
            if option == "library_menu":
                click(Pattern("firefox_start_bar_library.png"))
            if option == "browser_console":
                click(Pattern("firefox_start_bar_browser_console.png"))
        except FindError:
            raise APIHelperError("Restore window from taskbar unsuccessful.")

    else:
        type(text=Key.TAB, modifier=KeyModifier.ALT)
        if OSHelper.is_linux():
            Mouse().move(Location(0, 50))
    time.sleep(Settings.DEFAULT_UI_DELAY)


def right_click_and_type(target, delay=None, keyboard_action=None):
    right_click(target)
    if delay:
        time.sleep(delay)
    else:
        time.sleep(Settings.DEFAULT_UI_DELAY_LONG)
    type(text=keyboard_action)


def scroll_until_pattern_found(
    image_pattern: Pattern,
    scroll_function,
    scroll_params: tuple = tuple(),
    num_of_scroll_iterations: int = 10,
    timeout: float = Settings.auto_wait_timeout,
):
    """
    Scrolls until specified image pattern is found.

    :param image_pattern: Image Pattern to search.
    :param scroll_function: Scrolling function or any callable object (e.g. type, scroll, etc.)
    :param scroll_params: Tuple of params to pass in the scroll_function
            (e.g. (Key.UP, ) or (Key.UP, KeyModifier.CTRL) for the type function).
            NOTE: Tuple should contains from 0 (empty tuple) to 2 items.
    :param num_of_scroll_iterations: Number of scrolling iterations.
    :param timeout: Number of seconds passed to the 'timeout' param of the 'exist' function.
    :return: Boolean. True if image pattern found during scrolling, False otherwise
    """

    scroll_arg = None
    scroll_modifier = None

    if not isinstance(image_pattern, Pattern):
        raise ValueError(INVALID_GENERIC_INPUT)

    if not callable(scroll_function):
        raise ValueError(INVALID_GENERIC_INPUT)

    if not isinstance(scroll_params, tuple):
        raise ValueError(INVALID_GENERIC_INPUT)

    if len(scroll_params) == 2:
        scroll_arg, scroll_modifier = scroll_params
    elif len(scroll_params) == 1:
        scroll_arg, = scroll_params
    elif len(scroll_params) == 0:
        pass
    else:
        raise ValueError(INVALID_GENERIC_INPUT)

    pattern_found = False

    for _ in range(num_of_scroll_iterations):
        pattern_found = exists(image_pattern, timeout)

        if pattern_found:
            break

        if scroll_modifier is None and scroll_arg is None:
            scroll_function()
        elif scroll_modifier is None:
            scroll_function(scroll_arg)
        else:
            scroll_function(scroll_arg, scroll_modifier)

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


def select_zoom_menu_option(option_number):
    """Open the 'Zoom' menu from the 'View' menu and select option."""

    open_zoom_menu()

    repeat_key_down(option_number)
    type(text=Key.ENTER)


def zoom_with_mouse_wheel(nr_of_times=1, zoom_type=None):
    """Zoom in/Zoom out using the mouse wheel.

    :param nr_of_times: Number of times the 'zoom in'/'zoom out' action should
    take place.
    :param zoom_type: Type of the zoom action('zoom in'/'zoom out') intended to
    be performed.
    :return: None.
    """

    # MAC needs doubled number of mouse wheels to zoom in correctly.
    if OSHelper.is_mac():
        nr_of_times *= 2

    # Move focus in the middle of the page to be able to use the scroll.

    Mouse().move(Location(Screen.SCREEN_WIDTH // 4, Screen.SCREEN_HEIGHT // 2))

    for i in range(nr_of_times):
        if OSHelper.is_mac():
            key_down("command")

        else:
            key_down("ctrl")

        Mouse().scroll(dy=zoom_type, dx=0)
        if OSHelper.is_mac():
            key_up("command")

        else:
            key_up("ctrl")

        time.sleep(Settings.DEFAULT_UI_DELAY)
    Mouse().move(Location(0, 0))


class Option(object):
    """Class with zoom members."""

    ZOOM_IN = 0
    ZOOM_OUT = 1
    RESET = 2
    ZOOM_TEXT_ONLY = 3


class RightClickLocationBar:
    """Class with location bar members."""

    UNDO = 0
    CUT = 1
    COPY = 2
    PASTE = 3
    PASTE_GO = 4
    DELETE = 5
    SELECT_ALL = 6


class ZoomType(object):
    """Class with zoom type members."""

    IN = 300 if OSHelper.is_windows() else 1
    OUT = -300 if OSHelper.is_windows() else -1


def find_in_region_from_pattern(
    outer_pattern: Pattern,
    inner_pattern: Pattern,
    outer_pattern_timeout=Settings.auto_wait_timeout,
    inner_pattern_timeout=Settings.auto_wait_timeout,
):
    """ Finds pattern in region created from another pattern
    :param outer_pattern: Pattern for region creation
    :param inner_pattern: Pattern to find in region
    :param outer_pattern_timeout: Time to finding outer_pattern
    :param inner_pattern_timeout: Time to finding inner_pattern,
    :return: Boolean. True if inner_pattern found in outer_pattern region
    :raises: ValueError and APIHelperError
    """
    if not isinstance(outer_pattern, Pattern) or not isinstance(inner_pattern, Pattern):
        raise ValueError(INVALID_GENERIC_INPUT)

    try:
        wait(outer_pattern, outer_pattern_timeout)
        logger.debug("Outer pattern found.")

    except FindError:
        raise APIHelperError("Can't find the outer pattern.")

    width, height = outer_pattern.get_size()
    region = Region(
        image_find(outer_pattern).x, image_find(outer_pattern).y, width, height
    )

    pattern_found = exists(inner_pattern, inner_pattern_timeout, region=region)

    return pattern_found

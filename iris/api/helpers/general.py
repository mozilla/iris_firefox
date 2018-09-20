# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import json

import mozversion

from iris.api.core.environment import Env
from iris.api.core.firefox_ui.menus import LibraryMenu
from iris.api.core.firefox_ui.toolbars import NavBar
from iris.api.core.key import *
from iris.api.core.region import *
from iris.api.core.screen import get_screen
from iris.configuration.config_parser import *
from keyboard_shortcuts import *

logger = logging.getLogger(__name__)


def launch_firefox(path, profile=None, url=None, args=None):
    """Launch the app with optional args for profile, windows, URI, etc."""
    if args is None:
        args = []

    if profile is None:
        logger.error('No profile name present, aborting run.')
        raise ValueError

    cmd = [path, '-foreground', '-no-remote', '-profile', profile]

    # Add other Firefox flags
    for arg in args:
        cmd.append(arg)

    if url is not None:
        cmd.append('-new-tab')
        cmd.append(url)

    logger.debug('Launching Firefox with arguments: %s' % ' '.join(cmd))
    subprocess.Popen(cmd)
    return cmd


def confirm_firefox_launch(app):
    """waits for firefox to exist by waiting for the home button to be present."""
    try:
        wait(Pattern('iris_logo.png'), 20)
    except Exception as err:
        logger.error(err)
        logger.error('Can\'t launch Firefox - aborting test run.')
        app.finish(code=1)


def confirm_firefox_quit(app):
    try:
        wait_vanish(NavBar.HOME_BUTTON, 10)
        address_crash_reporter()
    except FindError:
        logger.error('Firefox still around - aborting test run.')
        app.finish(code=1)


def get_firefox_region():
    # TODO: needs better logic to determine bounds
    # For now, just return the whole screen
    return get_screen()


def navigate_slow(url):
    """Navigates, via the location bar, to a given URL

    :param url: the string to type into the location bar.

    The function handles typing 'Enter' to complete the action.
    """

    try:
        select_location_bar()
        # increase the delay between each keystroke while typing strings
        # (sikuli defaults to .02 sec)
        Settings.type_delay = 0.1
        type(url + Key.ENTER)
    except Exception:
        raise APIHelperError('No active window found, cannot navigate to page')


def navigate(url):
    try:
        select_location_bar()
        paste(url)
        type(Key.ENTER)
    except Exception:
        raise APIHelperError('No active window found, cannot navigate to page')


def restart_firefox(path, profile, url, args=None):
    # Just as it says, with options.
    logger.debug('Restarting Firefox.')
    quit_firefox()
    logger.debug('Confirming that Firefox has been quit.')
    home_pattern = NavBar.HOME_BUTTON
    try:
        wait_vanish(home_pattern, 10)
        # TODO: This should be made into a robust function instead of a hard coded sleep
        # Give Firefox a chance to cleanly shutdown all of its processes
        time.sleep(Settings.SYSTEM_DELAY)
        logger.debug('Relaunching Firefox with profile name \'%s\'' % profile)
        launch_firefox(path, profile, url, args)
        logger.debug('Confirming that Firefox has been relaunched')
        if exists(home_pattern, 20):
            logger.debug('Successful Firefox restart performed')
        else:
            raise APIHelperError('Firefox not relaunched.')
    except FindError:
        raise APIHelperError('Firefox still around - cannot restart.')


def get_menu_modifier():
    if Settings.get_os() == Platform.MAC:
        menu_modifier = Key.CTRL
    else:
        menu_modifier = Key.CMD
    return menu_modifier


def get_main_modifier():
    if Settings.get_os() == Platform.MAC:
        main_modifier = Key.CMD
    else:
        main_modifier = Key.CTRL
    return main_modifier


def copy_to_clipboard():
    edit_select_all()
    edit_copy()
    value = Env.get_clipboard().strip()
    logger.debug("Copied to clipboard: %s" % value)
    return value


def change_preference(pref_name, value):
    try:
        new_tab()
        select_location_bar()
        paste('about:config')
        type(Key.ENTER)
        time.sleep(Settings.UI_DELAY)

        type(Key.SPACE)
        time.sleep(Settings.UI_DELAY)

        paste(pref_name)
        time.sleep(Settings.UI_DELAY_LONG)
        type(Key.TAB)
        time.sleep(Settings.UI_DELAY_LONG)

        try:
            retrieved_value = copy_to_clipboard().split(';'[0])[1]
        except Exception as e:
            raise APIHelperError('Failed to retrieve preference value. %s' % e.message)

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
        raise APIHelperError('Could not set value: %s to preference: %s' % (value, pref_name))


def reset_mouse():
    hover(Location(0, 0))


def login_site(site_name):
    username = get_config_property(site_name, 'username')
    password = get_config_property(site_name, 'password')
    paste(username)
    focus_next_item()
    paste(password)
    focus_next_item()
    type(Key.ENTER)


def dont_save_password():
    if exists(Pattern('dont_save_password_button.png'), 10):
        click(Pattern('dont_save_password_button.png'))
    else:
        raise APIHelperError('Unable to find dont_save_password_button.png')


def click_hamburger_menu_option(option):
    hamburger_menu_pattern = NavBar.HAMBURGER_MENU
    try:
        wait(hamburger_menu_pattern, 10)
        region = create_region_from_image(hamburger_menu_pattern)
        logger.debug('hamburger menu found')
    except FindError:
        raise APIHelperError('Can\'t find the "hamburger menu" in the page, aborting test.')
    else:
        click(hamburger_menu_pattern)
        time.sleep(Settings.UI_DELAY)
        try:
            region.wait(option, 10)
            logger.debug('Option found')
        except FindError:
            raise APIHelperError('Can\'t find the option in the page, aborting test.')
        else:
            region.click(option)
            return region


def confirm_close_multiple_tabs():
    """Click confirm 'Close all tabs' for warning popup when multiple tabs are opened"""
    close_all_tabs_button_pattern = Pattern('close_all_tabs_button.png')

    try:
        wait(close_all_tabs_button_pattern, 5)
        logger.debug('"Close all tabs" warning popup found.')
        type(Key.ENTER)
    except FindError:
        logger.debug('Couldn\'t find the "Close all tabs" warning popup.')
        pass


def click_auxiliary_window_control(button):
    """Click auxiliary window with options: close, minimize, maximize, full_screen, zoom_restore."""
    close_button_pattern = Pattern('auxiliary_window_close_button.png')
    zoom_full_button_pattern = Pattern('auxiliary_window_maximize.png')
    zoom_restore_button_pattern = Pattern('minimize_full_screen_auxiliary_window.png')
    minimize_button_pattern = Pattern('auxiliary_window_minimize.png')
    auxiliary_window_controls_pattern = Pattern('auxiliary_window_controls.png')
    if Settings.get_os() == Platform.MAC:
        red_button_pattern = Pattern('unhovered_red_control.png').similar(0.9)
        hovered_red_button = Pattern('hovered_red_button.png')

    # Help ensure mouse is not over controls by moving the cursor to the left of the screen.
    hover(Location(1, 300))

    if Settings.get_os() == Platform.MAC:
        try:
            wait(red_button_pattern, 5)
            logger.debug('Auxiliary window control found.')
        except FindError:
            raise APIHelperError('Can\'t find the auxiliary window controls, aborting.')
    else:
        if Settings.get_os() == Platform.LINUX:
            hover(Location(80, 0))
        try:
            wait(close_button_pattern, 5)
            logger.debug('Auxiliary window control found.')
        except FindError:
            raise APIHelperError('Can\'t find the auxiliary window controls, aborting.')

    if button == 'close':
        if Settings.get_os() == Platform.MAC:
            hover(red_button_pattern, 0.3)
            click(hovered_red_button)
        else:
            click(close_button_pattern)
    elif button == 'minimize':
        if Settings.get_os() == Platform.MAC:
            window_controls_pattern = auxiliary_window_controls_pattern
            width, height = get_image_size(window_controls_pattern)
            click(window_controls_pattern.target_offset(width / 2, height / 2))
        else:
            click(minimize_button_pattern)
    elif button == 'full_screen':
        window_controls_pattern = auxiliary_window_controls_pattern
        width, height = get_image_size(window_controls_pattern)
        click(window_controls_pattern.target_offset(width - 10, height / 2))
        if Settings.get_os() == Platform.LINUX:
            hover(Location(80, 0))
    elif button == 'maximize':
        if Settings.get_os() == Platform.MAC:
            key_down(Key.ALT)
            window_controls_pattern = auxiliary_window_controls_pattern
            width, height = get_image_size(window_controls_pattern)
            click(window_controls_pattern.target_offset(width - 10, height / 2))
            key_up(Key.ALT)
        else:
            click(zoom_full_button_pattern)
            if Settings.get_os() == Platform.LINUX:
                hover(Location(80, 0))
    elif button == 'zoom_restore':
        if Settings.get_os() == Platform.MAC:
            reset_mouse()
            hover(red_button_pattern)
        click(zoom_restore_button_pattern)


def click_cancel_button():
    cancel_button_pattern = Pattern('cancel_button.png')
    try:
        wait(cancel_button_pattern, 10)
        logger.debug('Cancel button found')
    except FindError:
        raise APIHelperError('Can\'t find the cancel button, aborting.')
    else:
        click(cancel_button_pattern)


def close_customize_page():
    customize_done_button_pattern = Pattern('customize_done_button.png')
    try:
        wait(customize_done_button_pattern, 10)
        logger.debug('Done button found')
    except FindError:
        raise APIHelperError('Can\'t find the Done button in the page, aborting.')
    else:
        click(customize_done_button_pattern)


def address_crash_reporter():
    # TODO: Only works on Mac and Windows until we can get Linux images
    reporter_pattern = Pattern('crash_sorry.png')
    if exists(reporter_pattern, 2):
        logger.debug('Crash Reporter found!')
        # Let crash stats know this is an Iris automation crash.
        click(reporter_pattern)
        # TODO: Add additional info in this message to crash stats
        type('Iris automation test crash')
        # Then dismiss the dialog by choosing to quit Firefox
        click(Pattern('quit_firefox_button.png'))

        # Ensure the reporter closes before moving on
        try:
            wait_vanish(reporter_pattern, 20)
            logger.debug('Crash report sent')
        except FindError:
            logger.error('Crash reporter did not close')
            # Close the reporter if it hasn't gone away in time
            click_auxiliary_window_control('close')
        else:
            return
    else:
        # If no crash reporter, silently move on to the next test case
        return


def open_about_firefox():
    if Settings.get_os() == Platform.MAC:
        # Key stroke into Firefox Menu to get to About Firefox.
        type(Key.F3, modifier=KeyModifier.CTRL)
        type(Key.F2, modifier=KeyModifier.CTRL)

        time.sleep(0.5)
        type(Key.RIGHT)
        type(Key.DOWN)
        type(Key.DOWN)
        type(Key.ENTER)

    elif Settings.get_os() == Platform.WINDOWS:
        # Use Help menu keyboard shortcuts to open About Firefox
        key_down(Key.ALT)
        type('h')
        time.sleep(0.5)
        type('a')
        key_up(Key.ALT)

    else:
        # Use Help menu keyboard shortcuts to open About Firefox
        key_down(Key.ALT)
        type('h')
        time.sleep(1)
        key_up(Key.ALT)
        type('a')


class Option(object):
    ZOOM_IN = 0
    ZOOM_OUT = 1
    RESET = 2
    ZOOM_TEXT_ONLY = 3


def open_zoom_menu():
    """Open the Zoom menu from the View Menu."""

    view_menu_pattern = Pattern('view_menu.png')
    if Settings.get_os() == Platform.MAC:
        click(view_menu_pattern)
        for i in range(3):
            type(text=Key.DOWN)
        type(text=Key.ENTER)
    else:
        type(text='v', modifier=KeyModifier.ALT)
        for i in range(2):
            type(text=Key.DOWN)
        type(text=Key.ENTER)


def select_zoom_menu_option(option_number):
    """Open the Zoom menu from the View Menu and select option."""

    open_zoom_menu()

    for i in range(option_number):
        type(text=Key.DOWN)
    type(text=Key.ENTER)


class RightClickLocationBar(object):
    UNDO = 0
    CUT = 1
    COPY = 2
    PASTE = 3
    PASTE_GO = 4
    DELETE = 5
    SELECT_ALL = 6


def select_location_bar_option(option_number):
    """Select option from the location bar menu."""
    if Settings.get_os() == Platform.WINDOWS:
        for i in range(option_number + 1):
            type(text=Key.DOWN)
        type(text=Key.ENTER)
    else:
        for i in range(option_number - 1):
            type(text=Key.DOWN)
        type(text=Key.ENTER)


def create_region_from_image(image):
    try:
        m = find(image)
        if m:
            hamburger_pop_up_menu_weight = 285
            hamburger_pop_up_menu_height = 655
            logger.debug('Creating a region for Hamburger Pop Up Menu')
            region = Region(m.x - hamburger_pop_up_menu_weight, m.y, hamburger_pop_up_menu_weight,
                            hamburger_pop_up_menu_height)
            return region
        else:
            raise APIHelperError('No Matching found')
    except FindError:
        raise APIHelperError('Image not present')


def create_region_for_url_bar():
    hamburger_menu_pattern = NavBar.HAMBURGER_MENU
    show_history_pattern = LocationBar.SHOW_HISTORY_BUTTON
    select_location_bar()
    region = create_region_from_patterns(show_history_pattern, hamburger_menu_pattern,
                                         padding_top=20, padding_bottom=20)
    return region


def create_region_for_hamburger_menu():
    hamburger_menu_pattern = NavBar.HAMBURGER_MENU
    exit_menu_pattern = Pattern('exit.png')
    help_menu_pattern = Pattern('help.png')
    quit_menu_pattern = Pattern('quit.png')
    try:
        wait(hamburger_menu_pattern, 10)
        click(hamburger_menu_pattern)
        time.sleep(1)
        if Settings.get_os() == Platform.LINUX:
            reg = create_region_from_patterns(None, hamburger_menu_pattern, quit_menu_pattern, None, padding_right=20)
        elif Settings.get_os() == Platform.MAC:
            reg = create_region_from_patterns(None, hamburger_menu_pattern, help_menu_pattern, None, padding_right=20)
        else:
            reg = create_region_from_patterns(None, hamburger_menu_pattern, exit_menu_pattern, None, padding_right=20)
    except (FindError, ValueError):
        raise APIHelperError('Can\'t find the hamburger menu in the page, aborting test.')
    return reg


def restore_window_from_taskbar():
    if Settings.get_os() == Platform.MAC:
        try:
            main_menu_window_pattern = Pattern('main_menu_window.png')
            wait(main_menu_window_pattern, 5)
            click(main_menu_window_pattern)
            type(Key.DOWN)
            time.sleep(Settings.FX_DELAY)
            type(Key.ENTER)
        except FindError:
            raise APIHelperError('Restore window from taskbar unsuccessful.')
    else:
        type(text=Key.TAB, modifier=KeyModifier.ALT)
        if Settings.get_os() == Platform.LINUX:
            hover(Location(0, 50))
    time.sleep(Settings.UI_DELAY)


def open_library_menu(option):
    library_menu_pattern = NavBar.LIBRARY_MENU

    try:
        wait(library_menu_pattern, 10)
        region = Region(find(library_menu_pattern).x - SCREEN_WIDTH / 4, find(library_menu_pattern).y, SCREEN_WIDTH / 4,
                        SCREEN_HEIGHT / 4)
        logger.debug('Library menu found')
    except FindError:
        raise APIHelperError('Can\'t find the library menu in the page, aborting test.')
    else:
        time.sleep(Settings.UI_DELAY_LONG)
        click(library_menu_pattern)
        time.sleep(Settings.FX_DELAY)
        try:
            time.sleep(Settings.FX_DELAY)
            region.wait(option, 10)
            logger.debug('Option found')
        except FindError:
            raise APIHelperError('Can\'t find the option in the page, aborting test.')
        else:
            region.click(option)
            return region


def remove_zoom_indicator_from_toolbar():
    zoom_control_toolbar_decrease_pattern = Pattern('zoom_control_toolbar_decrease.png')
    remove_from_toolbar_pattern = Pattern('remove_from_toolbar.png')

    try:
        wait(zoom_control_toolbar_decrease_pattern, 10)
        logger.debug('\'Decrease\' zoom control found.')
        right_click(zoom_control_toolbar_decrease_pattern)
    except FindError:
        raise APIHelperError('Can\'t find the \'Decrease\' zoom control button in the page, aborting.')

    try:
        wait(remove_from_toolbar_pattern, 10)
        logger.debug('\'Remove from Toolbar\' option found.')
        click(remove_from_toolbar_pattern)
    except FindError:
        raise APIHelperError('Can\'t find the \'Remove from Toolbar\' option in the page, aborting.')

    try:
        wait_vanish(zoom_control_toolbar_decrease_pattern, 10)
    except FindError:
        raise APIHelperError('Zoom indicator not removed from toolbar, aborting.')


def bookmark_options(option):
    try:
        wait(option, 10)
        logger.debug('Option %s is present on the page.' % option)
        click(option)
    except FindError:
        raise APIHelperError('Can\'t find option %s, aborting.' % option)


def access_bookmarking_tools(option):
    bookmarking_tools_pattern = LibraryMenu.BookmarksOption.BOOKMARKING_TOOLS
    open_library_menu(LibraryMenu.BOOKMARKS_OPTION)

    try:
        wait(bookmarking_tools_pattern, 10)
        logger.debug('Bookmarking Tools option has been found.')
        click(bookmarking_tools_pattern)
    except FindError:
        raise APIHelperError('Can\'t find the Bookmarking Tools option, aborting.')
    try:
        wait(option, 10)
        logger.debug('%s option has been found.' % option)
        click(option)
    except FindError:
        raise APIHelperError('Can\'t find the %s option, aborting.' % option)


def write_profile_prefs(test_case):
    if len(test_case.prefs):
        pref_file = os.path.join(test_case.profile_path, 'user.js')
        f = open(pref_file, 'w')
        for pref in test_case.prefs:
            name, value = pref.split(';')
            if value == 'true' or value == 'false' or value.isdigit():
                f.write('user_pref("%s", %s);\n' % (name, value))
            else:
                f.write('user_pref("%s", "%s");\n' % (name, value))
        f.close()


def create_firefox_args(test_case):
    args = []
    if test_case.private_browsing:
        args.append('-private')

    if test_case.private_window:
        args.append('-private-window')

    try:
        if test_case.window_size:
            w, h = test_case.window_size.split('x')
            args.append('-width')
            args.append('%s' % w)
            args.append('-height')
            args.append('%s' % h)
            test_case.maximize_window = False
            if int(w) < 600:
                logger.warning('Windows of less than 600 pixels wide may cause Iris to fail.')
    except ValueError:
        raise APIHelperError('Incorrect window size specified. Must specify width and height separated by lowercase x.')

    if test_case.profile_manager:
        args.append('-ProfileManager')

    if test_case.set_default_browser:
        args.append('-setDefaultBrowser')

    if test_case.import_wizard:
        args.append('-migration')

    if test_case.search:
        args.append('-search')
        args.append(test_case.search)

    if test_case.preferences:
        args.append('-preferences')

    if test_case.devtools:
        args.append('-devtools')

    if test_case.js_debugger:
        args.append('-jsdebugger')

    if test_case.js_console:
        args.append('-jsconsole')

    if test_case.safe_mode:
        args.append('-safe-mode')

    return args


class ZoomType(object):
    IN = 300 if Settings.is_windows() else 1
    OUT = -300 if Settings.is_windows() else -1


def zoom_with_mouse_wheel(nr_of_times=1, zoom_type=None):
    """Zoom in/Zoom out using the mouse wheel

    :param nr_of_times: Number of times the 'zoom in'/'zoom out' action should take place
    :param zoom_type: Type of the zoom action('zoom in'/'zoom out') intended to perform
    :return: None
    """

    # move focus in the middle of the page to be able to use the scroll
    pyautogui.moveTo(SCREEN_WIDTH / 4, SCREEN_HEIGHT / 2)

    for i in range(nr_of_times):
        if Settings.get_os() == Platform.MAC:
            pyautogui.keyDown('command')
        else:
            pyautogui.keyDown('ctrl')
        pyautogui.scroll(zoom_type)
        if Settings.get_os() == Platform.MAC:
            pyautogui.keyUp('command')
        else:
            pyautogui.keyUp('ctrl')
        time.sleep(Settings.UI_DELAY)
    pyautogui.moveTo(0, 0)


def wait_for_firefox_restart():
    home_pattern = NavBar.HOME_BUTTON
    try:
        wait_vanish(home_pattern, 10)
        logger.debug('Firefox successfully closed.')
        wait(home_pattern, 20)
        logger.debug('Successful Firefox restart performed.')
    except FindError:
        raise APIHelperError('Firefox restart has not been performed, aborting.')


def restore_firefox_focus():
    w, h = get_image_size(NavBar.HOME_BUTTON)
    horizontal_offset = w * 2
    click_area = NavBar.HOME_BUTTON.target_offset(horizontal_offset, 0)
    click(click_area)


def get_firefox_version_from_about_support():
    return get_pref_value('extensions.lastAppVersion')


def get_firefox_build_id_from_about_support():
    # There are several prefs that may contain this data, but we are not guaranteed
    # to have them, depending on what type of profile we start with.
    pref_1 = 'browser.startup.homepage_override.buildID'
    pref_2 = 'extensions.lastAppBuildId'

    try:
        return get_pref_value(pref_1)
    except APIHelperError:
        return get_pref_value(pref_2)


def get_firefox_channel_from_about_support():
    return get_pref_value('app.update.channel')


def get_firefox_locale_from_about_support():
    value_str = get_pref_value('browser.newtabpage.activity-stream.feeds.section.topstories.options')
    logger.debug(value_str)
    try:
        temp = json.loads(value_str)
        value = str(temp['stories_endpoint']).split('&locale_lang=')[1].split('&')[0]
    except KeyError:
        raise APIHelperError('Pref format to determine locale has changed')
    return value


def get_pref_value(pref_name):
    new_tab()
    select_location_bar()
    paste('about:config')
    type(Key.ENTER)
    time.sleep(Settings.UI_DELAY)

    type(Key.SPACE)
    time.sleep(Settings.UI_DELAY)

    paste(pref_name)
    time.sleep(Settings.UI_DELAY_LONG)
    type(Key.TAB)
    time.sleep(Settings.UI_DELAY_LONG)

    try:
        value = copy_to_clipboard().split(';'[0])[1]
    except Exception as e:
        raise APIHelperError('Failed to retrieve preference value. %s' % e.message)

    close_tab()
    return value


def get_support_info():
    copy_raw_data_to_clipboard = Pattern('about_support_copy_raw_data_button.png')

    new_tab()
    select_location_bar()
    paste('about:support')
    type(Key.ENTER)
    time.sleep(Settings.UI_DELAY)

    try:
        click(copy_raw_data_to_clipboard)
        time.sleep(Settings.UI_DELAY)
        json_text = Env.get_clipboard()
    except Exception as e:
        raise APIHelperError('Failed to retrieve support information value. %s' % e.message)

    close_tab()
    return json.loads(json_text)


def get_firefox_info(build_path):
    """This method returns the application version information as a dict with the help of mozversion module."""
    return mozversion.get_version(binary=build_path)


def get_firefox_version(build_path):
    return get_firefox_info(build_path)['application_version']


def get_firefox_build_id(build_path):
    return get_firefox_info(build_path)['platform_buildid']


def get_firefox_channel(build_path):
    fx_channel = get_firefox_info(build_path)['application_repository']
    if 'beta' in fx_channel:
        return 'beta'
    elif 'release' in fx_channel:
        return 'release'
    elif 'esr' in fx_channel:
        return 'esr'
    else:
        return 'nightly'

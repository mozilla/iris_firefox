# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.api.core.environment import Env
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
    subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return


def confirm_firefox_launch(app):
    """waits for firefox to exist by waiting for the home button to be present."""
    try:
        wait('home.png', 20)
    except Exception as err:
        logger.error(err)
        logger.error('Can\'t launch Firefox - aborting test run.')
        app.finish(code=1)


def confirm_firefox_quit(app):
    try:

        wait_vanish('home.png', 10)
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
    try:
        wait_vanish('home.png', 10)
        # TODO: This should be made into a robust function instead of a hard coded sleep
        # Give Firefox a chance to cleanly shutdown all of its processes
        time.sleep(Settings.SYSTEM_DELAY)
        logger.debug('Relaunching Firefox with profile name \'%s\'' % profile)
        launch_firefox(path, profile, url, args)
        logger.debug('Confirming that Firefox has been relaunched')
        if exists('home.png', 10):
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
            dialog_box = Pattern('preference_dialog_icon.png')
            try:
                wait(dialog_box, 3)
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
    username = get_credential(site_name, 'username')
    password = get_credential(site_name, 'password')
    paste(username)
    focus_next_item()
    paste(password)
    focus_next_item()
    type(Key.ENTER)


def dont_save_password():
    if exists('dont_save_password_button.png', 10):
        click('dont_save_password_button.png')
    else:
        raise APIHelperError('Unable to find dont_save_password_button.png')


def click_hamburger_menu_option(option):
    hamburger_menu = 'hamburger_menu.png'
    try:
        wait(hamburger_menu, 10)
        region = create_region_from_image(hamburger_menu)
        logger.debug('hamburger menu found')
    except FindError:
        raise APIHelperError('Can\'t find the "hamburger menu" in the page, aborting test.')
    else:
        click(hamburger_menu)
        time.sleep(Settings.UI_DELAY)
        try:
            region.wait(option, 10)
            logger.debug('Option found')
        except FindError:
            raise APIHelperError('Can\'t find the option in the page, aborting test.')
        else:
            region.click(option)
            return region


def click_auxiliary_window_control(button):
    """Click auxiliary window with options: close, minimize, maximize, full_screen, zoom_restore."""
    close_button = 'auxiliary_window_close_button.png'
    zoom_full_button = 'auxiliary_window_maximize.png'
    zoom_restore_button = 'minimize_full_screen_auxiliary_window.png'
    red_button = 'unhovered_red_control.png'
    minimize_button = 'auxiliary_window_minimize.png'
    auxiliary_window_controls = 'auxiliary_window_controls.png'

    if Settings.get_os() == Platform.MAC:
        try:
            wait(red_button, 5)
            logger.debug('Auxiliary window control found.')
        except FindError:
            raise APIHelperError('Can\'t find the auxiliary window controls, aborting.')
    else:
        if Settings.get_os() == Platform.LINUX:
            hover(Location(80, 0))
        try:
            wait(close_button, 5)
            logger.debug('Auxiliary window control found.')
        except FindError:
            raise APIHelperError('Can\'t find the auxiliary window controls, aborting.')

    if button == 'close':
        if Settings.get_os() == Platform.MAC:
            click(red_button)
        else:
            click(close_button)
    elif button == 'minimize':
        if Settings.get_os() == Platform.MAC:
            window_controls_pattern = Pattern(auxiliary_window_controls)
            width, height = get_image_size(window_controls_pattern)
            click(window_controls_pattern.target_offset(width / 2, height / 2))
        else:
            click(minimize_button)
    elif button == 'full_screen':
        window_controls_pattern = Pattern(auxiliary_window_controls)
        width, height = get_image_size(window_controls_pattern)
        click(window_controls_pattern.target_offset(width - 10, height / 2))
        if Settings.get_os() == Platform.LINUX:
            hover(Location(80, 0))
    elif button == 'maximize':
        if Settings.get_os() == Platform.MAC:
            key_down(Key.ALT)
            window_controls_pattern = Pattern(auxiliary_window_controls)
            width, height = get_image_size(window_controls_pattern)
            click(window_controls_pattern.target_offset(width - 10, height / 2))
            key_up(Key.ALT)
        else:
            click(zoom_full_button)
            if Settings.get_os() == Platform.LINUX:
                hover(Location(80, 0))
    elif button == 'zoom_restore':
        if Settings.get_os() == Platform.MAC:
            reset_mouse()
            hover(red_button)
        click(zoom_restore_button)


def click_cancel_button():
    try:
        wait('cancel_button.png', 10)
        logger.debug('Cancel button found')
    except FindError:
        raise APIHelperError('Can\'t find the cancel button, aborting.')
    else:
        click('cancel_button.png')


def close_customize_page():
    customize_done_button = 'customize_done_button.png'
    try:
        wait(customize_done_button, 10)
        logger.debug('Done button found')
    except FindError:
        raise APIHelperError('Can\'t find the Done button in the page, aborting.')
    else:
        click(customize_done_button)


def address_crash_reporter():
    # TODO: Only works on Mac and Windows until we can get Linux images
    reporter = 'crash_sorry.png'
    if exists(reporter, 2):
        logger.debug('Crash Reporter found!')
        # Let crash stats know this is an Iris automation crash.
        click(reporter)
        # TODO: Add additional info in this message to crash stats
        type('Iris automation test crash')
        # Then dismiss the dialog by choosing to quit Firefox
        click('quit_firefox_button.png')

        # Ensure the reporter closes before moving on
        try:
            wait_vanish(reporter, 20)
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


def open_zoom_menu(option_number):
    """Opens the Zoom menu options from the View Menu."""

    view_menu = 'view_menu.png'
    if Settings.get_os() == Platform.MAC:
        click(view_menu)
        for i in range(3):
            type(text=Key.DOWN)
        type(text=Key.ENTER)
    else:
        type(text='v', modifier=KeyModifier.ALT)
        for i in range(2):
            type(text=Key.DOWN)
        type(text=Key.ENTER)

    for i in range(option_number):
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
    hamburger_menu = 'hamburger_menu.png'
    show_history = 'show_history.png'
    select_location_bar()
    region = create_region_from_patterns(show_history, hamburger_menu, padding_top=10, padding_bottom=15)
    return region


def create_region_for_hamburger_menu():
    hamburger_menu = 'hamburger_menu.png'
    exit_menu = 'exit.png'
    help_menu = 'help.png'
    quit_menu = 'quit.png'
    try:
        wait(hamburger_menu, 10)
        click(hamburger_menu)
        time.sleep(1)
        if Settings.get_os() == Platform.LINUX:
            region = create_region_from_patterns(None, hamburger_menu, quit_menu, None)
        elif Settings.get_os() == Platform.MAC:
            region = create_region_from_patterns(None, hamburger_menu, help_menu, None)
        else:
            region = create_region_from_patterns(None, hamburger_menu, exit_menu, None)
    except (FindError, ValueError):
        raise APIHelperError('Can\'t find the hamburger menu in the page, aborting test.')
    return region


def restore_window_from_taskbar():
    if Settings.get_os() == Platform.MAC:
        try:
            main_menu_window = 'main_menu_window.png'
            wait(main_menu_window, 5)
            click(main_menu_window)
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
    library_menu = 'library_menu.png'

    try:
        wait(library_menu, 10)
        region = Region(find(library_menu).x - SCREEN_WIDTH / 4, find(library_menu).y, SCREEN_WIDTH / 4,
                        SCREEN_HEIGHT / 4)
        logger.debug('Library menu found')
    except FindError:
        raise APIHelperError('Can\'t find the library menu in the page, aborting test.')
    else:
        time.sleep(Settings.FX_DELAY)
        click(library_menu)
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
    zoom_control_toolbar_decrease = 'zoom_control_toolbar_decrease.png'
    remove_from_toolbar = 'remove_from_toolbar.png'

    try:
        wait(zoom_control_toolbar_decrease, 10)
        logger.debug('\'Decrease\' zoom control found.')
        right_click(zoom_control_toolbar_decrease)
    except FindError:
        raise APIHelperError('Can\'t find the \'Decrease\' zoom control button in the page, aborting.')

    try:
        wait(remove_from_toolbar, 10)
        logger.debug('\'Remove from Toolbar\' option found.')
        click(remove_from_toolbar)
    except FindError:
        raise APIHelperError('Can\'t find the \'Remove from Toolbar\' option in the page, aborting.')

    try:
        wait_vanish(zoom_control_toolbar_decrease, 10)
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
    bookmarking_tools = 'bookmarking_tools.png'
    open_library_menu('bookmarks_menu.png')

    try:
        wait(bookmarking_tools, 10)
        logger.debug('Bookmarking Tools option has been found.')
        click(bookmarking_tools)
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
        file = open(pref_file, 'w')
        for pref in test_case.prefs:
            name, value = pref.split(';')
            if value == 'true' or value == 'false' or value.isdigit():
                file.write('user_pref("%s", %s);\n' % (name, value))
            else:
                file.write('user_pref("%s", "%s");\n' % (name, value))
        file.close()


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

    url_bar_default_zoom_level = 'url_bar_default_zoom_level.png'

    # move focus in the middle of the page to be able to use the scroll
    pyautogui.moveTo(SCREEN_WIDTH / 4, SCREEN_HEIGHT / 2)

    if Settings.getOS() == Platform.LINUX and nr_of_times == 1 and exists(url_bar_default_zoom_level, 10):
        nr_of_times = 2

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
        time.sleep(0.5)
    pyautogui.moveTo(0, 0)

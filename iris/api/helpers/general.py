# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import json

import mozversion
from mozrunner import FirefoxRunner, errors

from iris.api.core.environment import Env
from iris.api.core.firefox_ui.content_blocking import ContentBlocking
from iris.api.core.firefox_ui.library_menu import LibraryMenu
from iris.api.core.firefox_ui.nav_bar import NavBar
from iris.api.core.firefox_ui.window_controls import MainWindow, AuxiliaryWindow
from iris.api.core.key import *
from iris.api.core.region import *
from iris.api.core.screen import Screen
from iris.configuration.config_parser import *
from keyboard_shortcuts import *

logger = logging.getLogger(__name__)


def access_bookmarking_tools(option):
    """Access option from 'Bookmarking Tools'.

    :param option: Option from 'Bookmarking Tools'.
    :return: None.
    """

    bookmarking_tools_pattern = LibraryMenu.BookmarksOption.BOOKMARKING_TOOLS
    open_library_menu(LibraryMenu.BOOKMARKS_OPTION)

    try:
        wait(bookmarking_tools_pattern, 10)
        logger.debug('Bookmarking Tools option has been found.')
        click(bookmarking_tools_pattern)
    except FindError:
        raise APIHelperError(
            'Can\'t find the Bookmarking Tools option, aborting.')
    try:
        wait(option, 15)
        logger.debug('%s option has been found.' % option)
        click(option)
    except FindError:
        raise APIHelperError('Can\'t find the %s option, aborting.' % option)


def bookmark_options(option):
    """Click a bookmark option after right clicking on a bookmark from the
    library menu.

    :param option: Bookmark option to be clicked.
    :return: None.
    """

    try:
        wait(option, 10)
        logger.debug('Option %s is present on the page.' % option)
        click(option)
    except FindError:
        raise APIHelperError('Can\'t find option %s, aborting.' % option)


def change_preference(pref_name, value):
    """Change the value for a specific preference.

    :param pref_name: Preference to be changed.
    :param value: Preference's value after the change.
    :return: None.
    """
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
            raise APIHelperError(
                'Failed to retrieve preference value. %s' % e.message)

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


def click_cancel_button():
    """Click cancel button."""
    cancel_button_pattern = Pattern('cancel_button.png')
    try:
        wait(cancel_button_pattern, 10)
        logger.debug('Cancel button found.')
        click(cancel_button_pattern)
    except FindError:
        raise APIHelperError('Can\'t find the cancel button, aborting.')


def click_hamburger_menu_option(option):
    """Click on a specific option from the hamburger menu.

    :param option: Hamburger menu option to be clicked.
    :return: The region created starting from the hamburger menu pattern.
    """
    hamburger_menu_pattern = NavBar.HAMBURGER_MENU
    try:
        wait(hamburger_menu_pattern, 10)
        region = create_region_from_image(hamburger_menu_pattern)
        logger.debug('Hamburger menu found.')
    except FindError:
        raise APIHelperError(
            'Can\'t find the "hamburger menu" in the page, aborting test.')
    else:
        click(hamburger_menu_pattern)
        time.sleep(Settings.UI_DELAY)
        try:
            region.wait(option, 10)
            logger.debug('Option found.')
            region.click(option)
            return region
        except FindError:
            raise APIHelperError(
                'Can\'t find the option in the page, aborting test.')


def click_window_control(button, window_type='auxiliary'):
    """Click window with options: close, minimize, maximize, restore, full_screen.

    :param button: Auxiliary or main window options.
    :param window_type: Type of window that need to be controlled.
    :return: None.
    """
    if button == 'close':
        close_window_control(window_type)
    elif button == 'minimize':
        minimize_window_control(window_type)
    elif button == 'maximize':
        maximize_window_control(window_type)
    elif button == 'restore':
        restore_window_control(window_type)
    elif button == 'full_screen':
        full_screen_control(window_type)
    else:
        raise APIHelperError('Button option is not supported.')


def close_customize_page():
    """Close the 'Customize...' page by pressing the 'Done' button."""
    customize_done_button_pattern = Pattern('customize_done_button.png')
    try:
        wait(customize_done_button_pattern, 10)
        logger.debug('Done button found.')
        click(customize_done_button_pattern)
    except FindError:
        raise APIHelperError(
            'Can\'t find the Done button in the page, aborting.')


def close_firefox(test):
    if test.firefox_runner is not None and test.firefox_runner.process_handler is not None:
        logger.debug('Closing Firefox ...')
        quit_firefox()
        status = test.firefox_runner.process_handler.wait(
            Settings.FIREFOX_TIMEOUT)
        if status is None:
            logger.warning('Firefox is hanging. Executing force quit.')
            test.firefox_runner.stop()
            test.firefox_runner = None
    else:
        logger.debug('Firefox already closed. Skipping ...')


def close_window_control(window_type):
    """Click on close window control.

    :param window_type: Type of window that need to be closed.
    :return: None.
    """
    find_window_controls(window_type)

    if window_type == 'auxiliary':
        if Settings.is_mac():
            hover(AuxiliaryWindow.RED_BUTTON_PATTERN, 0.3)
            click(AuxiliaryWindow.HOVERED_RED_BUTTON)
        else:
            click(AuxiliaryWindow.CLOSE_BUTTON)
    else:
        if Settings.is_mac():
            hover(MainWindow.UNHOVERED_MAIN_RED_CONTROL, 0.3)
            click(MainWindow.HOVERED_MAIN_RED_CONTROL)
        else:
            click(MainWindow.CLOSE_BUTTON)


def close_content_blocking_pop_up():
    """Closes the content blocking pop up"""
    pop_up_region = Region(0, 100, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    try:
        pop_up_region.wait(ContentBlocking.POP_UP_ENABLED, 5)
        logger.debug('Content blocking is present on the page and can be closed.')
        pop_up_region.click(ContentBlocking.CLOSE_CB_POP_UP)
    except FindError:
        logger.debug('Couldn\'t find the Content blocking pop up.')
        pass


def confirm_close_multiple_tabs():
    """Click confirm 'Close all tabs' for warning popup when multiple tabs are
    opened.
    """
    close_all_tabs_button_pattern = Pattern('close_all_tabs_button.png')

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
        image = Pattern('iris_logo.png')

    try:
        wait(image, 60)
    except Exception:
        raise APIHelperError('Can\'t launch Firefox - aborting test run.')


def copy_to_clipboard():
    """Return the value copied to clipboard."""
    edit_select_all()
    edit_copy()
    value = Env.get_clipboard().strip()
    logger.debug("Copied to clipboard: %s" % value)
    return value


def create_firefox_args(test_case):
    """Create a list with firefox arguments.

    :param test_case: Instance of BaseTest class.
    :return: list of firefox arguments.
    """

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
                logger.warning(
                    'Windows of less than 600 pixels wide may cause Iris to \
                    fail.')
    except ValueError:
        raise APIHelperError(
            'Incorrect window size specified. Must specify width and height \
            separated by lowercase x.')

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


def create_region_for_hamburger_menu():
    """Create region for hamburger menu pop up."""

    hamburger_menu_pattern = NavBar.HAMBURGER_MENU
    try:
        wait(hamburger_menu_pattern, 10)
        click(hamburger_menu_pattern)
        time.sleep(0.5)
        sign_in_to_sync = Pattern('sign_in_to_sync.png')
        if Settings.get_os() == Platform.LINUX:
            quit_menu_pattern = Pattern('quit.png')
            return create_region_from_patterns(None, sign_in_to_sync,
                                               quit_menu_pattern, None,
                                               padding_right=20)
        elif Settings.get_os() == Platform.MAC:
            help_menu_pattern = Pattern('help.png')
            return create_region_from_patterns(None, sign_in_to_sync,
                                               help_menu_pattern, None,
                                               padding_right=20)
        else:
            exit_menu_pattern = Pattern('exit.png')
            return create_region_from_patterns(None, sign_in_to_sync,
                                               exit_menu_pattern, None,
                                               padding_right=20)
    except (FindError, ValueError):
        raise APIHelperError(
            'Can\'t find the hamburger menu in the page, aborting test.')


def create_region_for_url_bar():
    """Create region for the right side of the url bar."""

    try:
        hamburger_menu_pattern = NavBar.HAMBURGER_MENU
        show_history_pattern = LocationBar.HISTORY_DROPMARKER
        select_location_bar()
        return create_region_from_patterns(show_history_pattern,
                                           hamburger_menu_pattern,
                                           padding_top=20,
                                           padding_bottom=20)
    except FindError:
        raise APIHelperError('Could not create region for URL bar.')


def create_region_from_image(image):
    """Create region starting from a pattern.

    :param image: Pattern used to create a region.
    :return: None.
    """
    try:
        m = find(image)
        if m:
            hamburger_pop_up_menu_weight = 285
            hamburger_pop_up_menu_height = 655
            logger.debug('Creating a region for Hamburger menu pop up.')
            region = Region(m.x - hamburger_pop_up_menu_weight, m.y,
                            hamburger_pop_up_menu_weight,
                            hamburger_pop_up_menu_height)
            return region
        else:
            raise APIHelperError('No matching found.')
    except FindError:
        raise APIHelperError('Image not present.')


def dont_save_password():
    """Do not save the password for a login."""
    if exists(Pattern('dont_save_password_button.png'), 10):
        click(Pattern('dont_save_password_button.png'))
    else:
        raise APIHelperError('Unable to find dont_save_password_button.png.')


def find_window_controls(window_type):
    """Find window controls for main and auxiliary windows.

    :param window_type: Controls for a specific window type.
    :return: None.
    """
    if window_type == 'auxiliary':
        hover(Location(1, 300))

        if Settings.is_mac():
            try:
                wait(AuxiliaryWindow.RED_BUTTON_PATTERN.similar(0.9), 5)
                logger.debug('Auxiliary window control found.')
            except FindError:
                raise APIHelperError('Can\'t find the auxiliary window controls, aborting.')
        else:
            if Settings.is_linux():
                hover(Location(80, 0))
            try:
                wait(AuxiliaryWindow.CLOSE_BUTTON, 5)
                logger.debug('Auxiliary window control found.')
            except FindError:
                raise APIHelperError(
                    'Can\'t find the auxiliary window controls, aborting.')

    elif window_type == 'main':
        if Settings.is_mac():
            try:
                wait(MainWindow.MAIN_WINDOW_CONTROLS.similar(0.9), 5)
                logger.debug('Main window controls found.')
            except FindError:
                raise APIHelperError('Can\'t find the Main window controls, aborting.')
        else:
            try:
                if Settings.is_linux():
                    reset_mouse()
                wait(MainWindow.CLOSE_BUTTON, 5)
                logger.debug('Main window control found.')
            except FindError:
                raise APIHelperError(
                    'Can\'t find the Main window controls, aborting.')
    else:
        raise APIHelperError('Window Type not supported.')


def full_screen_control(window_type):
    """Click on full screen window mode (Applicable only for MAC system).

    :param window_type: Type of window that need to be maximized in full screen mode.
    :reurn: None.
    """
    if Settings.is_mac():
        find_window_controls(window_type)

        if window_type == 'auxiliary':
            width, height = AuxiliaryWindow.AUXILIARY_WINDOW_CONTROLS.get_size()
            click(AuxiliaryWindow.AUXILIARY_WINDOW_CONTROLS.target_offset(width - 10, height / 2))
        else:
            width, height = MainWindow.MAIN_WINDOW_CONTROLS.get_size()
            click(MainWindow.MAIN_WINDOW_CONTROLS.target_offset(width - 10, height / 2))
    else:
        raise APIHelperError('Full screen mode applicable only for MAC')


def get_firefox_build_id(build_path):
    """Returns build id string from the dictionary generated by mozversion
    library.

    :param build_path: Path to the binary for the application or Android APK
    file.
    """
    if build_path is None:
        return None

    return get_firefox_info(build_path)['platform_buildid']


def get_firefox_build_id_from_about_config():
    """Returns the Firefox build id from 'about:config' page."""

    pref_1 = 'browser.startup.homepage_override.buildID'
    pref_2 = 'extensions.lastAppBuildId'

    try:
        return get_pref_value(pref_1)
    except APIHelperError:
        try:
            return get_pref_value(pref_2)
        except APIHelperError:
            raise APIHelperError(
                'Could not retrieve firefox build id information from \
                about:config page.')


def get_firefox_channel(build_path):
    """Returns Firefox channel from application repository.

    :param build_path: Path to the binary for the application or Android APK
    file.
    """

    if build_path is None:
        return None

    fx_channel = get_firefox_info(build_path)['application_repository']
    if 'beta' in fx_channel:
        return 'beta'
    elif 'release' in fx_channel:
        return 'release'
    elif 'esr' in fx_channel:
        return 'esr'
    else:
        return 'nightly'


def get_firefox_channel_from_about_config():
    """Returns the Firefox channel from 'about:config' page."""

    try:
        return get_pref_value('app.update.channel')
    except APIHelperError:
        raise APIHelperError(
            'Could not retrieve firefox channel information from about:config \
            page.')


def get_firefox_info(build_path):
    """Returns the application version information as a dict with the help of
    mozversion library.

    :param build_path: Path to the binary for the application or Android APK
    file.
    """
    if build_path is None:
        return None
    import mozlog
    mozlog.commandline.setup_logging('mozversion', None, {})
    return mozversion.get_version(binary=build_path)


def get_firefox_locale_from_about_config():
    """Returns the Firefox locale from 'about:config' page."""

    try:
        value_str = get_pref_value(
            'browser.newtabpage.activity-stream.feeds.section.topstories.options')  # nopep8
        logger.debug(value_str)
        temp = json.loads(value_str)
        return str(temp['stories_endpoint']).split('&locale_lang=')[1].split('&')[0]  # nopep8
    except (APIHelperError, KeyError):
        raise APIHelperError('Pref format to determine locale has changed.')


def get_firefox_region():
    # TODO: needs better logic to determine bounds.
    """For now, just return the Primary Monitor."""
    return Screen(0)


def get_firefox_version(build_path):
    """Returns application version string from the dictionary generated by
    mozversion library.

    :param build_path: Path to the binary for the application or Android APK
    file.
    """
    if build_path is None:
        return None
    return get_firefox_info(build_path)['application_version']


def get_firefox_version_from_about_config():
    """Returns the Firefox version from 'about:config' page."""

    try:
        return get_pref_value('extensions.lastAppVersion')
    except APIHelperError:
        raise APIHelperError(
            'Could not retrieve firefox version information from about:config \
            page.')


def get_main_modifier():
    """Return the main modifier."""
    if Settings.get_os() == Platform.MAC:
        main_modifier = Key.CMD
    else:
        main_modifier = Key.CTRL
    return main_modifier


def get_menu_modifier():
    """Return the menu modifier."""
    if Settings.get_os() == Platform.MAC:
        menu_modifier = Key.CTRL
    else:
        menu_modifier = Key.CMD
    return menu_modifier


def get_pref_value(pref_name):
    """Returns the value of a provided preference from 'about:config' page.

    :param pref_name: Preference's name.
    :return: Preference's value.
    """

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
        raise APIHelperError(
            'Failed to retrieve preference value. %s' % e.message)

    close_tab()
    return value


def get_support_info():
    """Returns support information as a JSON object from 'about:support' page.
    """

    copy_raw_data_to_clipboard = Pattern(
        'about_support_copy_raw_data_button.png')

    new_tab()
    select_location_bar()
    paste('about:support')
    type(Key.ENTER)
    time.sleep(Settings.UI_DELAY)

    try:
        click(copy_raw_data_to_clipboard)
        time.sleep(Settings.UI_DELAY_LONG)
        json_text = Env.get_clipboard()
        return json.loads(json_text)
    except Exception as e:
        raise APIHelperError(
            'Failed to retrieve support information value. %s' % e.message)
    finally:
        close_tab()


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
        time.sleep(Settings.UI_DELAY)
        json_text = Env.get_clipboard()
        return json.loads(json_text)
    except Exception as e:
        raise APIHelperError(
            'Failed to retrieve raw message information value. %s' % e.message)
    finally:
        close_tab()


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


def launch_firefox(path, profile=None, url=None, args=None, show_crash_reporter=False):
    """Launch the app with optional args for profile, windows, URI, etc.

    :param path: Firefox path.
    :param profile: Firefox profile.
    :param url: URL to be loaded.
    :param args: Optional list of arguments.
    :param show_crash_reporter: Enable or disable Firefox Crash Reporting tool.
    :return: List of Firefox flags.
    """
    if args is None:
        args = []

    if profile is None:
        raise APIHelperError('No profile name present, aborting run.')

    args.append('-foreground')
    args.append('-no-remote')

    if url is not None:
        args.append('-new-tab')
        args.append(url)

    process_args = {'stream': None}
    logger.debug('Creating Firefox runner ...')
    try:
        runner = FirefoxRunner(binary=path, profile=profile,
                               cmdargs=args, process_args=process_args, show_crash_reporter=show_crash_reporter)
        logger.debug('Firefox runner successfully created.')
        logger.debug('Running Firefox with command: "%s"' %
                     ','.join(runner.command))
        return runner
    except errors.RunnerNotStartedError:
        raise APIHelperError('Error creating Firefox runner.')


def login_site(site_name):
    """Login into a specific site.

    :param site_name: Name of the site.
    :return: None.
    """
    username = get_config_property(site_name, 'username')
    password = get_config_property(site_name, 'password')
    paste(username)
    focus_next_item()
    paste(password)
    focus_next_item()
    type(Key.ENTER)


def maximize_window_control(window_type):
    """Click on maximize window control.

    :param window_type: Type of window that need to be maximized.
    :return: None.
    """
    find_window_controls(window_type)

    if window_type == 'auxiliary':
        if Settings.is_mac():
            key_down(Key.ALT)
            width, height = AuxiliaryWindow.AUXILIARY_WINDOW_CONTROLS.get_size()
            click(AuxiliaryWindow.AUXILIARY_WINDOW_CONTROLS.target_offset(width - 10, height / 2))
            key_up(Key.ALT)
        else:
            click(AuxiliaryWindow.MAXIMIZE_BUTTON)
            if Settings.is_linux():
                reset_mouse()
    else:
        if Settings.is_mac():
            key_down(Key.ALT)
            width, height = MainWindow.MAIN_WINDOW_CONTROLS.get_size()
            click(MainWindow.MAIN_WINDOW_CONTROLS.target_offset(width - 10, height / 2))
            key_up(Key.ALT)
        else:
            click(MainWindow.MAXIMIZE_BUTTON)


def minimize_window_control(window_type):
    """Click on minimize window control.

    :param window_type: Type of window that need to be minimized.
    :return: None.
    """
    find_window_controls(window_type)

    if window_type == 'auxiliary':
        if Settings.is_mac():
            width, height = AuxiliaryWindow.AUXILIARY_WINDOW_CONTROLS.get_size()
            click(AuxiliaryWindow.AUXILIARY_WINDOW_CONTROLS.target_offset(width / 2, height / 2))
        else:
            click(AuxiliaryWindow.MINIMIZE_BUTTON)
    else:
        if Settings.is_mac():
            width, height = MainWindow.MAIN_WINDOW_CONTROLS.get_size()
            click(MainWindow.MAIN_WINDOW_CONTROLS.target_offset(width / 2, height / 2))
        else:
            click(MainWindow.MINIMIZE_BUTTON)


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


def navigate_slow(url):
    """Navigates slow, via the location bar, to a given URL.

    :param url: The string to type into the location bar.
    :return: None.

    The function handles typing 'Enter' to complete the action.
    """

    try:
        select_location_bar()
        Settings.type_delay = 0.1
        type(url + Key.ENTER)
    except Exception:
        raise APIHelperError(
            'No active window found, cannot navigate to page.')


def open_about_firefox():
    """Open the 'About Firefox' window."""
    if Settings.get_os() == Platform.MAC:
        type(Key.F3, modifier=KeyModifier.CTRL)
        type(Key.F2, modifier=KeyModifier.CTRL)

        time.sleep(0.5)
        type(Key.RIGHT)
        type(Key.DOWN)
        type(Key.DOWN)
        type(Key.ENTER)

    elif Settings.get_os() == Platform.WINDOWS:
        type(Key.ALT)
        if parse_args().locale != 'ar':
            type(Key.LEFT)
        else:
            type(Key.RIGHT)
        type(Key.ENTER)
        type(Key.UP)
        type(Key.ENTER)

    else:
        type(Key.F10)
        if parse_args().locale != 'ar':
            type(Key.LEFT)
        else:
            type(Key.RIGHT)
        type(Key.UP)
        type(Key.ENTER)


def open_library_menu(option):
    """Open the Library menu with an option as argument.

    :param option: Library menu option.
    :return: Custom region created for a more efficient and accurate image
    pattern search.
    """

    library_menu_pattern = NavBar.LIBRARY_MENU

    try:
        wait(library_menu_pattern, 10)
        region = Region(find(library_menu_pattern).x - SCREEN_WIDTH / 4,
                        find(library_menu_pattern).y, SCREEN_WIDTH / 4,
                        SCREEN_HEIGHT / 4)
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


def open_zoom_menu():
    """Open the 'Zoom' menu from the 'View' menu."""

    if Settings.get_os() == Platform.MAC:
        view_menu_pattern = Pattern('view_menu.png')
        click(view_menu_pattern)
        for i in range(3):
            type(text=Key.DOWN)
        type(text=Key.ENTER)
    else:
        type(text='v', modifier=KeyModifier.ALT)
        for i in range(2):
            type(text=Key.DOWN)
        type(text=Key.ENTER)


def restore_window_control(window_type):
    """Click on restore window control.

    :param window_type: Type of window that need to be restored.
    :return: None.
    """
    find_window_controls(window_type)

    if window_type == 'auxiliary':
        if Settings.is_mac():
            key_down(Key.ALT)
            width, height = AuxiliaryWindow.AUXILIARY_WINDOW_CONTROLS.get_size()
            click(AuxiliaryWindow.AUXILIARY_WINDOW_CONTROLS.target_offset(width - 10, height / 2))
            key_up(Key.ALT)
        else:
            if Settings.is_linux():
                reset_mouse()
            click(AuxiliaryWindow.ZOOM_RESTORE_BUTTON)
    else:
        if Settings.is_mac():
            key_down(Key.ALT)
            width, height = MainWindow.MAIN_WINDOW_CONTROLS.get_size()
            click(MainWindow.MAIN_WINDOW_CONTROLS.target_offset(width - 10, height / 2))
            key_up(Key.ALT)
        else:
            if Settings.is_linux():
                reset_mouse()
            click(MainWindow.RESIZE_BUTTON)


def remove_zoom_indicator_from_toolbar():
    """Remove the zoom indicator from toolbar by clicking on the 'Remove from
    Toolbar' button.
    """

    zoom_control_toolbar_decrease_pattern = NavBar.ZOOM_OUT
    remove_from_toolbar_pattern = Pattern('remove_from_toolbar.png')

    try:
        wait(zoom_control_toolbar_decrease_pattern, 10)
        logger.debug('\'Decrease\' zoom control found.')
        right_click(zoom_control_toolbar_decrease_pattern)
    except FindError:
        raise APIHelperError(
            'Can\'t find the \'Decrease\' zoom control button in the page, \
            aborting.')

    try:
        wait(remove_from_toolbar_pattern, 10)
        logger.debug('\'Remove from Toolbar\' option found.')
        click(remove_from_toolbar_pattern)
    except FindError:
        raise APIHelperError(
            'Can\'t find the \'Remove from Toolbar\' option in the page, \
            aborting.')

    try:
        wait_vanish(zoom_control_toolbar_decrease_pattern, 10)
    except FindError:
        raise APIHelperError(
            'Zoom indicator not removed from toolbar, aborting.')


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


def reset_mouse():
    """Reset mouse position to location (0, 0)."""
    hover(Location(0, 0))


def restart_firefox(test, path, profile, url, args=None, image=None, show_crash_reporter=False):
    """Restart the app with optional args for profile.

    :param test: current test
    :param path: Firefox path.
    :param profile: Firefox profile.
    :param url: URL to be loaded.
    :param args: Optional list of arguments.
    :param image: Image checked to confirm that Firefox has successfully
    :param show_crash_reporter: Enable or disable Firefox Crash Reporting tool.
    restarted.
    :return: None.
        """
    logger.debug('Restarting firefox ...')
    close_firefox(test)
    test.firefox_runner = launch_firefox(path, profile, url, args, show_crash_reporter)
    test.firefox_runner.start()
    confirm_firefox_launch(image)
    logger.debug('Firefox successfully restarted.')


def restore_firefox_focus():
    """Restore Firefox focus by clicking the panel near HOME or REFRESH button."""

    try:
        if exists(NavBar.HOME_BUTTON, DEFAULT_UI_DELAY):
            target_pattern = NavBar.HOME_BUTTON
        else:
            target_pattern = NavBar.RELOAD_BUTTON
        w, h = target_pattern.get_size()
        horizontal_offset = w * 1.7
        click_area = target_pattern.target_offset(horizontal_offset, 0)
        click(click_area)
    except FindError:
        raise APIHelperError('Could not restore firefox focus.')


def restore_window_from_taskbar(option=None):
    """Restore firefox from taskbar."""
    if Settings.get_os() == Platform.MAC:
        try:
            click(Pattern('main_menu_window.png'))
            if option == "browser_console":
                click(Pattern('window_browser_console.png'))
            else:
                click(Pattern('window_firefox.png'))
        except FindError:
            raise APIHelperError('Restore window from taskbar unsuccessful.')
    elif get_os_version() == 'win7':
        try:
            click(Pattern('firefox_start_bar.png'))
            if option == "library_menu":
                click(Pattern('firefox_start_bar_library.png'))
            if option == "browser_console":
                click(Pattern('firefox_start_bar_browser_console.png'))
        except FindError:
            raise APIHelperError('Restore window from taskbar unsuccessful.')

    else:
        type(text=Key.TAB, modifier=KeyModifier.ALT)
        if Settings.get_os() == Platform.LINUX:
            hover(Location(0, 50))
    time.sleep(Settings.UI_DELAY)


def scroll_until_pattern_found(image_pattern, scroll_function, scroll_params, num_of_scroll_iterations=10, timeout=3):
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
    if Settings.get_os() == Platform.WINDOWS:
        for i in range(option_number + 1):
            type(text=Key.DOWN)
        type(text=Key.ENTER)
    else:
        for i in range(option_number - 1):
            type(text=Key.DOWN)
        type(text=Key.ENTER)


def select_zoom_menu_option(option_number):
    """Open the 'Zoom' menu from the 'View' menu and select option."""

    open_zoom_menu()

    for i in range(option_number):
        type(text=Key.DOWN)
    type(text=Key.ENTER)


def wait_for_firefox_restart():
    """Wait for Firefox to restart."""

    try:
        home_pattern = NavBar.HOME_BUTTON
        wait_vanish(home_pattern, 10)
        logger.debug('Firefox successfully closed.')
        wait(home_pattern, 20)
        logger.debug('Successful Firefox restart performed.')
    except FindError:
        raise APIHelperError(
            'Firefox restart has not been performed, aborting.')


def write_profile_prefs(test_case):
    """Add test case setup prefs.

    :param test_case: Instance of BaseTest class.
    :return: None.
    """

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


def zoom_with_mouse_wheel(nr_of_times=1, zoom_type=None):
    """Zoom in/Zoom out using the mouse wheel.

    :param nr_of_times: Number of times the 'zoom in'/'zoom out' action should
    take place.
    :param zoom_type: Type of the zoom action('zoom in'/'zoom out') intended to
    be performed.
    :return: None.
    """

    # Move focus in the middle of the page to be able to use the scroll.
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


def open_directory(directory):
    if Settings.get_os() == Platform.WINDOWS:
        os.startfile(directory)
    elif Settings.get_os() == Platform.LINUX:
        os.system('xdg-open \"' + directory + '\"')
    else:
        os.system('open \"' + directory + '\"')


class Option(object):
    """Class with zoom members."""

    ZOOM_IN = 0
    ZOOM_OUT = 1
    RESET = 2
    ZOOM_TEXT_ONLY = 3


class RightClickLocationBar(object):
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

    IN = 300 if Settings.is_windows() else 1
    OUT = -300 if Settings.is_windows() else -1


# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import shutil
import subprocess

from iris.api.helpers.keyboard_shortcuts import *
from iris.configuration.config_parser import *

logger = logging.getLogger(__name__)


def launch_firefox(path, profile='empty_profile', url=None, args=None):
    """Launch the app with optional args for profile, windows, URI, etc."""
    if args is None:
        args = []
    current_dir = os.path.split(__file__)[0]
    active_profile = os.path.join(current_dir, 'test_profiles', profile)
    if not os.path.exists(active_profile):
        os.mkdir(active_profile)

    cmd = [path, '-foreground', '-no-remote', '-profile', active_profile]

    # Add other Firefox flags
    for arg in args:
        cmd.append(arg)

    if url is not None:
        cmd.append('-new-tab')
        cmd.append(url)

    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return


def clean_profiles():
    path = os.path.join(os.path.split(__file__)[0], 'test_profiles')
    if os.path.exists(path):
        shutil.rmtree(path)
    os.mkdir(path)


def confirm_firefox_launch():
    """waits for firefox to exist by waiting for the home button to be present."""
    try:
        wait('home.png', 20)
    except Exception as err:
        logger.error(err)
        print ('Can\'t launch Firefox - aborting test run.')
        exit(1)


def confirm_firefox_quit():
    try:
        waitVanish('home.png', 10)
    except FindError:
        print ('Firefox still around - aborting test run.')
        exit(1)


def get_firefox_region():
    # TODO: needs better logic to determine bounds
    # For now, just return the whole screen
    return get_screen()


def navigate_slow(url):
    """Navigates, via the location bar, to a given URL
    :param:
        url - the string to type into the location bar.

    The function handles typing 'Enter' to complete the action.
    """
    select_location_bar()
    # increase the delay between each keystroke while typing strings
    # (sikuli defaults to .02 sec)
    Settings.TypeDelay = 0.1
    type(url + Key.ENTER)


def navigate(url):
    select_location_bar()
    paste(url)
    type(Key.ENTER)


def restart_firefox(args):
    # just as it says, with options
    return


def get_menu_modifier():
    if get_os() == Platform.MAC:
        menu_modifier = Key.CTRL
    else:
        menu_modifier = Key.CMD
    return menu_modifier


def get_main_modifier():
    if get_os() == Platform.MAC:
        main_modifier = Key.CMD
    else:
        main_modifier = Key.CTRL
    return main_modifier


def copy_to_clipboard():
    edit_select_all()
    edit_copy()
    value = Env.getClipboard().strip()
    logger.debug("Copied to clipboard: %s" % value)
    return value


def change_preference(pref_name, value):
    # Open preferences in new tab
    new_tab()
    time.sleep(1)

    # Sometimes we lose focus, therefore
    # an explicit selection is required here
    select_location_bar()
    type('about:config' + Key.ENTER)
    time.sleep(1)

    type(Key.SPACE)
    time.sleep(1)

    type(pref_name)
    time.sleep(2)
    type(Key.TAB)
    time.sleep(2)

    retrieved_value = None
    try:
        retrieved_value = copy_to_clipboard().split(';'[0])[1]
    except:
        logger.error('Failed to retrieve preference value')
        return None

    if retrieved_value == value:
        logger.debug('Flag is already set to value:' + value)
        return None
    else:
        # Typing enter here will toggle a boolean value
        type(Key.ENTER)
        # For non-boolean values, a dialog box should appear
        dialog_box = Pattern('preference_dialog_icon.png')
        if exists(dialog_box, 3):
            type(dialog_box, value)
            type(Key.ENTER)
    close_tab()


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
    try:
        if exists('dont_save_password_button.png', 10):
            click('dont_save_password_button.png')
    except FindError:
        logger.error('Failed to find save password dialog')
        return None


def click_hamburger_menu_option(option):
    try:
        wait('hamburger_menu.png', 10)
        region = create_region_from_image('hamburger_menu.png')
        logger.debug('hamburger menu found')
    except:
        logger.error('Can\'t find the "hamburger menu" in the page, aborting test.')
        return
    else:
        click('hamburger_menu.png')
        try:
            region.wait(option, 10)
            logger.debug('Option found')
        except FindError:
            logger.error('Can\'t find the option in the page, aborting test.')
            return
        else:
            region.click(option)
            return region


def close_auxiliary_window():
    try:
        wait('auxiliary_window_close_button.png', 10)
        logger.debug('Close auxiliary window button found')
    except FindError:
        logger.error('Can\'t find the close auxiliary window button in the page, aborting.')
        return
    else:
        click('auxiliary_window_close_button.png')


def close_customize_page():
    try:
        wait('customize_done_button.png', 10)
        logger.debug('Done button found')
    except FindError:
        logger.error('Can\'t find the Done button in the page, aborting.')
        return
    else:
        click('customize_done_button.png')


def open_about_firefox():
    if get_os() == Platform.MAC:
        # Key stroke into Firefox Menu to get to About Firefox
        type(Key.F2, modifier=KeyModifier.CTRL)
        time.sleep(0.5)
        type(text=Key.ESC)
        time.sleep(0.5)

        type(Key.RIGHT)
        type(Key.DOWN)
        type(Key.DOWN)
        type(Key.ENTER)

    elif get_os() == Platform.WINDOWS:
        # Use Help menu keyboard shortcuts to open About Firefox
        keyDown(Key.ALT)
        type('h')
        time.sleep(0.5)
        type('a')
        keyUp(Key.ALT)

    else:
        # Use Help menu keyboard shortcuts to open About Firefox
        keyDown(Key.ALT)
        type('h')
        time.sleep(1)
        keyUp(Key.ALT)
        type('a')


def create_region_from_image(image):
    try:
        m = find(image)
        if m:
            hamburger_pop_up_menu_weight = 285
            hamburger_pop_up_menu_height = 655
            logger.debug('Creating a region for Hamburger Pop Up Menu')
            region = Region(m.getX() - hamburger_pop_up_menu_weight, m.getY(), hamburger_pop_up_menu_weight,
                                   hamburger_pop_up_menu_height)
            return region
        else:
            logger.error('No Matching found')
    except:
        logger.error('Image not present')


def restore_window_from_taskbar():
    if get_os() == Platform.MAC:
        type(text=Key.TAB, modifier=KeyModifier.CMD)
        time.sleep(0.1)
        keyDown(Key.CMD)
        keyDown(Key.TAB)
        keyUp(Key.TAB)
        keyDown(Key.ALT)
        keyUp(Key.CMD)
        keyUp(Key.ALT)
    else:
        type(text=Key.TAB, modifier=KeyModifier.ALT)

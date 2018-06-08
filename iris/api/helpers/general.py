# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from distutils import dir_util
from distutils.spawn import find_executable

import shutil
import subprocess

from iris.api.helpers.keyboard_shortcuts import *
from iris.configuration.config_parser import *

logger = logging.getLogger(__name__)


def launch_firefox(path, profile=None, url=None, args=None):
    """Launch the app with optional args for profile, windows, URI, etc."""
    if args is None:
        args = []

    if profile is None:
        logger.warning('No profile name present, using last default profile on disk.')
        profile = os.path.join(os.path.expanduser('~'), '.iris', 'profiles', 'default')

    cmd = [path, '-foreground', '-no-remote', '-profile', profile]

    # Add other Firefox flags
    for arg in args:
        cmd.append(arg)

    if url is not None:
        cmd.append('-new-tab')
        cmd.append(url)

    logger.debug('Launching Firefox with arguments: %s' % ' '.join(cmd))
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return


def clean_profiles():
    profile_cache = os.path.join(os.path.expanduser('~'), '.iris', 'profiles')
    if os.path.exists(profile_cache):
        shutil.rmtree(profile_cache)
    os.mkdir(profile_cache)


def confirm_firefox_launch():
    """waits for firefox to exist by waiting for the home button to be present."""
    try:
        wait('home.png', 20)
    except Exception as err:
        logger.error(err)
        logger.error('Can\'t launch Firefox - aborting test run.')
        exit(1)


def confirm_firefox_quit():
    try:
        waitVanish('home.png', 10)
    except FindError:
        logger.error('Firefox still around - aborting test run.')
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
    try:
        wait('home.png', 5)
        select_location_bar()
        # increase the delay between each keystroke while typing strings
        # (sikuli defaults to .02 sec)
        Settings.TypeDelay = 0.1
        type(url + Key.ENTER)
    except:
        logger.error('No active window found, cannot navigate to page')


def navigate(url):
    try:
        wait('home.png', 5)
        select_location_bar()
        paste(url)
        type(Key.ENTER)
    except:
        logger.error('No active window found, cannot navigate to page')
        raise APIHelperError


def restart_firefox(path, profile, url, args=None):
    # just as it says, with options
    logger.debug('Restarting Firefox')
    quit_firefox()
    logger.debug('Confirming that Firefox has been quit')
    confirm_firefox_quit()
    # Give Firefox a chance to cleanly shutdown all of its processes
    # TODO: This should be made into a robust function instead of a hard coded sleep
    time.sleep(3)
    logger.debug('Relaunching Firefox with profile name \'%s\'' % profile)
    launch_firefox(path, profile, url, args)
    logger.debug('Confirming that Firefox has been launched')
    confirm_firefox_launch()
    logger.debug('Successful Firefox restart performed')
    return


def get_menu_modifier():
    if Settings.getOS() == Platform.MAC:
        menu_modifier = Key.CTRL
    else:
        menu_modifier = Key.CMD
    return menu_modifier


def get_main_modifier():
    if Settings.getOS() == Platform.MAC:
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
    if exists('dont_save_password_button.png', 10):
        click('dont_save_password_button.png')
    else:
        raise FindError('Unable to find dont_save_password_button.png')


def click_hamburger_menu_option(option):
    hamburger_menu = 'hamburger_menu.png'
    try:
        wait(hamburger_menu, 10)
        region = create_region_from_image(hamburger_menu)
        logger.debug('hamburger menu found')
    except:
        logger.error('Can\'t find the "hamburger menu" in the page, aborting test.')
        return
    else:
        click(hamburger_menu)
        time.sleep(1)
        try:
            time.sleep(1)
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


def click_cancel_button():
    try:
        wait('cancel_button.png', 10)
        logger.debug('Cancel button found')
    except FindError:
        logger.error('Can\'t find the cancel button, aborting.')
        return
    else:
        click('cancel_button.png')


def close_customize_page():
    customize_done_button = 'customize_done_button.png'
    try:
        wait(customize_done_button, 10)
        logger.debug('Done button found')
    except FindError:
        logger.error('Can\'t find the Done button in the page, aborting.')
        return
    else:
        click(customize_done_button)


def open_about_firefox():
    if Settings.getOS() == Platform.MAC:
        # Key stroke into Firefox Menu to get to About Firefox.
        type(Key.F2, modifier=KeyModifier.CTRL)

        time.sleep(0.5)
        type(Key.RIGHT)
        type(Key.DOWN)
        type(Key.DOWN)
        type(Key.ENTER)

    elif Settings.getOS() == Platform.WINDOWS:
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
    if Settings.getOS() == Platform.MAC:
        click('main_menu_window.png')
        type(Key.DOWN)
        time.sleep(.5)
        type(Key.ENTER)
    else:
        type(text=Key.TAB, modifier=KeyModifier.ALT)


def open_library_menu(option):
    library_menu = 'library_menu.png'
    try:
        wait(library_menu, 10)
        region = Region(find(library_menu).getX() - screen_width / 4, find(library_menu).getY(), screen_width / 4,
                        screen_height / 4)
        logger.debug('Library menu found')
    except:
        logger.error('Can\'t find the library menu in the page, aborting test.')
        return
    else:
        click(library_menu)
        time.sleep(1)
        try:
            time.sleep(1)
            region.wait(option, 10)
            logger.debug('Option found')
        except FindError:
            logger.error('Can\'t find the option in the page, aborting test.')
            return
        else:
            region.click(option)
            return region


def maximize_auxiliary_window():
    # This is different from maximize_window() since on OSX the auxiliary window controls are on grey background vs
    # black background for the main browser window

    if get_os() == Platform.MAC:
        library_controls = 'library_controls.png'
        # Set target to the maximize button
        maximize_button = Pattern(library_controls).targetOffset(48, 7)
        # We must hover the controls so the ALT key can take effect there.
        hover(library_controls)
        # Alt key changes maximize button from full screen to maximize window.
        keyDown(Key.ALT)
        click(maximize_button)
        keyUp(Key.ALT)

    elif get_os() == Platform.WINDOWS:
        type(text=Key.UP, modifier=KeyModifier.WIN)
    else:
        type(text=Key.UP, modifier=KeyModifier.CTRL + KeyModifier.META)


def remove_zoom_indicator_from_toolbar():
    zoom_control_toolbar_decrease = 'zoom_control_toolbar_decrease.png'
    remove_from_toolbar = 'remove_from_toolbar.png'

    try:
        wait(zoom_control_toolbar_decrease, 10)
        logger.debug('\'Decrease\' zoom control found.')
    except FindError:
        logger.error('Can\'t find the \'Decrease\' zoom control button in the page, aborting.')
        return
    else:
        rightClick(zoom_control_toolbar_decrease)

    time.sleep(1)

    if exists(remove_from_toolbar, 10):
        click(remove_from_toolbar)
    else:
        raise FindError('Unable to find the remove_from_toolbar.png.')

    try:
        waitVanish(zoom_control_toolbar_decrease, 10)
    except FindError:
        logger.error('Zoom indicator not removed from toolbar - aborting test run.')
        exit(1)


class _IrisProfile(object):

    # Disk locations for both profile cache and staged profiles.
    PROFILE_CACHE = os.path.join(os.path.expanduser('~'), '.iris', 'profiles')
    STAGED_PROFILES = os.path.join(get_module_dir(), 'iris', 'profiles')

    @property
    def DEFAULT(self):
        """Default profile that test cases will use, specified in BaseTest."""
        return Profile.LIKE_NEW

    @property
    def BRAND_NEW(self):
        """Make unique profile name using time stamp."""
        new_profile = os.path.join(Profile.PROFILE_CACHE, 'brand_new_' + Profile._create_unique_profile_name())
        logger.debug('Creating brand new profile: %s' % new_profile)
        os.mkdir(new_profile)
        return new_profile

    @property
    def LIKE_NEW(self):
        """Open a staged profile that already has ten bookmarks."""
        logger.debug('Creating new profile from LIKE_NEW staged profile')
        return self._get_staged_profile('like_new')

    @property
    def TEN_BOOKMARKS(self):
        """Open a staged profile that already has ten bookmarks."""
        logger.debug('Creating new profile from TEN_BOOKMARKS staged profile')
        return self._get_staged_profile('ten_bookmarks')

    def _get_staged_profile(self, profile_name):
        # Find 7zip binary
        sz_bin = find_executable('7z')
        if sz_bin is None:
            logger.critical('Cannot find 7zip')
            exit(5)
        logger.debug('Using 7zip executable at "%s"' % sz_bin)

        zipped_profile = os.path.join(Profile.STAGED_PROFILES, '%s.zip' % profile_name)

        cmd = [sz_bin, 'x', '-y', '-bd', '-o%s' % Profile.STAGED_PROFILES, zipped_profile]
        logger.debug('Unzipping profile with command "%s"' % ' '.join(cmd))
        try:
            output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            logger.error('7zip failed: %s' % repr(e.output))
            raise Exception('Unable to unzip profile')
        logger.debug('7zip succeeded: %s' % repr(output))

        # Find the desired profile
        from_directory = os.path.join(Profile.STAGED_PROFILES, profile_name)

        # Create a unique name for the profile.
        temp_name = '%s_%s' % (profile_name, Profile._create_unique_profile_name())

        # Create a folder to hold that profile's contents.
        to_directory = os.path.join(Profile.PROFILE_CACHE, temp_name)
        logger.debug('Creating new profile: %s' % to_directory)
        os.mkdir(to_directory)

        # Duplicate profile.
        dir_util.copy_tree(from_directory, to_directory)

        # Remove unzipped directory first.
        shutil.rmtree(from_directory)

        # Remove Mac resource fork folders left over from ZIP, if present.
        resource_fork_folder = os.path.join(Profile.STAGED_PROFILES, '__MACOSX')
        if os.path.exists(resource_fork_folder):
            try:
                shutil.rmtree(resource_fork_folder)
            except WindowsError:
                # This error can happen, but does not affect Iris.
                logger.debug('Error, can\'t remove orphaned directory, leaving in place')

        # Return path to profile in cache.
        return to_directory

    @staticmethod
    def _create_unique_profile_name():
        ts = int(time.time())
        profile_name = 'profile_%s' % ts
        return profile_name


Profile = _IrisProfile()

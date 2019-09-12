# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import importlib
import logging
import os
import shutil
import subprocess
import time
from distutils.dir_util import copy_tree

import psutil
import pytest
from mozprofile import Profile as MozProfile
from mozrunner import FirefoxRunner

from src.configuration.config_parser import validate_config_ini
from src.control_center.commands import delete
from src.core.api.keyboard.key import KeyModifier
from src.core.api.keyboard.keyboard import type
from src.core.api.keyboard.keyboard_util import check_keyboard_state
from src.core.api.os_helpers import OSHelper
from src.core.api.settings import Settings
from src.core.util.cleanup import *
from src.core.util.target_loader import collect_tests
from src.core.util.arg_parser import get_core_args, set_core_arg
from src.core.util.json_utils import create_target_json
from src.core.util.local_web_server import LocalWebServer
from src.core.util.logger_manager import initialize_logger
from src.core.util.path_manager import PathManager
from src.core.util.system import check_7zip, fix_terminal_encoding, init_tesseract_path, reset_terminal_encoding

logger = logging.getLogger(__name__)


def main():
    args = get_core_args()
    initialize_logger()
    migrate_data()
    validate_config_ini(args)
    if verify_config(args):
        pytest_args = None
        settings = None
        if show_control_center():
            init_control_center()
            user_result = launch_control_center()
            logger.debug(user_result)
            if user_result is not 'cancel':
                # Extract list of tests
                if not 'tests' in user_result:
                    exit_iris('No tests chosen, closing Iris.', status=0)

                pytest_args = user_result['tests']

                # Extract target from response and update core arg for target
                set_core_arg('target', user_result['target'])

                # Extract settings from response
                args = get_core_args()
                settings = user_result['args']
            else:
                # User cancelled or otherwise failed to select tests,
                # so we will shut down Iris.
                exit_iris('User cancelled run, closing Iris.', status=0)

        try:
            if pytest_args is None:
                pytest_args = get_test_params()
            if len(pytest_args) == 0:
                exit_iris('No tests found.', status=1)

            pytest_args.append('-vs')
            pytest_args.append('-r ')
            pytest_args.append('-s')
            target_plugin = get_target(args.target)
            if settings is not None:
                logger.debug('Passing settings to target: %s' % settings)
                target_plugin.update_settings(settings)
            initialize_platform(args)
            pytest.main(pytest_args, plugins=[target_plugin])
        except ImportError as e:
            exit_iris('Could not load plugin for %s target, error: %s' % (args.target, e), status=1)
    else:
        logger.error('Failed platform verification.')
        exit(1)


def show_control_center():
    if get_core_args().control:
        return True
    elif get_core_args().target is None:
        exit_iris('No target specified, e.g.: \n\niris your_target\n\nClosing Iris.', status=1)
        return False
    else:
        return False


def get_target(target_name):
    logger.info('Desired target: %s' % target_name)
    try:
        my_module = importlib.import_module('targets.%s.main' % target_name)
        try:
            target_plugin = my_module.Target()
            logger.info('Found target named %s' % target_plugin.target_name)
            return target_plugin
        except NameError:
            exit_iris('Can\'t find default Target class.', status=1)
    except ImportError as e:
        if e.name.__contains__('Xlib') and not OSHelper.is_linux():
            pass
        else:
            exit_iris('Problems importing module:\n%s' % e, status=1)


def initialize_platform(args):
    init()
    fix_terminal_encoding()
    migrate_data()
    PathManager.create_working_directory(args.workdir)
    PathManager.create_run_directory()


def get_test_params():
    tests_to_execute = collect_tests()
    pytest_args = []
    if get_core_args().rerun:
        failed_tests_file = os.path.join(PathManager.get_working_dir(), 'lastfail.txt')
        tests_dir = os.path.join(PathManager.get_tests_dir(), get_core_args().target)
        failed_tests = []
        with open(failed_tests_file, 'r') as f:
            for line in f:
                failed_tests.append(line.rstrip('\n'))
        f.close()
        # Read first line to see if these tests apply to current target.
        if tests_dir in failed_tests[0]:
            pytest_args = failed_tests
        else:
            logging.error('The -a flag cannot be used now because the last failed tests don\'t match current target.')
    else:
        if len(tests_to_execute) > 0:
            for running in tests_to_execute:
                pytest_args.append(running)
        else:
            exit_iris('No tests to execute.', status=1)
    return pytest_args


def verify_config(args):
    """Checks keyboard state is correct, and that Tesseract and 7zip are installed."""
    try:
        if not all([check_keyboard_state(args.no_check), init_tesseract_path(), check_7zip()]):
            exit_iris('Failed platform check, closing Iris.', status=1)
    except KeyboardInterrupt as e:
        exit_iris(e, status=1)
    return True


def init_control_center():
    copy_tree(os.path.join(PathManager.get_module_dir(), 'src', 'control_center', 'assets'), get_core_args().workdir)
    targets_dir = os.path.join(PathManager.get_module_dir(), 'targets')

    exclude_dirs = {'__pycache__'}
    for path, dirs, files in PathManager.sorted_walk(targets_dir):
        [dirs.remove(d) for d in list(dirs) if d in exclude_dirs]
        for target in dirs:
            src = os.path.join(targets_dir, target, 'icon.png')
            dest = os.path.join(get_core_args().workdir, 'images', '%s.png' % target)
            try:
                shutil.copyfile(src, dest)
            except FileNotFoundError:
                logger.warning('Could not find icon file for target: %s' % target)
        break
    create_target_json()


def launch_control_center():
    profile_path = os.path.join(get_core_args().workdir, 'cc_profile')
    fx_path = PathManager.get_local_firefox_path()
    if fx_path is None:
        logger.error('Can\'t find local Firefox installation, aborting Iris run.')
        return False, None

    args = ['http://127.0.0.1:%s' % get_core_args().port]
    process_args = {'stream': None}
    profile = MozProfile(profile=profile_path, preferences={})
    if OSHelper.is_windows():
        process = subprocess.Popen(
            [fx_path, '-no-remote', '-new-tab', args, '--wait-for-browser', '-foreground', '-profile',
             profile.profile], shell=False)

    else:
        fx_runner = FirefoxRunner(binary=fx_path, profile=profile, cmdargs=args, process_args=process_args)
        fx_runner.start()

    server = LocalWebServer(get_core_args().workdir, get_core_args().port)
    server.stop()
    time.sleep(Settings.DEFAULT_UI_DELAY)

    if OSHelper.is_mac():
        type(text='q', modifier=KeyModifier.CMD)
    elif OSHelper.is_windows():
        type(text='w', modifier=[KeyModifier.CTRL, KeyModifier.SHIFT])
    else:
        type(text='q', modifier=KeyModifier.CTRL)
    if OSHelper.is_windows():
        if process.pid is not None:
            try:
                logger.debug('Closing Firefox process ID: %s' % process.pid)
                process = psutil.Process(process.pid)
                for proc in process.children(recursive=True):
                    proc.kill()
                process.kill()
            except psutil.NoSuchProcess:
                pass
    else:
        try:
            fx_runner.stop()
        except Exception as e:
            logger.debug('Error stopping fx_runner')
            logger.debug(e)

    return server.result


def migrate_data():
    iris_1_install = os.path.join(os.path.expanduser('~'), '.iris', 'data', 'all_args.json')
    logger.debug('Old Iris 1 install exists: %s' % os.path.exists(iris_1_install))

    if os.path.exists(iris_1_install):
        os.rename(os.path.join(os.path.expanduser('~'), '.iris'), os.path.join(os.path.expanduser('~'), '.iris_old'))

    # TBD: what to do with previous Iris 2.0 folder
    old_iris_2_install = os.path.join(os.path.expanduser('~'), '.iris2')
    logger.debug('Old Iris 2 install exists: %s' % os.path.exists(old_iris_2_install))


def exit_iris(message, status=0):
    if status == 0:
        logger.info(message)
    elif status == 1:
        logger.error(message)
    else:
        logger.debug(message)
    delete(PathManager.get_run_id(), update_run_file=False)
    ShutdownTasks.at_exit()
    exit(status)


class ShutdownTasks(CleanUp):
    """Class for restoring system state when Iris has been quit.
    """

    @staticmethod
    def at_exit():
        reset_terminal_encoding()

        if os.path.exists(PathManager.get_temp_dir()):
            shutil.rmtree(PathManager.get_temp_dir(), ignore_errors=True)

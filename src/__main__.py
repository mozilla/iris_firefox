# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import importlib
import logging
import os
import shutil
from distutils.dir_util import copy_tree

import pytest
from mozrunner import FirefoxRunner

from src.configuration.config_parser import validate_config_ini
from src.control_center.commands import delete
from src.core.api.keyboard.key import KeyModifier
from src.core.api.keyboard.keyboard import type
from src.core.api.keyboard.keyboard_util import check_keyboard_state
from src.core.api.os_helpers import OSHelper
from src.core.util.cleanup import *
from src.core.util.app_loader import get_app_test_directory
from src.core.util.arg_parser import get_core_args, set_core_arg
from src.core.util.json_utils import create_target_json
from src.core.util.local_web_server import LocalWebServer
from src.core.util.logger_manager import initialize_logger
from src.core.util.path_manager import PathManager
from src.core.util.system import check_7zip, fix_terminal_encoding, init_tesseract_path, reset_terminal_encoding, get_python_version

logger = logging.getLogger(__name__)


def main():
    args = get_core_args()
    initialize_logger()
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
                    logger.info('No tests chosen, closing Iris.')
                    delete(PathManager.get_run_id(), update_run_file=False)
                    ShutdownTasks.at_exit()
                    exit(0)

                pytest_args = user_result['tests']

                # Extract target from response and update core arg for application/target
                set_core_arg('application', user_result['target'])

                # Extract settings from response
                args = get_core_args()
                settings = user_result['args']
            else:
                # User cancelled or otherwise failed to select tests,
                # so we will shut down Iris.
                delete(PathManager.get_run_id(), update_run_file=False)
                ShutdownTasks.at_exit()
                exit(0)

        try:
            target_plugin = get_target(args.application)
            if settings is not None:
                logger.debug('Passing settings to target: %s' % settings)
                target_plugin.update_settings(settings)
            if pytest_args is None:
                pytest_args = get_test_params()
            pytest_args.append('-vs')
            pytest_args.append('-r ')
            pytest_args.append('-s')
            initialize_platform(args)
            pytest.main(pytest_args, plugins=[target_plugin])
        except ImportError:
            logger.error('Could not load plugin for {} application'.format(args.application))
            exit(1)
    else:
        logger.error('Failed platform verification.')
        exit(1)


def show_control_center():
    # TODO
    # expand logic to display Control Center only when no target specified,
    # or if -k argument is explicitly used
    if get_core_args().control:
        return True
    else:
        return False


def get_target(target_name):
    logger.info('Desired target: %s' % target_name)
    try:
        my_module = importlib.import_module('targets.%s.app' % target_name)
        logger.info('1')
        try:
            target_plugin = my_module.Target()
            logger.info('2')
            logger.info('Found target named %s' % target_plugin.target_name)
            return target_plugin
        except NameError:
            logger.error('Can\'t find default Target class.')
            exit(1)
    except ImportError as e:
        if e.name.__contains__('Xlib') and not OSHelper.is_linux():
            pass
        else:
            logger.error('Problems importing module:\n%s' % e)
            exit(1)


def initialize_platform(args):
    init()
    fix_terminal_encoding()
    PathManager.create_working_directory(args.workdir)
    PathManager.create_run_directory()


def get_test_params():
    tests_to_execute = get_app_test_directory()
    pytest_args = []

    if len(tests_to_execute) > 0:
        for running in tests_to_execute:
            pytest_args.append(running)
    else:
        exit(1)

    return pytest_args


def verify_config(args):
    """Checks keyboard state is correct, and that Tesseract and 7zip are installed."""
    
    # TODO:
    # once issues #76 and #163 are addressed, we can enable this check.
    '''
    if OSHelper.get_os().value is 'win':
        if get_python_version() is not '3.5.3':
            logger.error('Iris 2.0 does not run on versions of Python above 3.5.3')
            logger.error('at the moment due to compatibility issues.')
            logger.info('Shutting down.')
            exit(1)
    '''
    try:
        if not all([check_keyboard_state(args.no_check), init_tesseract_path(), check_7zip()]):
            exit(1)
    except KeyboardInterrupt:
        exit(1)
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
    fx_runner = FirefoxRunner(binary=fx_path, profile=profile_path, cmdargs=args, process_args=process_args)
    fx_runner.start()
    server = LocalWebServer(get_core_args().workdir, get_core_args().port)
    server.stop()

    if OSHelper.is_mac():
        type(text='q', modifier=KeyModifier.CMD)
    elif OSHelper.is_windows():
        type(text='w', modifier=[KeyModifier.CTRL, KeyModifier.SHIFT])
    else:
        type(text='q', modifier=KeyModifier.CTRL)

    try:
        fx_runner.stop()
    except Exception as e:
        logger.debug('Error stopping fx_runner')
        logger.debug(e)

    return server.result


class ShutdownTasks(CleanUp):
    """Class for restoring system state when Iris has been quit.
    """

    @staticmethod
    def at_exit():
        reset_terminal_encoding()

        if os.path.exists(PathManager.get_temp_dir()):
            shutil.rmtree(PathManager.get_temp_dir(), ignore_errors=True)

        if os.path.exists(os.path.join(get_core_args().workdir, 'cc_profile')):
            shutil.rmtree(os.path.join(get_core_args().workdir, 'cc_profile'), ignore_errors = True)

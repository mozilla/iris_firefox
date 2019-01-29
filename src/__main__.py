# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import importlib

import pytest

from src.core.api.arg_parser import parse_args
from src.core.api.keyboard.keyboard_api import check_keyboard_state
from src.core.util.app_loader import get_app_test_directory
from src.core.util.system import check_7zip, init_tesseract_path
from src.iris_pytest_plugin import Plugin
from src.core.util.path_manager import PathManager


def main():
    args = parse_args()
    target_plugin = get_target(args.application)
    pytest_args = get_test_params(args.application)

    initialize_platform()

    if verify_config(args):
        pytest.main(pytest_args, plugins=[target_plugin, Plugin()])
    else:
        print('Failed platform verification.')
        exit(1)


def get_target(target_name):
    print('Desired target: %s' % target_name)

    try:
        my_module = importlib.import_module('targets.%s.app' % target_name)
        try:
            target_plugin = my_module.Target()
            print('Found target named %s' % target_plugin.target_name)
            return target_plugin
        except NameError:
            print('Can\'t find default Target class.')
            exit(1)
    except ModuleNotFoundError:
        print('Problems importing module.')
        exit(1)


def initialize_platform():
    PathManager.create_target_directory()


def get_test_params(target):
    tests_to_execute = get_app_test_directory(target)
    pytest_args = []

    if tests_to_execute['running']:
        for running in tests_to_execute['running']:
            pytest_args.append(running)

    if tests_to_execute['excluded']:
        for excluded in tests_to_execute['excluded']:
            pytest_args.append('--ignore={}'.format(excluded))

    pytest_args.append('-vs')
    pytest_args.append('-r ')
    pytest_args.append('-s')
    return pytest_args


def verify_config(args):
    """Checks keyboard state is correct or if Tesseract and 7zip are installed."""

    # Disabling until we fix these methods
    """
    try:
        if not all([check_keyboard_state(args.no_check), init_tesseract_path(), check_7zip()]):
            exit(1)
    except KeyboardInterrupt:
        exit(1)
    return True
    """

    # The check_keyboard_state function has this error (Mac):
    """
      File "/iris2/src/core/api/keyboard/key.py", line 210, in is_lock_on
        if processed_lock_key in line:
      TypeError: a bytes-like object is required, not 'str'
    """

    # Return True until fixed
    return True

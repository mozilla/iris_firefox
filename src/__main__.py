# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import importlib

import pytest

from src.core.api.arg_parser import parse_args
from src.core.util.app_loader import get_app_test_directory
from src.iris_pytest_plugin import Plugin


def main():
    args = parse_args()
    tests_to_execute = get_app_test_directory(args.application)
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

    print('Desired target: %s' % args.application)

    try:
        my_module = importlib.import_module('targets.%s.app' % args.application)
    except ModuleNotFoundError:
        print('Module not found')
        return

    try:
        target_plugin = my_module.Target()
        print('Found target named %s' % target_plugin.target_name)
    except NameError:
        print('Can\'t find default Target class.')
        return

    pytest.main(pytest_args, plugins=[target_plugin, Plugin()])

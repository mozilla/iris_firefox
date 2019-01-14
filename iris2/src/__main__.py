# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


import pytest

from iris2.src.core.api.app_loader import get_app_test_directory
from iris2.src.core.api.arg_parser import parse_args
from iris2.src.iris_pytest_plugin import Plugin


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

    pytest.main(pytest_args, plugins=[Plugin()])

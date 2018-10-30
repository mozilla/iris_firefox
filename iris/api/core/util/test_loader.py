# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import sys

import logging

from iris.api.core.util.core_helper import IrisCore
from iris.api.core.util.parse_args import parse_args

logger = logging.getLogger(__name__)


def get_tests_from_text_file(file_name):
    test_list = []
    test_packages = []

    if os.path.isfile(file_name):
        logger.debug('"%s" found. Proceeding ...' % file_name)
        with open(file_name, 'r') as f:
            test_paths_list = [line.strip() for line in f]
        if len(test_paths_list) == 0:
            logger.error('"%s" does not contain any valid test paths. Exiting program ...' % str(file_name))
            return test_list, test_packages
        logger.debug('Tests found in the test suite file:\n\n%s\n' % '\n'.join(map(str, test_paths_list)))
        logger.debug('Validating test paths ...')
        for test_path in test_paths_list:
            if os.path.isfile(test_path):
                logger.debug('"%s" is a valid test path. Proceeding ...' % test_path)
                test_list.append(os.path.splitext(os.path.basename(test_path))[0])
                test_packages.append(os.path.dirname(test_path))
            else:
                logger.warning('"%s" is not a valid test path. Skipping ...' % test_path)

        if len(test_list) == 0:
            logger.error('"%s" does not contain any valid test paths. Exiting program ...' % str(file_name))
            return test_list, test_packages
    else:
        logger.error('Could not locate "%s" . Exiting program ...', str(file_name))
        return test_list, test_packages
    logger.debug('List of tests to execute: [%s]' % ', '.join(map(str, test_list)))
    return test_list, test_packages


def get_tests_from_list(master_test_list):
    test_list = []
    test_packages = []

    for name in parse_args().test.split(','):
        if '.py' in name:
            name = name.split('.py')[0]
        name = name.strip()
        for package in master_test_list:
            for test in master_test_list[package]:
                if name == test['name']:
                    test_list.append(name)
                    if package not in test_packages:
                        test_packages.append(package)
        if name not in test_list:
            logger.warning('Could not locate test: %s' % name)

    if len(test_list) == 0:
        logger.error('No tests to run. Exiting program ...')
    return test_list, test_packages


def get_tests_from_directory(master_test_list):
    test_list = []
    test_packages = []

    tests, packages = scan_all_tests()
    for name in tests:
        if '.py' in name:
            name = name.split('.py')[0]
        name = name.strip()
        for package in master_test_list:
            for test in master_test_list[package]:
                if name == test['name']:
                    test_list.append(name)
                    if package not in test_packages:
                        test_packages.append(package)
        if name not in test_list:
            logger.warning('Could not locate test: %s' % name)

    if len(test_list) == 0:
        logger.error('No tests to run. Exiting program ...')
    return test_list, test_packages


def get_tests_from_package(master_test_list):
    test_list = []
    test_packages = [str(item).strip() for item in parse_args().directory.split(',')]
    for package in test_packages:
        try:
            if master_test_list[package]:
                for test in master_test_list[package]:
                    test_list.append(test["name"])
        except KeyError:
            logger.warning('Could not locate %s' % package)
    if len(test_list) == 0:
        logger.debug('No tests associated with package(s): %s' % test_packages)
    return test_list, test_packages


def sorted_walk(directory, topdown=True, onerror=None):
    names = os.listdir(directory)
    names.sort()
    dirs, nondirs = [], []

    for name in names:
        if os.path.isdir(os.path.join(directory, name)):
            dirs.append(name)
        else:
            nondirs.append(name)

    if topdown:
        yield directory, dirs, nondirs
    for name in dirs:
        path = os.path.join(directory, name)
        if not os.path.islink(path):
            for x in sorted_walk(path, topdown, onerror):
                yield x
    if not topdown:
        yield directory, dirs, nondirs


def scan_all_tests():
    test_list = []
    test_packages = []

    tests_directory = IrisCore.get_tests_dir()
    logger.debug('Path %s found. Checking content ...', tests_directory)

    for dir_path, sub_dirs, all_files in sorted_walk(tests_directory):
        for current_file in all_files:
            if current_file.endswith('.py') and not current_file.startswith('__'):
                test_list.append(os.path.splitext(current_file)[0])
                if dir_path not in test_packages:
                    test_packages.append(dir_path)

    if len(test_list) == 0:
        logger.error('Directory %s does not contain test files. Exiting program ...' % tests_directory)
        return test_list, test_packages
    else:
        logger.debug('Test packages: %s', test_packages)
        logger.debug('List of all tests found: [%s]' % ', '.join(map(str, test_list)))
        for package in test_packages:
            sys.path.append(package)
        return test_list, test_packages


def get_excluded_tests_list(master_test_list):
    args = parse_args()
    if args.exclude:
        exclude_list = [str(item).strip() for item in args.exclude.split(',')]
        logger.debug('Processing exclude list: %s' % ''.join(exclude_list))

        test_list = []
        for item in exclude_list:
            try:
                for test in master_test_list[item]:
                    test_list.append(test["name"])
            except KeyError:
                logger.debug('Could not find package: %s' % item)

        exclude_list += test_list
        return exclude_list
    return []


def load_tests(master_test_list):
    """Test loading

    Test loading is done by providing a list of test names separated by comma, a path to a file containing a custom list
    of tests or a directory. The provided list of test names can be with or without .py extension.

    The path to the file that contains the list of tests should have .txt extension. The full path is needed. For
    example: '/Users/user_name/full_path/test_suite.txt'. The content of the file should be a simple line-delimited list
    of test paths (full path required including file extensions).
    """

    temp_test_list_1 = []
    temp_test_packages_1 = []
    temp_test_list_2 = []
    temp_test_packages_2 = []

    args = parse_args()

    if args.rerun:
        path = os.path.join(args.workdir, 'runs', 'last_fail.txt')
        args.test = path
        logger.info('Re-running failed tests from previous run.')

    if args.test:
        if args.test.endswith('.txt'):
            logger.debug('Loading tests from text file: %s' % args.test)
            temp_test_list_1, temp_test_packages_1 = get_tests_from_text_file(args.test)
        else:
            logger.debug('Loading tests from list.')
            temp_test_list_1, temp_test_packages_1 = get_tests_from_list(master_test_list)

    if args.directory:
        if not os.path.exists(args.directory):
            logger.debug('Loading tests from packages.')
            temp_test_list_2, temp_test_packages_2 = get_tests_from_package(master_test_list)
        elif not args.test:
            logger.debug('Loading tests from directory: %s' % args.directory)
            temp_test_list_2, temp_test_packages_2 = get_tests_from_directory(master_test_list)

    test_list = temp_test_list_1 + temp_test_list_2
    test_packages = temp_test_packages_1 + temp_test_packages_2

    exclude_tests = get_excluded_tests_list(master_test_list)

    for item in exclude_tests:
        try:
            test_list.remove(item)
        except ValueError:
            logger.debug('Excluded item not found in test list: %s' % item)

    logger.debug('Found tests: %s' % ''.join(test_list))
    logger.debug('Found packages: %s' % ''.join(test_packages))

    return test_list, test_packages

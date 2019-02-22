import importlib
import logging
import os
import sys

logger = logging.getLogger(__name__)
from src.core.util.path_manager import PathManager


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


def get_targets():
    targets = []
    tests_directory = PathManager.get_tests_dir()
    for dir in os.listdir(tests_directory):
        if not dir.startswith('__') or dir.startswith('.'):
            targets.append(dir)

    return targets


def scan_all_tests():
    test_list = []
    test_packages = []

    tests_directory = PathManager.get_tests_dir()
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

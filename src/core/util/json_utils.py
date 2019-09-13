# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from datetime import datetime
import importlib
import json
import logging
import os
import sys
import time

import git
import pytest

from src.core.api.os_helpers import OSHelper
from src.core.util.arg_parser import get_core_args
from src.core.util.path_manager import PathManager
from src.core.util.system import get_python_version

logger = logging.getLogger(__name__)
args = get_core_args()


def create_target_json():
    if not use_cached_target_file():
        logging.info('Preparing data for the Control Center.')
        logging.info('This may take a minute.')
        master_target_dir = os.path.join(PathManager.get_module_dir(), 'targets')
        target_list = [f for f in os.listdir(master_target_dir) if not f.startswith('__') and not f.startswith('.')]

        targets = []
        for item in target_list:
            try:
                target_tests = scan_all_tests(item)
                target_module = importlib.import_module('targets.%s.main' % item)
                try:
                    target = target_module.Target()
                    targets.append({'name': target.target_name, 'tests': target_tests, 'icon': '%s.png' % item,
                                    'settings': target.cc_settings})
                except NameError:
                    logger.error('Can\'t find default Target class.')
            except ImportError as e:
                logger.error('Problems importing module \'%s\':\n%s' % (item, e))

        target_json = {'targets': targets}
        target_json_file = os.path.join(args.workdir, 'data', 'targets.json')
        with open(target_json_file, 'w') as f:
            json.dump(target_json, f, sort_keys=True, indent=True)


def update_run_index(app, finished=False):
    if finished:
        failed = 0
        total_duration = 0
        for test in app.completed_tests:
            if test.outcome == 'FAILED' or test.outcome == 'ERROR':
                failed = failed + 1
            total_duration = total_duration + test.test_duration

        current_run = {'duration': total_duration,
                       'failed': failed,
                       'id': PathManager.get_run_id(),
                       'locale': args.locale,
                       'target': args.target,
                       'total': len(app.completed_tests)}
    else:
        current_run = {'duration': '-1',
                       'failed': '-1',
                       'id': PathManager.get_run_id(),
                       'locale': args.locale,
                       'target': args.target,
                       'total': '-1'}

    run_file = os.path.join(args.workdir, 'data', 'runs.json')

    if os.path.exists(run_file):
        logger.debug('Updating run file: %s' % run_file)
        with open(run_file, 'r') as f:
            run_file_data = json.load(f)
        for run in run_file_data['runs']:
            if run['id'] == PathManager.get_run_id():
                run_file_data['runs'].remove(run)
        run_file_data['runs'].append(current_run)
    else:
        logger.debug('Creating run file: %s' % run_file)
        run_file_data = {'runs': []}
        run_file_data['runs'].append(current_run)

    with open(run_file, 'w') as f:
        json.dump(run_file_data, f, sort_keys=True, indent=True)
        f.close()


def create_run_log(app):
    args = get_core_args()
    meta = {'run_id': PathManager.get_run_id(),
            'platform': OSHelper.get_os().value,
            'config': '%s, %s-bit, %s' % (OSHelper.get_os_version(), OSHelper.get_os_bits(),
                                          OSHelper.get_processor()),
            'locale': args.locale,
            'args': ' '.join(sys.argv),
            'params': vars(args),
            'log': os.path.join(PathManager.get_current_run_dir(), 'iris_log.log')}
    values = {}
    for i in app.values:
        values[i] = app.values[i]
    meta['values'] = values

    meta['iris_version'] = 2.0
    try:
        repo = git.Repo(PathManager.get_module_dir())
        meta['iris_repo'] = repo.working_tree_dir
        try:
            meta['iris_branch'] = repo.active_branch.name
        except:
            # If we're on a detached head, the active_branch is
            # undefined and raises an exception. This at least
            # allows the test run to finish
            meta['iris_branch'] = "detached"
        meta['iris_branch_head'] = repo.head.object.hexsha
    except:
        # Iris is not running in a Git repo, so don't try to
        # report on non-existent data.
        meta['iris_repo'] = 'n/a'
        meta['iris_branch'] = 'n/a'
        meta['iris_branch_head'] = 'n/a'

    meta['python_version'] = get_python_version()

    failed = 0
    passed = 0
    skipped = 0
    errors = 0

    for test in app.completed_tests:
        if test.outcome == 'FAILED':
            failed = failed + 1
        if test.outcome == 'PASSED':
            passed = passed + 1
        if test.outcome == 'SKIPPED':
            skipped = skipped + 1
        if test.outcome == 'ERROR':
            errors = errors + 1

    logger.debug('Updating run.json with completed run data.')
    meta['total'] = len(app.completed_tests)
    meta['passed'] = passed
    meta['failed'] = failed
    meta['skipped'] = skipped
    meta['errors'] = errors
    meta['start_time'] = app.start_time
    meta['end_time'] = app.end_time
    meta['total_time'] = app.end_time - app.start_time

    tests = {'all_tests': convert_test_list(app.completed_tests),
             'failed_tests': convert_test_list(app.completed_tests, only_failures=True)}

    run_file = os.path.join(PathManager.get_current_run_dir(), 'run.json')
    run_file_data = {'meta': meta, 'tests': tests}

    with open(run_file, 'w') as f:
        json.dump(run_file_data, f, sort_keys=True, indent=True)


def convert_test_list(test_list, only_failures=False):
    """Takes a flat list of test objects and paths and converts to an object that can be serialized as JSON.

    :param test_list: List of completed tests
    :param only_failures: If True, only return failed tests
    :return:
    """
    test_root = os.path.join(PathManager.get_module_dir(), 'tests')
    tests = []
    for test in test_list:
        test_failed = True if 'FAILED' in test.outcome or 'ERROR' in test.outcome else False
        original_path = str(test.item.__dict__.get('fspath'))
        target_root = original_path.split(test_root)[1]
        target = target_root.split(os.sep)[1]
        test_path = target_root.split('%s%s%s' % (os.sep, target, os.sep))[1]
        parent = tests
        details = get_test_markers(test.item)
        for module in test_path.split(os.sep):
            test_obj = {'name': module.split('.py')[0]}
            if 'py' not in module:
                module_exists = False
                for objects in parent:
                    if objects['name'] == module:
                        parent = objects['children']
                        module_exists = True
                        break
                if not module_exists:
                    new_parent = test_obj['children'] = []
                    if only_failures and test_failed:
                        parent.append(test_obj)
                    elif not only_failures:
                        parent.append(test_obj)
                    parent = new_parent
            else:
                if test_failed:
                    test_assert = {
                        'error': test.error.lstrip(), 'message': test.message.lstrip(), 'call_stack': test.traceback + '\n\n ',
                        'code': get_failing_code(test.node_name, int(test.line))
                    }
                    test_obj['assert'] = test_assert
                test_obj['result'] = test.outcome
                test_obj['time'] = test.test_duration
                debug_image_directory = os.path.join(PathManager.get_current_run_dir(), test_path.split('.py')[0],
                                                     'debug_images')
                test_obj['debug_image_directory'] = debug_image_directory
                test_obj['debug_images'] = get_image_names(debug_image_directory)
                test_obj['description'] = details.get('description')

                values = {}
                for i in details:
                    if i != 'description':
                        values[i] = details.get(i)
                test_obj['values'] = values
                if only_failures and test_failed:
                    parent.append(test_obj)
                elif not only_failures:
                    parent.append(test_obj)
                parent = tests
    return tests


def get_image_names(path):
    images = []
    if os.path.exists(path):
        for root, dirs, files in os.walk(path):
            for file_name in files:
                images.append(file_name)
    images.sort()
    return images


def get_failing_code(file, line):
    f = open(file, 'rb').readlines()
    lines = []
    num_lines = 10
    if len(f) < num_lines:
        num_lines = len(f)
    for x in range(int(line) - 1, int(line) - (num_lines + 1), -1):
        lines.append('%s: %s' % (x + 1, f[x].decode('utf-8')))
    lines.reverse()
    lines.append('\n')
    return ''.join(lines)


def get_test_markers(item):
    details = {}
    for marker in item.iter_markers(name="details"):
        for arg in marker.kwargs:
            details[arg] = marker.kwargs[arg]
    return details


def scan_all_tests(target):
    logging.info('Gathering test info for \'%s\'...' % target)
    master_test_root = os.path.join(PathManager.get_module_dir(), 'tests')
    test_root = os.path.join(master_test_root, target)
    base_props = ['description']
    tests = []

    my_plugin = TestCollector()
    pytest.main(['--collect-only', '-s', '-p', 'no:terminal', test_root], plugins=[my_plugin])

    for test in my_plugin.get_collected_items():
        original_path = str(test.__dict__.get('fspath'))
        target_root = original_path.split(master_test_root)[1]
        test_path = target_root.split('%s%s%s' % (os.sep, target, os.sep))[1]
        parent = tests
        details = get_test_markers(test)
        for module in test_path.split(os.sep):
            test_obj = {'name': module.split('.py')[0]}
            if 'py' not in module:
                module_exists = False
                for objects in parent:
                    if objects['name'] == module:
                        parent = objects['children']
                        module_exists = True
                        break
                if not module_exists:
                    new_parent = test_obj['children'] = []
                    parent.append(test_obj)
                    parent = new_parent
            else:
                for prop in base_props:
                    if details.get(prop) is not None:
                        test_obj[prop] = details.get(prop)
                    else:
                        test_obj[prop] = ''
                test_obj['file'] = original_path
                values = {}
                for i in details:
                    if i not in base_props:
                        values[i] = details.get(i)
                if details.get('platform') is None:
                    values['platform'] = 'all'
                if details.get('locale') is None:
                    values['locale'] = 'all'
                test_obj['values'] = values
                parent.append(test_obj)
                parent = tests
    return tests

def use_cached_target_file():
    """
    Helper function to determine if target.json is relatively recent and can be re-used.
    :return: True/False
    """
    # We will cache the target file for t5 minutes - adjust below if desired.
    cache_time = 60 * 15

    result = False
    target_json_file = os.path.join(args.workdir, 'data', 'targets.json')
    if os.path.exists(target_json_file):
        file_modified_time = int(os.path.getmtime(target_json_file))
        logger.debug('Target file created: %s' % file_modified_time)
        current_time = int(time.mktime(datetime.now().timetuple()))
        logger.debug('Current time: %s' % current_time)
        elapsed_time = current_time - file_modified_time
        logger.debug('Elapsed time: %s' % elapsed_time)
        if elapsed_time < cache_time:
            result = True
    return result

class TestCollector:

    def __init__(self):
        self.collected = []

    def pytest_collection_modifyitems(self, items):
        for item in items:
            self.collected.append(item)

    def get_collected_items(self):
        return self.collected

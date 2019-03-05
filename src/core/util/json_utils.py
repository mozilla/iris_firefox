# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
import inspect
import os
import sys

import git
import importlib
import json
import logging
import shutil

from src.core.api.os_helpers import OSHelper
from src.core.util.arg_parser import parse_args
from src.core.util.path_manager import PathManager
from src.core.util.test_loader import scan_all_tests

logger = logging.getLogger(__name__)


def update_run_index(app, finished=False):
    if finished:
        failed = 0
        total_duration = 0

        for test in app.completed_tests:
            if test.outcome == 'FAILED':
                failed = failed + 1
            total_duration = total_duration + test.test_duration

        current_run = {'duration': total_duration,
                       'failed': failed,
                       'id': PathManager.get_run_id(),
                       'locale': app.locale,
                       'target': parse_args().application,
                       'total': len(app.completed_tests)}
    else:
        current_run = {'duration': '-1',
                       'failed': '-1',
                       'id': PathManager.get_run_id(),
                       'locale': app.locale,
                       'target': parse_args().application,
                       'total': '-1'}

    run_file = os.path.join(parse_args().workdir, 'data', 'runs.json')

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


def update_run_log(fx_app, new_data=None):
    meta = {'run_id': PathManager.get_run_id(),
            'fx_version': fx_app.version,
            'fx_build_id': fx_app.build_id,
            'platform': OSHelper.get_os(),
            'config': '%s, %s-bit, %s' % (OSHelper.get_os, OSHelper.get_os_bits(),
                                          OSHelper.get_processor()),
            'channel': fx_app.channel,
            'locale': fx_app.locale,
            'args': ' '.join(sys.argv),
            'params': vars(parse_args()),
            'log': os.path.join(PathManager.get_current_run_dir(), 'iris_log.log')}

    repo = git.Repo(PathManager.get_module_dir())
    meta['iris_version'] = 1.0
    meta['iris_repo'] = repo.working_tree_dir
    if parse_args().headless_run:
        pass
    else:
        meta['iris_branch'] = repo.active_branch.name
        meta['iris_branch_head'] = repo.head.object.hexsha

    if new_data is None:
        logger.debug('Updating run.json with initial run data.')
        meta['total'] = 0
        meta['passed'] = 0
        meta['failed'] = 0
        meta['skipped'] = 0
        meta['errors'] = 0
        meta['start_time'] = 0
        meta['end_time'] = 0
        meta['total_time'] = 0
        tests = []
    else:
        logger.debug('Updating runs.json with completed run data.')
        meta['total'] = new_data['total']
        meta['passed'] = new_data['passed']
        meta['failed'] = new_data['failed']
        meta['failed_tests'] = new_data['failed_tests']
        meta['skipped'] = new_data['skipped']
        meta['errors'] = new_data['errors']
        meta['start_time'] = new_data['start_time']
        meta['end_time'] = new_data['end_time']
        meta['total_time'] = new_data['total_time']
        tests = new_data['tests']

    run_file = os.path.join(PathManager.get_current_run_dir(), 'run.json')
    run_file_data = {'meta': meta, 'tests': tests}
    with open(run_file, 'w') as f:
        json.dump(run_file_data, f, sort_keys=True, indent=True)


def create_arg_json():
    arg_data = {'email': {'type': 'bool', 'value': ['true', 'false'], 'default': 'false', 'label': 'Email results'},
                'firefox': {'type': 'str', 'value': ['local', 'latest', 'latest-esr', 'latest-beta', 'nightly'],
                            'default': 'latest-beta', 'label': 'Firefox'},
                'highlight': {'type': 'bool', 'value': ['true', 'false'], 'default': 'false',
                              'label': 'Debug using highlighting'},
                'locale': {'type': 'str', 'value': 'en-US', 'default': 'en-US', 'label': 'Locale'},
                'mouse': {'type': 'float', 'value': ['0.0', '0.5', '1.0', '2.0'], 'default': '0.5',
                          'label': 'Mouse speed'},
                'override': {'type': 'bool', 'value': ['true', 'false'], 'default': 'false',
                             'label': 'Run disabled tests'},
                'port': {'type': 'int', 'value': ['2000'], 'default': '2000', 'label': 'Local web server port'},
                'report': {'type': 'bool', 'value': ['true', 'false'], 'default': 'false',
                           'label': 'Create TestRail report'},
                'save': {'type': 'bool', 'value': ['true', 'false'], 'default': 'false',
                         'label': 'Save profiles to disk'}}

    arg_log_file = os.path.join(parse_args().workdir, 'data', 'all_args.json')
    with open(arg_log_file, 'w') as f:
        json.dump(arg_data, f, sort_keys=True, indent=True)


def create_target_json():
    master_target_dir = os.path.join(PathManager.get_module_dir(), 'targets')
    target_list = [f for f in os.listdir(master_target_dir) if not f.startswith('__') and not f.startswith('.')]

    master_test_list = scan_all_tests()
    tests=master_test_list['tests']

    targets = []
    for item in target_list:
        try:
            app_tests=tests[item]
            target_module = importlib.import_module('targets.%s.app' % item)
            try:
                target = target_module.Target()
                targets.append({'name': target.target_name, 'tests': app_tests, 'icon': '%s.png' % item,
                                'settings': target.cc_settings})
            except NameError:
                logger.error('Can\'t find default Target class.')
        except ModuleNotFoundError:
            logger.error('Problems importing module.')

    target_json = {'targets': targets}
    # print('Target Json is :',target_json)
    target_json_file = os.path.join(parse_args().workdir, 'data', 'targets.json')
    with open(target_json_file, 'w') as f:
        json.dump(target_json, f, sort_keys=True, indent=True)



def create_test_json(master_test_list):
    test_log_file = os.path.join(parse_args().workdir, 'data', 'all_tests.json')
    with open(test_log_file, 'w') as f:
        json.dump(master_test_list, f, sort_keys=True, indent=True)


def filter_list(original_list, exclude_list):
    new_list = []
    for item in original_list:
        if item not in exclude_list:
            new_list.append(item)
    return new_list



def create_log_object(module, current, fx_args):
    run_obj = {'name': module.__name__, 'meta': current.meta, 'profile': current.profile, 'module': module.__file__,
               'profile_path': current.profile_path.profile, 'fx_args': fx_args, 'prefs': current.prefs,
               'time': int(current.end_time - current.start_time), 'asserts': []}

    outcome = 'PASSED'
    for result in current.results:
        if result.outcome is 'FAILED':
            outcome = result.outcome
        run_obj['asserts'].append({'outcome': result.outcome, 'message': result.message,
                                   'expected': result.expected, 'actual': result.actual,
                                   'error': result.error})
        run_obj['result'] = outcome
    return run_obj


def update_log_object(run_obj):
    if os.path.exists(PathManager.get_debug_image_directory()):
        debug_images = []
        for root, dirs, files in os.walk(PathManager.get_debug_image_directory()):
            for file_name in files:
                debug_images.append(file_name)
        run_obj['debug_images'] = sorted(debug_images)
        run_obj['debug_image_directory'] = PathManager.get_debug_image_directory()
    return run_obj


def append_logs(browser, test_list, master_test_list, passed, failed, skipped, errors, start_time, end_time, tests):
    update_run_index(browser, {'total': len(test_list), 'failed': len(failed)})
    failed_tests = {}
    if len(failed) > 0:
        for item in failed:
            for package in master_test_list:
                for test in master_test_list[package]:
                    if test["name"] == item:
                        if failed_tests.get(package) is None:
                            failed_tests[package] = []
                        failed_tests[package].append(item)

    data = {'total': len(test_list), 'passed': passed, 'failed': len(failed),
            'failed_tests': failed_tests, 'skipped': skipped, 'errors': errors,
            'start_time': int(start_time), 'end_time': int(end_time),
            'total_time': int(round(end_time - start_time, 2)), 'tests': tests}
    update_run_log(browser, data)

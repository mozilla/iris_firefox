# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import sys
from distutils import dir_util

import logging
import shutil
from multiprocessing import Process

from api.core.key import check_keyboard_state
from api.core.platform import Platform
from api.core.settings import Settings
from api.core.util.core_helper import IrisCore
from api.core.util.json_utils import create_master_test_list, create_test_json, create_arg_json
from api.core.util.logger_manager import initialize_logger
from api.core.util.parse_args import parse_args
from api.core.util.test_loader import load_tests
from api.helpers.general import launch_firefox, quit_firefox
from firefox import cleanup
from firefox.firefox_app import FirefoxApp
from iris.firefox.firefox_app import get_local_firefox_path
from local_web_server import LocalWebServer
from test_runner import run

restore_terminal_encoding = None
logger = logging.getLogger(__name__)

process_list = []
master_test_list = create_master_test_list()


def main():
    initialize_platform()
    verify_config()
    run_iris()


def start_local_web_server(port):
    """
    Web servers are spawned in new Process instances, which
    must be saved in a list in order to be terminated later.
    """
    try:
        path = IrisCore.get_local_web_root()
        logger.debug('Starting local web server on port %s for directory %s' % (port, path))
        web_server_process = Process(target=LocalWebServer, args=(path, port,))
        process_list.append(web_server_process)
        web_server_process.start()
    except IOError:
        logger.critical('Unable to launch local web server, aborting Iris.')


def finish(code=0):
    """All exit points of Iris need to call this function in order to exit properly."""
    global process_list
    logger.debug('There are %s queued process(es) to terminate.' % len(process_list))
    for process in process_list:
        logger.debug('Terminating process.')
        process.terminate()
        process.join()
    sys.exit(code)


def initialize_platform():
    """Initialize platform.

    Fixes the terminal encoding, creating directories, Firefox profiles, report JSONs.
    """
    try:
        cleanup.init()
        fix_terminal_encoding()
        IrisCore.create_working_directory()
        IrisCore.create_run_directory()
        initialize_logger()
        IrisCore.create_profile_cache()
        create_test_json(master_test_list)
        create_arg_json()
    except KeyboardInterrupt:
        finish(1)


def verify_config():
    """Checks keyboard state is correct or if Tesseract and 7zip are installed."""
    try:
        if not all([check_keyboard_state(), IrisCore.init_tesseract_path(), IrisCore.check_7zip()]):
            finish(1)
    except KeyboardInterrupt:
        finish(1)


def run_iris():
    """Runs Iris."""
    use_control_center, tests_list = control_center()
    if use_control_center:
        start_local_web_server(parse_args().port)
        if tests_list is not None and len(tests_list) > 0:
            tests = tests_list
        else:
            tests, packages = load_tests(master_test_list)
            if len(tests) == 0:
                logger.error('Specified tests not found, aborting run.')
                finish(1)
        try:
            browser = FirefoxApp()
            run(master_test_list, tests, browser)
        except (ValueError, KeyboardInterrupt):
            finish(1)
    else:
        IrisCore.delete_run_directory()
        finish(0)


class RemoveTempDir(cleanup.CleanUp):
    """Class definition for cleanup helper responsible for deleting the temporary directory prior to exit."""

    @staticmethod
    def at_exit():
        tmp_dir = IrisCore.get_tempdir()
        if tmp_dir is not None:
            logger.debug('Removing temp dir "%s"' % tmp_dir)
            shutil.rmtree(tmp_dir, ignore_errors=True)


class ResetTerminalEncoding(cleanup.CleanUp):
    """Class for restoring original terminal encoding at exit."""

    @staticmethod
    def at_exit():
        global restore_terminal_encoding
        if restore_terminal_encoding is not None:
            set_terminal_encoding(restore_terminal_encoding)


class TerminateSubprocesses(cleanup.CleanUp):
    """Class for terminiting subprocesses, such as local web server instances."""

    @staticmethod
    def at_exit():
        global process_list
        logger.debug('There are %s queued process(es) to terminate.' % len(process_list))
        for process in process_list:
            logger.debug('Terminating process.')
            process.terminate()
            process.join()
        if Settings.is_mac():
            # Extra call to shutdown the program we use to check keyboard lock,
            # in case Iris was terminated abruptly.
            IrisCore.shutdown_process('Xquartz')


def get_terminal_encoding():
    """Helper function to get current terminal encoding."""
    if sys.platform.startswith(Platform.WINDOWS):
        logger.debug('Running "chcp" shell command')
        chcp_output = os.popen('chcp').read().strip()
        logger.debug('chcp output: "%s"' % chcp_output)
        if chcp_output.startswith('Active code page:'):
            codepage = chcp_output.split(': ')[1]
            logger.debug('Active codepage is "%s"' % codepage)
            return codepage
        else:
            logger.warning('There was an error detecting the active codepage')
            return None
    else:
        logger.debug('Platform does not require switching terminal encoding')
        return None


def set_terminal_encoding(encoding):
    """Helper function to set terminal encoding."""
    if os.path.exists('C:\\'):
        logger.debug('Running "chcp" shell command, setting codepage to "%s"', encoding)
        chcp_output = os.popen('chcp %s' % encoding).read().strip()
        logger.debug('chcp output: "%s"' % chcp_output)
        if chcp_output == 'Active code page: %s' % encoding:
            logger.debug('Successfully set codepage to "%s"' % encoding)
        else:
            logger.warning('Can\'t set codepage for terminal')


def fix_terminal_encoding():
    """Helper function to set terminal to platform-specific UTF encoding."""
    global restore_terminal_encoding
    restore_terminal_encoding = get_terminal_encoding()
    if restore_terminal_encoding is None:
        return
    if os.path.exists('C:\\'):
        platform_utf_encoding = '65001'
    else:
        platform_utf_encoding = None
    if restore_terminal_encoding != platform_utf_encoding:
        set_terminal_encoding(platform_utf_encoding)


def control_center():
    if len(sys.argv) > 1 and not parse_args().control:
        return True, None
    else:
        dir_util.copy_tree(os.path.join(IrisCore.get_module_dir(), 'iris', 'cc_files'), parse_args().workdir)
        profile_path = os.path.join(parse_args().workdir, 'cc_profile')

        fx_path = get_local_firefox_path()
        if fx_path is None:
            logger.error('Can\'t find local Firefox installation, aborting Iris run.')
            return False, None

        fx_runner = launch_firefox(fx_path, profile=profile_path, url=IrisCore.get_base_local_web_url())
        fx_runner.start()
        server = LocalWebServer(parse_args().workdir, parse_args().port)
        quit_firefox()
        status = fx_runner.process_handler.wait(Settings.FIREFOX_TIMEOUT)
        if status is None:
            logger.debug('Firefox did not quit. Executing force quit.')
            fx_runner.stop()

        if server.result == 'cancel':
            logger.info('Canceling Iris run.')
            return False, None
        else:
            logger.debug('Received data from control center: %s' % server.result)
            update_args_from_server(server)
            tests = sorted(server.result['tests'])
            test_packages = []
            test_list = []
            if len(tests):
                for package in tests:
                    test_packages.append(package)
                    for test in server.result['tests'][package]:
                        test_list.append(test['name'])
            return True, test_list


def update_args_from_server(server):
    if not hasattr(server, 'result'):
        return

    parse_args().locale = server.result['locale']
    parse_args().firefox = server.result['firefox']
    parse_args().override = server.result['override']
    parse_args().port = int(server.result['port'])
    parse_args().email = server.result['email']
    parse_args().highlight = server.result['highlight']
    parse_args().mouse = float(server.result['mouse'])
    parse_args().report = server.result['report']
    parse_args().save = server.result['save']
    Settings.move_mouse_delay = parse_args().mouse

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


import datetime
import logging
import os
import shutil
import tempfile

from core.arg_parser import parse_args
from core.helpers.os_helpers import OSHelper

logger = logging.getLogger(__name__)


def __create_tempdir():
    """Creates the temporary directory.
    Writes to the global variable tmp_dir
    :return:
         Path of temporary directory.
    """
    temp_dir = tempfile.mkdtemp(prefix='iris2_')
    logger.debug('Created temp dir "%s"' % temp_dir)
    return temp_dir


_tmp_dir = __create_tempdir()
_run_id = datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')
_current_module = os.path.join(os.path.expanduser('~'), 'temp', 'test')


class PathManager:

    @staticmethod
    def get_current_module():
        """Returns the name of the active test module."""
        return _current_module

    @staticmethod
    def parse_module_path():
        """Returns the parent directory and module name of the calling file."""
        delimiter = '\\' if '\\' in PathManager.get_current_module() else '/'
        temp = PathManager.get_current_module().split(delimiter)
        parent = temp[len(temp) - 2]
        test = temp[len(temp) - 1].split('.py')[0]
        return parent, test

    @staticmethod
    def set_current_module(module):
        """Sets the active module name."""
        global _current_module
        _current_module = module

    @staticmethod
    def get_module_dir():
        """Returns the path to the root of the local Iris repo."""
        return os.path.realpath(os.path.split(__file__)[0] + '/../../../..')

    @staticmethod
    def get_working_dir():
        """Returns the path to the root of the directory where local data is stored."""
        PathManager.create_working_directory()
        return parse_args().workdir

    @staticmethod
    def get_tests_dir():
        """Returns the directory where tests are located."""
        return os.path.join(PathManager.get_module_dir(), 'iris2', 'tests')

    @staticmethod
    def get_current_run_dir():
        """Returns the directory inside the working directory of the active run."""
        PathManager.create_run_directory()
        return os.path.join(parse_args().workdir, 'runs', PathManager.get_run_id())

    @staticmethod
    def get_log_file_path():
        """Returns the path to the log file."""
        path = PathManager.get_current_run_dir()
        if not os.path.exists(path):
            os.mkdir(path)
        return os.path.join(path, 'iris_log.log')

    @staticmethod
    def create_test_output_dir():
        """Creates directories inside the current run directory for test output."""
        parent, test = PathManager.parse_module_path()
        parent_directory = os.path.join(PathManager.get_current_run_dir(), parent)
        if not os.path.exists(parent_directory):
            os.makedirs(parent_directory)
        test_directory = os.path.join(parent_directory, test)
        os.mkdir(test_directory)
        return test_directory

    @staticmethod
    def get_image_debug_path():
        """Returns the root directory where a test's debug images are located."""
        parent, test = PathManager.parse_module_path()
        path = os.path.join(parse_args().workdir, 'runs', PathManager.get_run_id(), parent, test, 'debug_images')
        return path

    @staticmethod
    def get_tempdir():
        """Returns temporary directory path."""
        return _tmp_dir

    @staticmethod
    def get_run_id():
        """Returns run id based on timestamp."""
        return _run_id

    @staticmethod
    def get_images_path():
        """Returns images directory path."""
        return os.path.join('images', OSHelper.get_os().value)

    @staticmethod
    def delete_run_directory():
        """Removes run directory."""
        master_run_directory = os.path.join(parse_args().workdir, 'runs')
        run_directory = os.path.join(master_run_directory, PathManager.get_run_id())
        if os.path.exists(run_directory):
            shutil.rmtree(run_directory, ignore_errors=True)

    @staticmethod
    def create_run_directory():
        """Creates run directory."""
        PathManager.create_working_directory()
        master_run_directory = os.path.join(parse_args().workdir, 'runs')
        if not os.path.exists(master_run_directory):
            os.mkdir(master_run_directory)
        run_directory = os.path.join(master_run_directory, PathManager.get_run_id())
        if not os.path.exists(run_directory):
            os.mkdir(run_directory)

    @staticmethod
    def create_working_directory():
        """Creates working directory."""
        work_dir = parse_args().workdir
        if not os.path.exists(work_dir):
            logger.debug('Creating working directory %s' % work_dir)
            os.makedirs(work_dir)
        if not os.path.exists(os.path.join(work_dir, 'data')):
            os.makedirs(os.path.join(work_dir, 'data'))

        if parse_args().clear:
            master_run_directory = os.path.join(work_dir, 'runs')
            if os.path.exists(master_run_directory):
                shutil.rmtree(master_run_directory, ignore_errors=True)
            run_file = os.path.join(work_dir, 'data', 'all_runs.json')
            if os.path.exists(run_file):
                os.remove(run_file)
            cache_builds_directory = os.path.join(work_dir, 'cache')
            if os.path.exists(cache_builds_directory):
                shutil.rmtree(cache_builds_directory, ignore_errors=True)

PathManager.create_run_directory()
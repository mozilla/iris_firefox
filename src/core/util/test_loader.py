import importlib
import logging
import os
import pprint
import pytest
import sys
from functools import reduce

from src.core.util.path_manager import PathManager

logger = logging.getLogger(__name__)


def scan_all_tests():
    tests_directory = PathManager.get_tests_dir()
    logger.debug('Path %s found. Checking content ...', tests_directory)

    test_list = {}
    rootdir = tests_directory.rstrip(os.sep)
    start = rootdir.rfind(os.sep) + 1
    exclude_dirs = {'images', '.pytest_cache', '__pycache__'}
    exclude_files = {'__init__.py', 'pytest.ini', '.DS_Store'}

    for path, dirs, files in PathManager.sorted_walk(rootdir):
        [dirs.remove(d) for d in list(dirs) if d in exclude_dirs]
        [files.remove(d) for d in list(files) if d in exclude_files]

        folders = path[start:].split(os.sep)
        subdir = dict.fromkeys(files)
        parent = reduce(dict.get, folders[:-1], test_list)
        parent[folders[-1]] = subdir

        if len(files) > 0:
            if os.path.isdir(path):
                my_plugin = TestCollector()
                pytest.main(['--collect-only', '-p', 'no:terminal', path], plugins=[my_plugin])
                for module in my_plugin.get_collected_items():
                    try:
                        module_path = str(module.fspath)
                        module_name = os.path.basename(module_path)
                        temp = module_path.split('%stests%s' % (os.sep, os.sep))[1].split(module_name)[0]
                        package = os.path.join('tests', temp)
                        current_test = module.own_markers[0].kwargs
                        test_object = {'name': module_name, 'module': module_path,
                                       'description': current_test.get('description'),
                                       'package': package}
                        if not current_test.get('values'):
                            pass
                        else:
                            for value in current_test.get('values').kwargs:
                                test_object[value] = current_test.get('values').kwargs[value]
                        subdir[module_name] = test_object

                    except TypeError as e:
                        logger.warning('Error in test - %s: %s' % (module, e.message))
                    except AttributeError:
                        logger.warning('[%s] is not a test file. Skipping...', module)
    return test_list


class TestCollector:

    def __init__(self):
        self.collected = []

    def pytest_collection_modifyitems(self, items):
        for item in items:
            self.collected.append(item)

    def get_collected_items(self):
        return self.collected

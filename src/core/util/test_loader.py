import importlib
import logging
import os
import pprint
import sys
from functools import reduce

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


def scan_all_tests():
    tests_directory = PathManager.get_tests_dir()
    logger.debug('Path %s found. Checking content ...', tests_directory)

    test_list = {}
    rootdir = tests_directory.rstrip(os.sep)
    start = rootdir.rfind(os.sep) + 1
    exclude_dirs = {'images', '.pytest_cache', '__pycache__'}
    exclude_files = {'__init__.py', 'pytest.ini', '.DS_Store'}

    for path, dirs, files in sorted_walk(rootdir):
        [dirs.remove(d) for d in list(dirs) if d in exclude_dirs]
        [files.remove(d) for d in list(files) if d in exclude_files]

        folders = path[start:].split(os.sep)

        subdir = dict.fromkeys(files)

        parent = reduce(dict.get, folders[:-1], test_list)
        parent[folders[-1]] = subdir

        for module in files:

            try:
                module_path = os.path.relpath(path)
                module_name = module
                sys.path.append(module_path)
                current_module = importlib.import_module(module_name.split('.')[0])

                current_test = current_module.Test().details.kwargs

                test_object = {'name': module, 'module': current_module.__file__,
                               'description': current_test.get('description'),
                               'package': module_path}
                if not current_test.get('values').kwargs :
                    pass

                else:
                    for value in current_test.get('values').kwargs:
                        test_object[value]=current_test.get('values').kwargs[value]

                subdir[module] = test_object

            except TypeError as e:
                logger.warning('Error in test - %s: %s' % (module, e.message))
            except AttributeError:
                logger.warning('[%s] is not a test file. Skipping...', module)


    return test_list

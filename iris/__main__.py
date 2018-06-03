# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


import glob
import shutil
import sys
import tempfile

import coloredlogs

import firefox.app as fa
import firefox.downloader as fd
import firefox.extractor as fe
import test_runner
from api.core import *
from api.helpers.parse_args import parse_args
from firefox import cleanup

tmp_dir = None
restore_terminal_encoding = None
LOG_FILENAME = 'iris_log.log'
LOG_FORMAT = '%(asctime)s [%(levelname)s] [%(name)s] %(message)s'
logger = logging.getLogger(__name__)

coloredlogs.DEFAULT_LOG_FORMAT = LOG_FORMAT
coloredlogs.DEFAULT_FIELD_STYLES = {'levelname': {'color': 'cyan', 'bold': True},
                                    'name': {'color': 'cyan', 'bold': True}}
coloredlogs.DEFAULT_LEVEL_STYLES = {'warning': {'color': 'yellow', 'bold': True},
                                    'success': {'color': 'green', 'bold': True},
                                    'error': {'color': 'red', 'bold': True}}


def main(argv=None):
    """This is the main entry point defined in setup.py"""
    Iris()


class Iris(object):

    def __init__(self):
        self.args = parse_args()
        initialize_logger(LOG_FILENAME, self.args.level)
        self.init_tesseract_path()
        self.module_dir = get_module_dir()
        self.platform = get_platform()
        self.os = Settings.getOS()
        self.main()
        test_runner.run(self)

    def main(self, argv=None):
        global tmp_dir

        logger.debug('Command arguments: %s' % self.args)

        cleanup.init()
        Iris.fix_terminal_encoding()
        tmp_dir = self.__create_tempdir()

        # Create workdir (usually ~/.iris, used for caching etc.)
        # Assumes that no previous code must write to it.
        if not os.path.exists(self.args.workdir):
            logger.debug('Creating working directory %s' % self.args.workdir)
            os.makedirs(self.args.workdir)

        if self.args.firefox == 'local':
            # Use default Firefox installation
            logger.info('Running with default installed Firefox build')
            if Settings.getOS() == Platform.MAC:
                self.fx_app = self.get_test_candidate('/Applications/Firefox.app/Contents')
            elif Settings.getOS() == Platform.WINDOWS:
                if os.path.exists('C:\\Program Files (x86)\\Mozilla Firefox'):
                    self.fx_app = self.get_test_candidate('C:\\Program Files (x86)\\Mozilla Firefox')
                else:
                    self.fx_app = self.get_test_candidate('C:\\Program Files\\Mozilla Firefox')
            else:
                self.fx_app = self.get_test_candidate('/usr/lib/firefox')
        else:
            self.fx_app = self.get_test_candidate(self.args.firefox)

        self.fx_path = self.fx_app.exe
        self.version = self.fx_app.version
        self.build_id = self.fx_app.build_id

        return 0

    @staticmethod
    def __create_tempdir():
        """Helper function for creating the temporary directory.

        Writes to the global variable tmp_dir
        :return:
             Path of temporary directory.
        """
        temp_dir = tempfile.mkdtemp(prefix='iris_')
        logger.debug('Created temp dir "%s"' % temp_dir)
        return temp_dir

    @staticmethod
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

    @staticmethod
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

    @staticmethod
    def fix_terminal_encoding():
        """Helper function to set terminal to platform-specific UTF encoding."""
        global restore_terminal_encoding
        restore_terminal_encoding = Iris.get_terminal_encoding()
        if restore_terminal_encoding is None:
            return
        if os.path.exists('C:\\'):
            platform_utf_encoding = '65001'
        else:
            platform_utf_encoding = None
        if restore_terminal_encoding != platform_utf_encoding:
            Iris.set_terminal_encoding(platform_utf_encoding)

    def get_test_candidate(self, build):
        """Download and extract a build candidate.

        Build may either refer to a Firefox release identifier, package, or build directory.
        :param:
            build: str with firefox build
        :return:
            FirefoxApp object for test candidate
        """
        if os.path.isdir(build):
            candidate_app = fa.FirefoxApp(build, Settings.getOS(), False)
            return candidate_app
        else:
            platform = fd.FirefoxDownloader.detect_platform()
            if platform is None:
                logger.error('Unsupported platform: "%s"' % sys.platform)
                sys.exit(5)

            # `build` may refer to a build reference as defined in FirefoxDownloader,
            # a local Firefox package as produced by `mach build`, or a local build tree.
            if build in fd.FirefoxDownloader.build_urls:
                # Download test candidate by Firefox release ID
                logger.info('Downloading Firefox "%s" build for platform "%s"' % (build, platform))
                fdl = fd.FirefoxDownloader(self.args.workdir, cache_timeout=1 * 60 * 60)
                build_archive_file = fdl.download(build, self.args.locale, platform)
                if build_archive_file is None:
                    sys.exit(-1)
                # Extract candidate archive
                candidate_app = fe.extract(build_archive_file, Settings.getOS(), self.args.workdir,
                                           cache_timeout=1 * 60 * 60)
                candidate_app.package_origin = fdl.get_download_url(build, platform)
            elif os.path.isfile(build):
                # Extract firefox build from archive
                logger.info('Using file "%s" as Firefox package' % build)
                candidate_app = fe.extract(build, Settings.getOS(), self.args.workdir, cache_timeout=1 * 60 * 60)
                candidate_app.package_origin = build
                logger.debug('Build candidate executable is "%s"' % candidate_app.exe)
            elif os.path.isfile(os.path.join(build, 'mach')):
                logger.info('Using Firefox build tree at `%s`' % build)
                dist_globs = sorted(glob.glob(os.path.join(build, 'obj-*', 'dist')))
                if len(dist_globs) == 0:
                    logger.critical('"%s" looks like a Firefox build directory, but can\'t find a build in it' % build)
                    sys.exit(5)
                logger.debug('Potential globs for dist directory: %s' % dist_globs)
                dist_dir = dist_globs[-1]
                logger.info('Using "%s" as build distribution directory' % dist_dir)
                if 'apple-darwin' in dist_dir.split('/')[-2]:
                    # There is a special case for OS X dist directories:
                    # FirefoxApp expects OS X .dmg packages to contain the .app folder inside
                    # another directory. However, that directory isn't there in build trees,
                    # thus we need to point to the parent for constructing the app.
                    logger.info('Looks like this is an OS X build tree')
                    candidate_app = fa.FirefoxApp(os.path.abspath(os.path.dirname(dist_dir)), Settings.getOS(), True)
                    candidate_app.package_origin = os.path.abspath(build)
                else:
                    candidate_app = fa.FirefoxApp(os.path.abspath(dist_dir), Settings.getOS(), True)
                    candidate_app.package_origin = os.path.abspath(build)
            else:
                logger.critical('"%s" specifies neither a Firefox release, package file, or build directory' % build)
                logger.critical('Valid Firefox release identifiers are: %s' % ', '.join(fd.FirefoxDownloader.list()[0]))
                sys.exit(5)

            logger.debug('Build candidate executable is "%s"' % candidate_app.exe)
            if candidate_app.platform != platform:
                logger.warning('Platform mismatch detected')
                logger.critical('Running a Firefox binary for "%s" on a "%s" platform will probably fail' %
                                (candidate_app.platform, platform))
            return candidate_app

    @staticmethod
    def check_tesseract_path(dir_path):
        if not isinstance(dir_path, str):
            return False
        if not os.path.exists(dir_path):
            return False
        return True

    def init_tesseract_path(self):

        win_tesseract_path = 'C:\\Program Files (x86)\\Tesseract-OCR'
        osx_linux_tesseract_path_1 = '/usr/local/bin/tesseract'
        osx_linux_tesseract_path_2 = '/usr/bin/tesseract'

        path_not_found = False
        current_os = Settings.getOS()

        if current_os == Platform.WINDOWS:
            if self.check_tesseract_path(win_tesseract_path):
                pytesseract.pytesseract.tesseract_cmd = win_tesseract_path + '\\tesseract'
            else:
                path_not_found = True
        elif current_os == Platform.LINUX or current_os == Platform.MAC:
            if self.check_tesseract_path(osx_linux_tesseract_path_1):
                pytesseract.pytesseract.tesseract_cmd = osx_linux_tesseract_path_1
            elif self.check_tesseract_path(osx_linux_tesseract_path_2):
                pytesseract.pytesseract.tesseract_cmd = osx_linux_tesseract_path_2
            else:
                path_not_found = True
        else:
            path_not_found = True

        if path_not_found:
            logger.error('Unable to find tesseract')
            exit(1)


class RemoveTempDir(cleanup.CleanUp):
    """Class definition for cleanup helper responsible for deleting the temporary directory prior to exit."""

    @staticmethod
    def at_exit():
        global tmp_dir
        if tmp_dir is not None:
            logger.debug('Removing temp dir "%s"' % tmp_dir)
            shutil.rmtree(tmp_dir, ignore_errors=True)


class ResetTerminalEncoding(cleanup.CleanUp):
    """Class for restoring original terminal encoding at exit."""

    @staticmethod
    def at_exit():
        global restore_terminal_encoding
        if restore_terminal_encoding is not None:
            Iris.set_terminal_encoding(restore_terminal_encoding)


def initialize_logger_level(level):
    if level == 10:
        coloredlogs.install(level='DEBUG')
    elif level == 20:
        coloredlogs.install(level='INFO')
    elif level == 30:
        coloredlogs.install(level='WARNING')
    elif level == 40:
        coloredlogs.install(level='ERROR')
    elif level == 50:
        coloredlogs.install(level='CRITICAL')


def initialize_logger(output, level):
    if output:
        logging.basicConfig(filename=LOG_FILENAME, format=LOG_FORMAT)
    initialize_logger_level(level)

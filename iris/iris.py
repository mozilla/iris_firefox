# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


import argparse
import shutil
import tempfile

from firefox import cleanup
import firefox.app as fa
import firefox.downloader as fd
import firefox.extractor as fe

import test_runner
from api.core import *
from logger.iris_logger import *

logger = None
tmp_dir = None
restore_terminal_encoding = None


class Iris(object):

    def __init__(self):
        global logger
        self.parse_args()
        logger = initialize_logger(self)
        self.module_dir = get_module_dir()
        self.platform = get_platform()
        self.os = get_os()
        self.main()
        test_runner.run(self)

    def main(self, argv=None):
        global tmp_dir, logger

        logger.debug("Command arguments: %s" % self.args)

        cleanup.init()
        Iris.fix_terminal_encoding()
        tmp_dir = self.__create_tempdir()

        # Create workdir (usually ~/.iris, used for caching etc.)
        # Assumes that no previous code must write to it.
        if not os.path.exists(self.args.workdir):
            logger.debug('Creating working directory %s' % self.args.workdir)
            os.makedirs(self.args.workdir)

        if self.args.firefox:
            self.fx_path = self.get_test_candidate(self.args.firefox).exe
        else:
            # Use default Firefox installation
            logger.info("Running with default installed Firefox build")
            if get_os() == "osx":
                self.fx_path = '/Applications/Firefox.app/Contents/MacOS/firefox'
            elif get_os() == "win":
                if os.path.exists('C:\\Program Files (x86)\\Mozilla Firefox'):
                    self.fx_path = 'C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe'
                else:
                    self.fx_path = 'C:\\Program Files\\Mozilla Firefox\\firefox.exe'
            else:
                self.fx_path = '/usr/bin/firefox'

        return 0

    def __create_tempdir(self):
        """
        Helper function for creating the temporary directory.
        Writes to the global variable tmp_dir
        :return: Path of temporary directory
        """
        global logger
        temp_dir = tempfile.mkdtemp(prefix='iris_')
        logger.debug('Created temp dir `%s`' % temp_dir)
        return temp_dir

    @staticmethod
    def get_terminal_encoding():
        """
        Helper function to get current terminal encoding
        """
        global logger
        if sys.platform.startswith("win"):
            logger.debug("Running `chcp` shell command")
            chcp_output = os.popen("chcp").read().strip()
            logger.debug("chcp output: `%s`" % chcp_output)
            if chcp_output.startswith("Active code page:"):
                codepage = chcp_output.split(": ")[1]
                logger.debug("Active codepage is `%s`" % codepage)
                return codepage
            else:
                logger.warning("There was an error detecting the active codepage")
                return None
        else:
            logger.debug("Platform does not require switching terminal encoding")
            return None

    @staticmethod
    def set_terminal_encoding(encoding):
        """
        Helper function to set terminal encoding.
        """
        global logger
        if os.path.exists("C:\\"):
            logger.debug("Running `chcp` shell command, setting codepage to `%s`", encoding)
            chcp_output = os.popen("chcp %s" % encoding).read().strip()
            logger.debug("chcp output: `%s`" % chcp_output)
            if chcp_output == "Active code page: %s" % encoding:
                logger.debug("Successfully set codepage to `%s`" % encoding)
            else:
                logger.warning("Can't set codepage for terminal")

    @staticmethod
    def fix_terminal_encoding():
        """
        Helper function to set terminal to platform-specific UTF encoding
        """
        global restore_terminal_encoding
        restore_terminal_encoding = Iris.get_terminal_encoding()
        if restore_terminal_encoding is None:
            return
        if os.path.exists("C:\\"):
            platform_utf_encoding = "65001"
        else:
            platform_utf_encoding = None
        if restore_terminal_encoding != platform_utf_encoding:
            Iris.set_terminal_encoding(platform_utf_encoding)

    def get_test_candidate(self, build):
        """
        Download and extract a build candidate. build may either refer
        to a Firefox release identifier, package, or build directory.
        :param build: str with firefox build
        :return: FirefoxApp object for test candidate
        """
        global logger
        platform = fd.FirefoxDownloader.detect_platform()
        if platform is None:
            logger.error("Unsupported platform: `%s`" % sys.platform)
            sys.exit(5)

        # `build` may refer to a build reference as defined in FirefoxDownloader,
        # a local Firefox package as produced by `mach build`, or a local build tree.
        if build in fd.FirefoxDownloader.build_urls:
            # Download test candidate by Firefox release ID
            logger.info("Downloading Firefox `%s` build for platform `%s`" % (build, platform))
            fdl = fd.FirefoxDownloader(self.args.workdir, cache_timeout=1 * 60 * 60)
            build_archive_file = fdl.download(build, self.args.locale, platform)
            if build_archive_file is None:
                sys.exit(-1)
            # Extract candidate archive
            candidate_app = fe.extract(build_archive_file, self.args.workdir, cache_timeout=1 * 60 * 60)
            candidate_app.package_origin = fdl.get_download_url(build, platform)
        elif os.path.isfile(build):
            # Extract firefox build from archive
            logger.info("Using file `%s` as Firefox package" % build)
            candidate_app = fe.extract(build, self.args.workdir, cache_timeout=1 * 60 * 60)
            candidate_app.package_origin = build
            logger.debug("Build candidate executable is `%s`" % candidate_app.exe)
        elif os.path.isfile(os.path.join(build, "mach")):
            logger.info("Using Firefox build tree at `%s`" % build)
            dist_globs = sorted(glob.glob(os.path.join(build, "obj-*", "dist")))
            if len(dist_globs) == 0:
                logger.critical("`%s` looks like a Firefox build directory, but can't find a build in it" % build)
                sys.exit(5)
            logger.debug("Potential globs for dist directory: %s" % dist_globs)
            dist_dir = dist_globs[-1]
            logger.info("Using `%s` as build distribution directory" % dist_dir)
            if "apple-darwin" in dist_dir.split("/")[-2]:
                # There is a special case for OS X dist directories:
                # FirefoxApp expects OS X .dmg packages to contain the .app folder inside
                # another directory. However, that directory isn't there in build trees,
                # thus we need to point to the parent for constructing the app.
                logger.info("Looks like this is an OS X build tree")
                candidate_app = fa.FirefoxApp(os.path.abspath(os.path.dirname(dist_dir)))
                candidate_app.package_origin = os.path.abspath(build)
            else:
                candidate_app = fa.FirefoxApp(os.path.abspath(dist_dir))
                candidate_app.package_origin = os.path.abspath(build)
        else:
            logger.critical("`%s` specifies neither a Firefox release, package file, or build directory" % build)
            logger.critical("Valid Firefox release identifiers are: %s" % ", ".join(fd.FirefoxDownloader.list()[0]))
            sys.exit(5)

        logger.debug("Build candidate executable is `%s`" % candidate_app.exe)
        if candidate_app.platform != platform:
            logger.warning("Platform mismatch detected")
            logger.critical("Running a Firefox binary for `%s` on a `%s` platform will probably fail" %
                            (candidate_app.platform, platform))
        return candidate_app

    def parse_args(self):
        home = os.path.expanduser("~")
        release_choice, _, test_default = fd.FirefoxDownloader.list()

        LOG_LEVEL_STRINGS = ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG']

        def log_level_string_to_int(log_level_string):
            if not log_level_string in LOG_LEVEL_STRINGS:
                logger.error('Invalid choice: %s (choose from %s)', log_level_string, LOG_LEVEL_STRINGS)
                exit(1)

            log_level_int = getattr(logging, log_level_string, logging.INFO)
            assert isinstance(log_level_int, int)
            return log_level_int

        parser = argparse.ArgumentParser(description='Run Iris testsuite', prog='iris')
        parser.add_argument('-d', '--directory',
                            help='Directory where tests are located',
                            type=str, metavar='test_directory',
                            default=os.path.join("tests"))
        parser.add_argument('-t', '--test',
                            help='Test name',
                            type=str, metavar='test_name.py')
        parser.add_argument('-i', '--level',
                            help='Set the logging output level',
                            type=log_level_string_to_int,
                            dest='level',
                            default='INFO')
        parser.add_argument("-w", "--workdir",
                            help="Path to working directory",
                            type=os.path.abspath,
                            action="store",
                            default="%s/.iris" % home)
        parser.add_argument('-f', '--firefox',
                            help=("Firefox version to test. It can be one of {%s}, a package file, "
                                  "or a build directory (default: `%s`)") % (",".join(release_choice), test_default),
                            action='store')
        parser.add_argument("-l", "--locale",
                            help="Locale to use for Firefox",
                            type=str,
                            action="store",
                            default="en-US")
        self.args = parser.parse_args()


class RemoveTempDir(cleanup.CleanUp):
    """
    Class definition for cleanup helper responsible
    for deleting the temporary directory prior to exit.
    """
    global logger

    @staticmethod
    def at_exit():
        global tmp_dir
        if tmp_dir is not None:
            logger.debug('Removing temp dir `%s`' % tmp_dir)
            shutil.rmtree(tmp_dir, ignore_errors=True)


class ResetTerminalEncoding(cleanup.CleanUp):
    """
    Class for restoring original terminal encoding at exit.
    """

    @staticmethod
    def at_exit():
        global restore_terminal_encoding
        if restore_terminal_encoding is not None:
            Iris.set_terminal_encoding(restore_terminal_encoding)


def initialize_logger(app):
    global logger
    logger = getLogger(__name__)
    logger.setLevel(app.args.level)
    return logger


Iris()

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from distutils.spawn import find_executable
import logging
import os
import stat
import subprocess
import sys

import cache
from app import FirefoxApp
from downloader import FirefoxDownloader

from logger.iris_logger import *


logger = getLogger(__name__)


def extract(archive_file, workdir, cache_timeout=24*60*60, use_cache=True):

    """Extract a Firefox archive file into a subfolder in the given temp dir."""
    logger.info("Extracting Firefox archive `%s`" % archive_file)

    # Find 7zip binary
    sz_bin = find_executable("7z")
    if sz_bin is None:
        logger.critical("Cannot find 7zip")
        sys.exit(5)
    logger.debug("Using 7zip executable at `%s`" % sz_bin)

    # Name in cache is file name without extensions
    cache_id = os.path.basename(archive_file)
    cache_id = os.path.splitext(cache_id)[0]
    cache_id = os.path.splitext(cache_id)[0]

    dc = cache.DiskCache(os.path.join(workdir, "cache"), cache_timeout, purge=True)

    if not use_cache:
        # Enforce re-extraction even if cached
        dc.delete(cache_id)

    cache_dir = dc[cache_id]

    if cache_id not in dc:
        cmd = [sz_bin, "x", "-y", "-bd", "-o%s" % cache_dir, archive_file]
        logger.debug("Executing shell command `%s`" % " ".join(cmd))
        try:
            output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            logger.error("7zip failed: %s" % repr(e.output))
            raise Exception("Unable to extract Firefox archive")
        logger.debug("7zip succeeded: %s" % repr(output))

        # Check whether we have just extracted a tar file (from a .tar.bz2 archive)
        inner_tar = os.path.join(cache_dir, "%s.tar" % cache_id)
        if os.path.isfile(inner_tar):
            logger.debug("Running second 7zip pass on inner TAR archive `%s`" % inner_tar)
            cmd = [sz_bin, "x", "-y", "-bd", "-o%s" % cache_dir, inner_tar]
            logger.debug("Executing shell command `%s`" % " ".join(cmd))
            try:
                output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
            except subprocess.CalledProcessError as e:
                logger.error("7zip failed: %s" % repr(e.output))
                raise Exception("Unable to extract inner Firefox archive")
            logger.debug("7zip succeeded at second pass: %s" % repr(output))
            os.remove(inner_tar)

    app = FirefoxApp(cache_dir)

    # Workaround until 7zip learns to maintain file attributes
    os.chmod(app.exe, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)

    # Workaround for Mac
    if FirefoxDownloader.detect_os() == "osx":
        p = os.path.join (app.app_dir, "Contents", "MacOS", "plugin-container.app",
                          "Contents", "MacOS", "plugin-container")
        os.chmod (p, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)


    return app

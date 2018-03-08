# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import struct
import sys
import urllib2

import cache
from logger.iris_logger import *


logger = getLogger(__name__)


def get_to_file(url, filename):

    try:
        # TODO: Validate the server's SSL certificate
        req = urllib2.urlopen(url)
        file_size = int(req.info().get('Content-Length').strip())

        # Caching logic is: don't re-download if file of same size is
        # already in place. TODO: Switch to ETag if that's not good enough.
        # This already prevents cache clutter with incomplete files.
        if os.path.isfile(filename):
            if os.stat(filename).st_size == file_size:
                req.close()
                logger.warning('Skipping download, using cached file `%s` instead' % filename)
                return filename
            else:
                logger.warning('Purging incomplete or obsolete cache file `%s`' % filename)
                os.remove(filename)

        logger.debug('Downloading `%s` to %s' % (url, filename))
        downloaded_size = 0
        chunk_size = 32 * 1024
        with open(filename, 'wb') as fp:
            while True:
                chunk = req.read(chunk_size)
                if not chunk:
                    break
                downloaded_size += len(chunk)
                fp.write(chunk)

    except urllib2.HTTPError, err:
        if os.path.isfile(filename):
            os.remove(filename)
        logger.error('HTTP error: %s, %s' % (err.code, url))
        return None

    except urllib2.URLError, err:
        if os.path.isfile(filename):
            os.remove(filename)
        logger.error('URL error: %s, %s' % (err.reason, url))
        return None

    except KeyboardInterrupt:
        if os.path.isfile(filename):
            os.remove(filename)
        if sys.stdout.isatty():
            print
        logger.critical('Download interrupted by user')
        return None

    return filename


class FirefoxDownloader(object):

    __base_url = 'https://download.mozilla.org/?product=firefox' \
                '-{release}&os={platform}'
    build_urls = {
        'esr':     __base_url.format(release='esr-latest', platform='{platform}'),
        'release': __base_url.format(release='latest', platform='{platform}'),
        'beta':    __base_url.format(release='beta-latest', platform='{platform}'),
        'nightly': __base_url.format(release='nightly-latest', platform='{platform}')
    }
    __platforms = {
        'osx':     {'platform': 'osx', 'extension': 'dmg'},
        'linux':   {'platform': 'linux64', 'extension': 'tar.bz2'},
        'linux32': {'platform': 'linux', 'extension': 'tar.bz2'},
        'win':     {'platform': 'win64', 'extension': 'exe'},
        'win32':   {'platform': 'win', 'extension': 'exe'}
    }

    @staticmethod
    def list():
        build_list = FirefoxDownloader.build_urls.keys()
        platform_list = FirefoxDownloader.__platforms.keys()
        test_default = "nightly"
        return build_list, platform_list, test_default

    @staticmethod
    def detect_os():
        if os.path.exists("C:\\"):
            return "win"
        if os.path.exists("/Applications"):
            return "osx"
        else:
            return "linux"

    @staticmethod
    def detect_platform():
        if FirefoxDownloader.detect_os() == "osx":
            return "osx"
        if sys.maxsize == 2 ** 31:
            return FirefoxDownloader.detect_os() + "32"
        else:
            return FirefoxDownloader.detect_os()

    @staticmethod
    def get_download_url(build, platform=None):
        if platform is None:
            platform = FirefoxDownloader.detect_platform()
        # Internally we use slightly different platform naming, so translate
        # internal platform name to the platform name used in download URL.
        download_platform = FirefoxDownloader.__platforms[platform]['platform']
        if build in FirefoxDownloader.build_urls:
            url = FirefoxDownloader.build_urls[build].format(platform=download_platform)
            return url
        else:
            return None

    def __init__(self, workdir, cache_timeout=24*60*60):
        self.__workdir = workdir
        self.__cache = cache.DiskCache(os.path.join(workdir, "cache"), cache_timeout, purge=True)

    def download(self, release, locale, platform=None, use_cache=True):

        if platform is None:
            platform = FirefoxDownloader.detect_platform()

        if release not in self.build_urls:
            raise Exception("Failed to download unknown release `%s`" % release)
        if platform not in self.__platforms:
            raise Exception("Failed to download for unknown platform `%s`" % platform)

        extension = self.__platforms[platform]['extension']
        url = self.get_download_url(release, platform) + "&lang=" + locale
        cache_id = 'firefox-%s_%s.%s' % (release, platform, extension)

        # Always delete cached file when cache function is overridden
        if cache_id in self.__cache and not use_cache:
            self.__cache.delete(cache_id)

        # __get_to_file will not re-download if same-size file is already there.
        return get_to_file(url, self.__cache[cache_id])

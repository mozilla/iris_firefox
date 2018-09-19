# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import logging
import os
import platform
import sys
import urllib2

import cache

logger = logging.getLogger(__name__)


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
                logger.warning('Skipping download, using cached file "%s" instead' % filename)
                return filename
            else:
                logger.warning('Purging incomplete or obsolete cache file "%s"' % filename)
                os.remove(filename)

        logger.debug('Downloading "%s" to "%s"' % (url, filename))
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

    __archive_base_url = 'https://archive.mozilla.org/pub/firefox' \
                         '/{build}/{version}/{platform}'

    build_urls = {
        'esr': __base_url.format(release='esr-latest', platform='{platform}'),
        'release': __base_url.format(release='latest', platform='{platform}'),
        'beta': __base_url.format(release='beta-latest', platform='{platform}'),
        'nightly': __base_url.format(release='nightly-latest', platform='{platform}')
    }

    archive_build_urls = {
        'beta': __archive_base_url.format(build='releases', version='{version}', platform='{platform}'),
        'release': __archive_base_url.format(build='releases', version='{version}', platform='{platform}'),
        'nightly': __archive_base_url.format(build='nightly', version='{version}', platform='{platform}')
    }
    __platforms = {
        'osx': {'platform': 'osx', 'extension': 'dmg'},
        'linux': {'platform': 'linux64', 'extension': 'tar.bz2'},
        'linux32': {'platform': 'linux', 'extension': 'tar.bz2'},
        'win': {'platform': 'win64', 'extension': 'exe'},
        'win32': {'platform': 'win', 'extension': 'exe'}
    }

    __archive_platforms = {
        'osx': {'platform': 'mac', 'extension': 'dmg'},
        'linux': {'platform': 'linux-x86_64', 'extension': 'tar.bz2'},
        'linux32': {'platform': 'linux-i686', 'extension': 'tar.bz2'},
        'win': {'platform': 'win64', 'extension': 'exe'},
        'win32': {'platform': 'win32', 'extension': 'exe'}
    }

    def __init__(self, workdir, cache_timeout=24 * 60 * 60):
        self.__workdir = workdir
        self.__cache = cache.DiskCache(os.path.join(workdir, 'cache'), cache_timeout, purge=True)

    @staticmethod
    def list():
        build_list = FirefoxDownloader.build_urls.keys()
        platform_list = FirefoxDownloader.__platforms.keys()
        test_default = 'beta'
        return build_list, platform_list, test_default

    @staticmethod
    def detect_os():
        if os.path.exists('C:\\'):
            return 'win'
        if os.path.exists('/Applications'):
            return 'osx'
        else:
            return 'linux'

    @staticmethod
    def detect_platform():
        if FirefoxDownloader.detect_os() == 'osx':
            return 'osx'
        if platform.machine().endswith('64'):
            return FirefoxDownloader.detect_os()
        else:
            return FirefoxDownloader.detect_os() + '32'

    @staticmethod
    def get_download_url(build, locale, fx_version=None, platform=None):
        if platform is None:
            platform = FirefoxDownloader.detect_platform()

        # Internally we use slightly different platform naming, so translate
        # internal platform name to the platform name used in download URL.
        if fx_version is None:
            download_platform = FirefoxDownloader.__platforms[platform]['platform']
            if build in FirefoxDownloader.build_urls:
                url = FirefoxDownloader.build_urls[build].format(platform=download_platform)
                return url
            else:
                return None
        else:
            download_extension = FirefoxDownloader.__archive_platforms[platform]['extension']
            download_platform = FirefoxDownloader.__archive_platforms[platform]['platform']
            if platform is 'osx':
                installer = 'Firefox%20' + '%s.%s' % (fx_version, download_extension)
            elif platform == 'win' or platform == 'win32':
                installer = 'Firefox%20Setup%20' + '%s.%s' % (fx_version, download_extension)
            elif platform == 'linux' or platform == 'linux32':
                installer = 'firefox-' + '%s.%s' % (fx_version, download_extension)

            if build in FirefoxDownloader.archive_build_urls:
                url = FirefoxDownloader.archive_build_urls[build].format(version=fx_version, platform=download_platform)
                return url + '/' + locale + '/' + installer
            else:
                return None

    def download(self, build, locale, fx_version=None, platform=None, use_cache=True):
        if platform is None:
            platform = FirefoxDownloader.detect_platform()

        if build not in self.build_urls or build not in self.archive_build_urls:
            raise Exception('Failed to download unknown release "%s"' % build)
        if platform not in self.__platforms or platform not in self.__archive_platforms:
            raise Exception('Failed to download for unknown platform "%s"' % platform)

        if fx_version is None:
            extension = self.__platforms[platform]['extension']
            url = self.get_download_url(build, locale, fx_version, platform) + '&lang=' + locale
            cache_id = 'firefox-%s_%s_%s.%s' % (build, locale, platform, extension)
        else:
            extension = self.__archive_platforms[platform]['extension']
            url = self.get_download_url(build, locale, fx_version, platform)
            cache_id = 'Firefox_Setup_%s_%s.%s' % (locale, fx_version, extension)

        # Always delete cached file when cache function is overridden
        if cache_id in self.__cache and not use_cache:
            self.__cache.delete(cache_id)

        # __get_to_file will not re-download if same-size file is already there.
        return get_to_file(url, self.__cache[cache_id])

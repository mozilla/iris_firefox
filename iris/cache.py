# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import logging
import os
from shutil import rmtree
from time import time


logger = logging.getLogger(__name__)


class DiskCache(object):

    def __init__(self, root_directory, maximum_age=24*60*60, purge=False):
        global logger
        self.__root = os.path.abspath(root_directory)
        self.__maximum_age = maximum_age
        if not os.path.exists(self.__root):
            logger.debug('Creating cache directory %s' % self.__root)
            os.makedirs(self.__root)
        if purge:
            self.purge()

    def list(self):
        """Return list of IDs in cache"""
        return os.listdir(self.__root)

    def __clear(self):
        """Remove all entries from cache directory"""
        global logger
        logger.debug("Clearing cache directory `%s`" % self.__root)
        for cache_id in self:
            path = self[cache_id]
            if os.path.isdir(path):
                rmtree(path)
            else:
                os.remove(path)

    def delete(self, id_or_path=None):
        """
        Delete cache entries by ID or full path.
        Delete everything if no ID or path given.
        """
        if id_or_path is None:
            self.__clear()
            return
        path = self[id_or_path.lstrip(self.__root)]
        if os.path.isdir(path):
            rmtree(path)
        elif os.path.exists(path):
            os.remove(path)

    def purge(self, maximum_age=None):
        """Remove stale entries from cache directory"""
        global logger
        logger.debug("Purging stale cache entries from `%s`" % self.__root)
        if maximum_age is None:
            maximum_age = self.__maximum_age
        now = time()  # Current time as epoch
        stale_limit = now - maximum_age
        for cache_id in self:
            path = self[cache_id]
            mtime = os.path.getmtime(path)  # Modification time as epoch (might have just 1.0s resolution)
            if mtime < stale_limit:
                logger.debug('Purging stale cache entry `%s`' % cache_id)
                if os.path.isdir(path):
                    rmtree(path)
                else:
                    os.remove(path)

    def __iter__(self):
        """Iterate IDs of cache entries"""
        for name in self.list():
            yield name

    def __contains__(self, cache_id):
        """Check for presence of ID in cache"""
        return cache_id in self.list()

    def __getitem__(self, cache_id):
        """Return full path of cache entry (existing or not)"""
        return os.path.join(self.__root, cache_id)

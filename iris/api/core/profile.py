# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import subprocess

from distutils import dir_util
from distutils.spawn import find_executable
import shutil

from util.core_helper import *


class _IrisProfile(object):
    # Disk locations for both profile cache and staged profiles.
    RUN_DIRECTORY = get_current_run_dir()
    STAGED_PROFILES = os.path.join(get_module_dir(), 'iris', 'profiles')

    """These are profile options available to tests. With the exception of BRAND_NEW, 
    they are pre-configured, zipped profiles that are part of the source tree, unzipped 
    and uniquely created for each test. Profiles are saved to the current run directory, 
    and each is named after the test it was created for. 
    """

    BRAND_NEW = 'brand_new'
    LIKE_NEW = 'like_new'
    TEN_BOOKMARKS = 'ten_bookmarks'

    # We will make LIKE_NEW the default.
    DEFAULT = 'like_new'

    @staticmethod
    def _get_staged_profile(profile_name, path):
        sz_bin = find_executable('7z')
        logger.debug('Using 7zip executable at "%s"' % sz_bin)

        zipped_profile = os.path.join(Profile.STAGED_PROFILES, '%s.zip' % profile_name)

        cmd = [sz_bin, 'x', '-y', '-bd', '-o%s' % Profile.STAGED_PROFILES, zipped_profile]
        logger.debug('Unzipping profile with command "%s"' % ' '.join(cmd))
        try:
            output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            logger.error('7zip failed: %s' % repr(e.output))
            raise Exception('Unable to unzip profile')
        logger.debug('7zip succeeded: %s' % repr(output))

        # Find the desired profile
        from_directory = os.path.join(Profile.STAGED_PROFILES, profile_name)

        # Create a folder to hold that profile's contents.
        to_directory = path
        logger.debug('Creating new profile: %s' % to_directory)

        # Duplicate profile.
        dir_util.copy_tree(from_directory, to_directory)

        # Remove old unzipped directory.
        try:
            shutil.rmtree(from_directory)
        except WindowsError:
            # This error can happen, but does not affect Iris.
            logger.debug('Error, can\'t remove orphaned directory, leaving in place')

        # Remove Mac resource fork folders left over from ZIP, if present.
        resource_fork_folder = os.path.join(Profile.STAGED_PROFILES, '__MACOSX')
        if os.path.exists(resource_fork_folder):
            try:
                shutil.rmtree(resource_fork_folder)
            except WindowsError:
                # This error can happen, but does not affect Iris.
                logger.debug('Error, can\'t remove orphaned directory, leaving in place')

    def make_profile(self, template, module):
        parent, test = parse_module_path()
        parent_directory = os.path.join(Profile.RUN_DIRECTORY, parent)

        if not os.path.exists(parent_directory):
            os.makedirs(parent_directory)
        test_directory = os.path.join(parent_directory, test)
        os.mkdir(test_directory)
        profile_path = os.path.join(test_directory, 'profile')
        os.mkdir(profile_path)

        if template is _IrisProfile.BRAND_NEW:
            """Make new, unique profile."""
            logger.debug('Creating brand new profile: %s' % profile_path)
        elif template is _IrisProfile.LIKE_NEW:
            """Open a staged profile that is nearly new, but with some first-run preferences altered."""
            logger.debug('Creating new profile from LIKE_NEW staged profile')
            self._get_staged_profile(template, profile_path)
        elif template is _IrisProfile.TEN_BOOKMARKS:
            """Open a staged profile that already has ten bookmarks."""
            logger.debug('Creating new profile from TEN_BOOKMARKS staged profile')
            self._get_staged_profile(template, profile_path)
        else:
            raise ValueError('No profile found: %s' % template)

        return profile_path


Profile = _IrisProfile()

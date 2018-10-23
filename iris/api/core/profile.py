# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from distutils import dir_util
from distutils.spawn import find_executable
import os
import shutil

from util.core_helper import *


class _IrisProfile(object):

    """These are profile options available to tests. With the exception of BRAND_NEW, 
    they are pre-configured, zipped profiles that are part of the source tree, unzipped 
    and uniquely created for each test. Profiles are saved to the current run directory, 
    and each is named after the test it was created for. 
    """

    """A completely new profile from scratch."""
    BRAND_NEW = 'brand_new'

    """Profile that has had minimal configuration, but would be set up to avoid things like the default browser dialog 
    (browser.shell.checkDefaultBrowser;false); dealing with different warnings (browser.tabs.warnOnClose;false),
    (browser.tabs.warnOnCloseOtherTabs;false), (browser.warnOnQuit;false) and possibly first-run tour items."""
    LIKE_NEW = 'like_new'

    """Identical to LIKE_NEW but has had the activity of bookmarking ten sites."""
    TEN_BOOKMARKS = 'ten_bookmarks'

    """We will make LIKE_NEW the default profile."""
    DEFAULT = 'like_new'

    """Save profile locations in case we wish to delete them later."""
    _profiles = []

    @staticmethod
    def _get_staged_profile(profile_name, path):
        """
        Internal-only method used to extract a given profile.
        :param profile_name:
        :param path:
        :return:
        """
        """Disk location for staged profiles."""
        _staged_profiles = os.path.join(IrisCore.get_module_dir(), 'iris', 'profiles')

        sz_bin = find_executable('7z')
        logger.debug('Using 7zip executable at "%s"' % sz_bin)

        zipped_profile = os.path.join(_staged_profiles, '%s.zip' % profile_name)

        cmd = [sz_bin, 'x', '-y', '-bd', '-o%s' % _staged_profiles, zipped_profile]
        logger.debug('Unzipping profile with command "%s"' % ' '.join(cmd))
        try:
            output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            logger.error('7zip failed: %s' % repr(e.output))
            raise Exception('Unable to unzip profile.')
        logger.debug('7zip succeeded: %s' % repr(output))

        """Find the desired profile."""
        from_directory = os.path.join(_staged_profiles, profile_name)

        """Create a folder to hold that profile's contents."""
        to_directory = path
        logger.debug('Creating new profile: %s' % to_directory)

        """Duplicate profile."""
        dir_util.copy_tree(from_directory, to_directory)

        """Remove old unzipped directory."""
        try:
            shutil.rmtree(from_directory)
        except WindowsError:
            # This error can happen, but does not affect Iris.
            logger.debug('Error, can\'t remove orphaned directory, leaving in place.')

        """Remove Mac resource fork folders left over from ZIP, if present."""
        resource_fork_folder = os.path.join(_staged_profiles, '__MACOSX')
        if os.path.exists(resource_fork_folder):
            try:
                shutil.rmtree(resource_fork_folder)
            except WindowsError:
                # This error can happen, but does not affect Iris.
                logger.debug('Error, can\'t remove orphaned directory, leaving in place.')

    def make_profile(self, template):
        """
        Internal-only method used to create profiles on disk.
        :param template:
        :return:
        """
        test_directory = IrisCore.make_test_output_dir()

        if parse_args().save:
            profile_path = os.path.join(test_directory, 'profile')
            os.mkdir(profile_path)
        else:
            profile_temp = IrisCore.get_tempdir()
            parent, test = IrisCore.parse_module_path()
            profile_path = os.path.join(profile_temp, '%s_%s' % (parent, test))
            os.mkdir(profile_path)

        if template is _IrisProfile.BRAND_NEW:
            """Make new, unique profile."""
            logger.debug('Creating brand new profile: %s' % profile_path)
        elif template is _IrisProfile.LIKE_NEW:
            """Open a staged profile that is nearly new, but with some first-run preferences altered."""
            logger.debug('Creating new profile from LIKE_NEW staged profile.')
            self._get_staged_profile(template, profile_path)
        elif template is _IrisProfile.TEN_BOOKMARKS:
            """Open a staged profile that already has ten bookmarks."""
            logger.debug('Creating new profile from TEN_BOOKMARKS staged profile.')
            self._get_staged_profile(template, profile_path)
        else:
            raise ValueError('No profile found: %s' % template)

        if not parse_args().save:
            self._manage_profile_cache(profile_path)
        return profile_path

    @staticmethod
    def _manage_profile_cache(path):
        """
        Internal-only method used to delete old profiles that are not in use.
        :param path:
        :return:
        """
        Profile._profiles.append(path)
        if len(Profile._profiles) > 1:
            shutil.rmtree(Profile._profiles.pop(0), ignore_errors=True)


Profile = _IrisProfile()

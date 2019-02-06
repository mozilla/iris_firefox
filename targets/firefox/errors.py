# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


class TestRailError(Exception):
    """Exception raised when TestRail Api returns an error."""
    def __init__(self, message):
        """Create an exception instance."""
        Exception.__init__(self, message)


class BugManagerError(Exception):
    """Exception raised when an bug_manager error occurs."""
    def __init__(self, message):
        """Create an exception instance."""
        Exception.__init__(self, message)

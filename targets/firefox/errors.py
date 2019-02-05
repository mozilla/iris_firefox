# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from src.core.api.errors import *


class TestRailError(Exception):
    """Exception raised when TestRail Api returns an error."""
    def __init__(self, message):
        """Create an instance of an exception."""
        Exception.__init__(self, message)

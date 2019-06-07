# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


class FindError(Exception):
    """Exception raised when a Location, Pattern, image or text is not found."""
    def __init__(self, message):
        """Create an exception instance."""
        Exception.__init__(self, message)


class ConfigError(Exception):
    """Exception raised if there is unexpected behavior when manipulating config files."""
    def __init__(self, message):
        """Create an exception instance."""
        Exception.__init__(self, message)


class APIHelperError(Exception):
    """Exception raised when an API helper returns an error."""
    def __init__(self, message):
        """Create an exception instance."""
        Exception.__init__(self, message)


class EmailError(Exception):
    """Exception raised when an email error occurs."""
    def __init__(self, message):
        """Create an exception instance."""
        Exception.__init__(self, message)


class ScreenshotError(Exception):
    """Exception raised when an screenshot error occurs."""
    def __init__(self, message):
        """Create an exception instance."""
        Exception.__init__(self, message)

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


class FindError(Exception):
    """Exception raised when a Location, Pattern, image or text is not found."""
    pass


class ConfigError(Exception):
    """Exception raised if there is unexpected behavior when manipulating config files."""
    pass


class APIHelperError(Exception):
    """Exception raised when an API helper returns an error."""
    pass

class TestRailError(Exception):
    """Exception raised when TestRail Api returns an error."""
    pass
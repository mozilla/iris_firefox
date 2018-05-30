class FindError(Exception):
    """Exception raised when a Location, Pattern, image or text is not found."""
    pass


class ConfigError(Exception):
    """Exception raised if there is unexpected behavior when manipulating config files."""
    pass


class UnsupportedMethodError(Exception):
    """Exception raised for unsupported methods."""
    pass


class UnsupportedAttributeError(Exception):
    """Exception raised for unsupported attributes."""
    pass


class UnsupportedClassMethodError(Exception):
    """Exception raised for unsupported classmethods."""
    pass


class APIHelperError(Exception):
    """Exception raised when an API helper returns an error."""
    pass

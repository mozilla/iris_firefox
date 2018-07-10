import platform
import logging

logger = logging.getLogger(__name__)

INVALID_GENERIC_INPUT = 'Invalid input'
INVALID_NUMERIC_INPUT = 'Expected numeric value'


def get_os():
    """Get the type of the operating system your script is running on."""
    current_system = platform.system()
    current_os = ''
    if current_system == 'Windows':
        current_os = 'win'
    elif current_system == 'Linux':
        current_os = 'linux'
    elif current_system == 'Darwin':
        current_os = 'osx'
    else:
        logger.error('Iris does not yet support your current environment: ' + current_system)

    return current_os

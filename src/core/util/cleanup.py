# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import atexit
import logging
import signal
import sys

logger = logging.getLogger(__name__)
__cleanup_done = False


def init():
    """Register cleanup handler."""
    logger.debug('Registering cleanup handler')

    global __cleanup_done
    __cleanup_done = False

    # Will be OS-specific, see https://docs.python.org/2/library/signal.html
    atexit.register(cleanup_handler)
    signal.signal(signal.SIGTERM, cleanup_handler)
    if sys.platform == 'darwin' or 'linux' in sys.platform:
        # SIGHUP is not available on Windows
        signal.signal(signal.SIGHUP, cleanup_handler)


def cleanup_handler():
    """The cleanup handler that runs when process terminates."""
    global __cleanup_done
    if not __cleanup_done:
        __cleanup_done = True
        for child in CleanUp.__subclasses__():
            child.at_exit()


class CleanUp(object):
    """When process terminates, .at_exit() is called on every subclass."""
    pass

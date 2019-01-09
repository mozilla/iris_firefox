import logging
from iris2.core.helpers.rectangle import Rectangle
from iris2.core.helpers.os_helpers import MONITORS

logger = logging.getLogger(__name__)


class Display:
    def __init__(self, screen_id: int = 0):
        self.screen_id = screen_id
        self.screen_list = [item for item in MONITORS]
        self.bounds = _get_screen_details(self.screen_list, self.screen_id)

    def __repr__(self):
        return '%s(%r, %r, %r, %r)' % (self.__class__.__name__, self.bounds.x, self.bounds.y, self.bounds.width,
                                       self.bounds.height)


def _get_screen_details(screen_list: list, screen_id: int) -> Rectangle:
    """Get the screen details.

    :param screen_list: List with available monitors.
    :param screen_id: Screen ID.
    :return: Region object.
    """
    if len(screen_list) == 0:
        logger.error('Could not retrieve list of available monitors.')
    else:
        try:
            details = screen_list[screen_id]
            return Rectangle(details['left'], details['top'], details['width'], details['height'])
        except IndexError:
            logger.warning('Screen %s does not exist. Available monitors: %s'
                           % (screen_id, ', '.join(_get_available_monitors(screen_list))))
    return Rectangle()


def _get_available_monitors(screen_list: list) -> list:
    """Return a list with all the available monitors."""
    res = []
    for screen in screen_list:
        res.append('Screen(%s)' % screen_list.index(screen))
    return res

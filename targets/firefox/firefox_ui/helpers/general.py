from src.core.api.errors import APIHelperError
from src.core.api.finder.finder import wait
from src.core.api.finder.pattern import Pattern
from targets.firefox.firefox_ui.nav_bar import NavBar


def confirm_firefox_launch(image=None):
    """Waits for firefox to exist by waiting for the iris logo to be present.
    :param image: Pattern to confirm Firefox launch
    :return: None.
    """
    if image is None:
        image = NavBar.HOME_BUTTON

    try:
        wait(image, 60)
    except Exception:
        raise APIHelperError('Can\'t launch Firefox - aborting test run.')

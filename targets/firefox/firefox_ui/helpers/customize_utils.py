# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.firefox_ui.helpers.general import *
from targets.firefox.firefox_ui.nav_bar import NavBar

logger = logging.getLogger(__name__)


class CustomizePage(object):
    AUTO_HIDE = Pattern('auto_hide.png')
    OVERFLOW_MENU_ICON = Pattern('overflow_menu_icon.png')


def auto_hide_download_button():
    click_hamburger_menu_option('Customize...')

    try:
        wait(NavBar.DOWNLOADS_BUTTON, 10)
        logger.debug('Downloads button found in the \'Customize\' page.')
    except FindError:
        raise APIHelperError('Downloads button not found in the \'Customize\' page.')

    click(NavBar.DOWNLOADS_BUTTON)
    try:
        wait(CustomizePage.AUTO_HIDE, 5)
        logger.debug('The auto-hide button found in the page.')
    except FindError:
        raise APIHelperError('The auto-hide button not found in the page.')

    click(CustomizePage.AUTO_HIDE)
    close_customize_page()

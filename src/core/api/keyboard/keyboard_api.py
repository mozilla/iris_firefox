# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


import time

import pyautogui
import pyperclip

from src.core.api.errors import FindError
from src.core.api.keyboard.key import KeyModifier
from src.core.api.keyboard.keyboard import type
from src.core.api.os_helpers import OSHelper
from src.core.api.settings import Settings

DEFAULT_KEY_SHORTCUT_DELAY = 0.1
pyautogui.FAILSAFE = False


def paste(text: str):
    """
    :param text: Text to be pasted.
    :return: None.
    """

    pyperclip.copy(text)
    text_copied = False
    wait_scan_rate = float(Settings.wait_scan_rate)
    interval = 1 / wait_scan_rate
    max_attempts = int(Settings.auto_wait_timeout * wait_scan_rate)
    attempt = 0

    while not text_copied and attempt < max_attempts:
        if pyperclip.paste() == text:
            text_copied = True
        else:
            time.sleep(interval)
            attempt += 1

    if not text_copied:
        raise FindError('Paste method failed.')

    if OSHelper.is_mac():
        type(text='v', modifier=KeyModifier.CMD)
    else:
        type(text='v', modifier=KeyModifier.CTRL)

    pyperclip.copy('')

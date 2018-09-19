# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from iris.api.core.platform import Platform
from iris.api.core.settings import get_os


class FirefoxApp(object):
    """Class holding information about an extracted Firefox application directory."""

    BETA = 'beta'
    RELEASE = 'release'
    NIGHTLY = 'nightly'
    ESR = 'esr'
    CHANNELS = [BETA, ESR, NIGHTLY, RELEASE]
    LOCALES = ['en-US', 'zh-CN', 'es-ES', 'de', 'fr', 'ru', 'ar', 'ko', 'pt-PT', 'vi', 'pl', 'tr', 'ro',
               'ja-JP-mac' if get_os() == Platform.MAC else 'ja']

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


import logging
import unittest

import pytest

from src.core.api.finder.finder import *
from src.core.api.finder.pattern import Pattern
from src.core.api.keyboard.key import *
from src.core.api.keyboard.keyboard import type, key_down, key_up
from src.core.api.mouse.mouse import *
from src.core.api.mouse.mouse import Mouse
from src.core.api.screen.region import *
from src.core.api.screen.screen import *
from src.core.api.enums import *
from src.core.api.errors import *
from src.core.api.location import *
from src.core.api.os_helpers import *
from src.core.api.rectangle import *
from src.core.api.settings import Settings
from funcy import compose


mylogger = logging.getLogger(__name__)


class BaseTest:

    def setup(self):
        return

    @classmethod
    def setup_class(cls):
        return

    @classmethod
    def teardown_class(cls):
        return

    def setup_method(self, method):
        return

    def teardown_method(self, method):
        return

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


# This class is used to wrap methods around the Sikuli API

from sikuli import *
import os
from platform import *

Settings.MoveMouseDelay = 0
Settings.ActionLogs = False
Settings.InfoLogs = False
Settings.DebugLogs = False


Key = Sikuli.Key
Screen = Sikuli.Screen


def close():
    Sikuli.Screen().type("w", Sikuli.KeyModifier.CMD + Sikuli.KeyModifier.SHIFT)

def add_image_path(path):
    Sikuli.addImagePath(path)


def Pattern(path):
    return Sikuli.Pattern(path)


def get_screen():
    return Sikuli.Screen()


def get_key():
    return Sikuli.Key()


def find(pattern):
    return Sikuli.Screen().find(pattern)


def findAll(pattern):
    return Sikuli.Screen().findAll(pattern)


def wait(pattern, timeout):
    return Sikuli.Screen().wait(pattern, timeout)


def waitVanish(pattern, timeout):
    return Sikuli.Screen().waitVanish(pattern, timeout)


def exists(pattern, timeout):
    return Sikuli.Screen().exists(pattern, timeout)


def click(pattern):
    return Sikuli.Screen().click(pattern)


def doubleClick(pattern):
        return Sikuli.Screen().doubleClick(pattern)


def rightClick(pattern):
    return Sikuli.Screen().rightClick(pattern)


def hover(pattern):
    return Sikuli.Screen().hover(pattern)


def dragDrop(pattern1, pattern2):
    return Sikuli.Screen().dragDrop(pattern1, pattern2)


def type(pattern=None, text=None, modifier=None):
    if pattern is None:
        if modifier is None:
            return Sikuli.Screen().type(text)
        else:
            return Sikuli.Screen().type(text, modifier)
    else:
        if modifier is None:
            if text is None:
                return Sikuli.Screen().type(pattern)
            else:
                return Sikuli.Screen().type(pattern, text)
        else:
            if text is None:
                return Sikuli.Screen().type(pattern, modifier)
            else:
                return Sikuli.Screen().type(pattern, text, modifier)


def paste(pattern=None, text=None, modifier=None):
    if pattern is None:
        if modifier is None:
            return Sikuli.Screen().paste(text)
        else:
            return Sikuli.Screen().paste(text, modifier)
    else:
        if modifier is None:
            if text is None:
                return Sikuli.Screen().paste(pattern)
            else:
                return Sikuli.Screen().paste(pattern, text)
        else:
            if text is None:
                return Sikuli.Screen().paste(pattern, modifier)
            else:
                return Sikuli.Screen().paste(pattern, text, modifier)

import pyautogui
from core_helper import get_os


class Platform(object):
    """Class that holds all supported operating systems (HIGH_DEF = High definition displays)."""
    WINDOWS = 'win'
    LINUX = 'linux'
    MAC = 'osx'
    ALL = get_os()
    HIGH_DEF = not (pyautogui.screenshot().size == pyautogui.size())
    SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()
    LOW_RES = (SCREEN_WIDTH < 1280 or SCREEN_HEIGHT < 800)

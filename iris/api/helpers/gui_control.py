import pyautogui
pyautogui.FAILSAFE = False


def hover(x=0, y=0, duration=0.0, tween='linear', pause=None):
    pyautogui.moveTo(x, y, duration, tween, pause)

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


# This class is used to wrap methods around the Sikuli API

import platform
import sys
import pyautogui
import numpy as np
import time
from helpers.image_remove_noise import process_image_for_ocr
import pytesseract
import cv2
from logger.iris_logger import *

try:
    import Image
except ImportError:
    from PIL import Image

pyautogui.FAILSAFE = False
DEFAULT_IMG_ACCURACY = 0.8
IMAGES = {}
DEBUG = True

logger = getLogger(__name__)


def get_os():
    current_system = platform.system()
    current_os = ''
    if current_system == "Windows":
        current_os = "win"
        pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract'
    elif current_system == "Linux":
        current_os = "linux"
        pytesseract.pytesseract.tesseract_cmd = '/usr/local/bin/tesseract'
    elif current_system == "Darwin":
        current_os = "osx"
        pytesseract.pytesseract.tesseract_cmd = '<unknown>'
    else:
        logger.error("Iris does not yet support your current environment: " + current_system)

    return current_os


def get_platform():
    return platform.machine()


def get_module_dir():
    return os.path.realpath(os.path.split(__file__)[0] + "/../..")


CURRENT_PLATFORM = get_os()
PROJECT_BASE_PATH = os.path.abspath(os.path.join("iris", os.pardir))
for root, dirs, files in os.walk(PROJECT_BASE_PATH):
    for file_name in files:
        if file_name.endswith(".png"):
            if CURRENT_PLATFORM in root:
                IMAGES[file_name] = os.path.join(root, file_name)

screenWidth, screenHeight = pyautogui.size()

'''
Private function: Saves PIL input image for debug
'''


def _save_debug_image(image):
    if DEBUG is True:
        file_path = PROJECT_BASE_PATH + '/last_grabbed_region.png'
        try:
            os.remove(file_path)
        except:
            pass
        image.save(file_path)


'''
Private function: Returns a screenshot from tuple (topx, topy, bottomx, bottomy)

Input : Region tuple (topx, topy, bottomx, bottomy)
Output : PIL screenshot image

Ex: _region_grabber(region=(0, 0, 500, 500)) 
'''


def _region_grabber(coordinates):
    x1 = coordinates[0]
    y1 = coordinates[1]
    width = coordinates[2] - x1
    height = coordinates[3] - y1
    grabbed_area = pyautogui.screenshot(region=(x1, y1, width, height))
    _save_debug_image(grabbed_area)
    return grabbed_area


'''
Private function: Search for needle in stack
'''


def _match_template(search_for, search_in, precision=DEFAULT_IMG_ACCURACY):
    img_rgb = np.array(search_in)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(search_for, 0)

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    if max_val < precision:
        return [-1, -1]
    return max_loc


'''
Private function: Search for an image on the entire screen.
    For searching in a certain area use _image_search_area

Input :
    image_path : Path to the searched for image.
    precision : OpenCv image search precision.

Output :
   Top left coordinates of the element if found as [x,y] or [-1,-1] if not.

'''


def _image_search(image_path, precision=DEFAULT_IMG_ACCURACY):
    in_region = _region_grabber(coordinates=(0, 0, screenWidth, screenHeight))
    return _match_template(image_path, in_region, precision)


'''
Private function: Search for an image within an area

Input :
    image_path :  Path to the searched for image.
    x1 : Top left x area value.
    y1 : Top left y area value.
    x2 : Bottom right x area value.
    y2 : Bottom right y area value.
    precision : OpenCv image search precision.
    in_region : an already cached region, in this case x1,y1,x2,y2 will be ignored

Output :
    Top left coordinates of the element if found as [x,y] or [-1,-1] if not.
'''


def _image_search_area(image_path, x1, y1, x2, y2, precision=DEFAULT_IMG_ACCURACY, in_region=None):
    if in_region is None:
        in_region = _region_grabber(coordinates=(x1, y1, x2, y2))
    return _match_template(image_path, in_region, precision)


'''
Private function: Search for an image on entire screen continuously until it's found.

Input :
    image_path : Path to the searched for image.
    time_sample : Waiting time after failing to find the image .
    precision :  OpenCv image search precision.

Output :
     Top left coordinates of the element if found as [x,y] or [-1,-1] if not.

'''


def _image_search_loop(image_path, time_sample, attempts=5, precision=0.8):
    pos = _image_search(image_path, precision)
    tries = 0
    while (pos[0] == -1) and (tries < attempts):
        time.sleep(time_sample)
        pos = _image_search(image_path, precision)
        tries += 1
    return pos


'''
Private function: Search for an image on a region of the screen continuously until it's found.

Input :
    time : Waiting time after failing to find the image. 
    image_path :  Path to the searched for image.
    x1 : Top left x area value.
    y1 : Top left y area value.
    x2 : Bottom right x area value.
    y2 : Bottom right y area value.
    precision : OpenCv image search precision.
    in_region : An already cached region, in this case x1,y1,x2,y2 will be ignored

Output :
    Top left coordinates of the element if found as [x,y] or [-1,-1] if not.

'''


def _image_search_region_loop(image_path, time_sample, x1, y1, x2, y2, precision=DEFAULT_IMG_ACCURACY, in_region=None):
    pos = _image_search_area(image_path, x1, y1, x2, y2, precision, in_region)
    while pos[0] == -1:
        time.sleep(time_sample)
        pos = _image_search_area(image_path, x1, y1, x2, y2, precision, in_region)
    return pos


'''

Private function: Clicks on a image

input :
    image_path : Path to the clicked image ( only for width,height calculation)
    pos : Position of the top left corner of the image [x,y].
    action : button of the mouse to activate : "left" "right" "middle".
    time : Time taken for the mouse to move from where it was to the new position.
'''


def _click_image(image_path, pos, action, time_stamp):
    img = cv2.imread(image_path)
    height, width, channels = img.shape
    pyautogui.moveTo(pos[0] + width / 2, pos[1] + height / 2, time_stamp)
    pyautogui.click(button=action)


# @todo map data form image_to_data and search for text input
def text_search(text, debug):
    screenWidth, screenHeight = pyautogui.size()
    screencapture = _region_grabber(coordinates=(screenWidth / 2 - 400, 50, screenWidth / 2, 800))
    screencapture.save('./debug.png')

    optimized_ocr_image = process_image_for_ocr('./debug.png')
    cv2.imwrite("./debug_ocr_ready.png", optimized_ocr_image)
    print(pytesseract.image_to_data(Image.fromarray(optimized_ocr_image)))


'''

Sikuli wrappers
- wait
- waitVanish
- click
- exists 

'''


def wait(image_name, max_attempts, time_sample=0.5, precision=DEFAULT_IMG_ACCURACY):
    image_path = IMAGES[image_name]
    image_found = _image_search_loop(image_path, time_sample, max_attempts, precision)
    if (image_found[0] != -1) & (image_found[1] != -1):
        return True
    return False


def waitVanish(image_name, max_attempts, time_sample=0.5, precision=DEFAULT_IMG_ACCURACY):
    logger.debug("Wait vanish for: " + image_name)
    pattern_found = wait(image_name, 1)
    tries = 0
    while (pattern_found is True) and (tries < max_attempts):
        time.sleep(time_sample)
        pattern_found = wait(image_name, 1)
        tries += 1

    return pattern_found


# @todo Search in regions for faster results
def click(image_name):
    logger.debug("Try click on: " + image_name)
    image_path = IMAGES[image_name]
    pos = _image_search(image_path)
    if pos[0] != -1:
        _click_image(image_path, pos, "left", 0)
        time.sleep(1)
        return pos
    else:
        logger.debug("Image not found:", image_name)


def exists(image_name, time_sample):
    return wait(image_name, 3, 0.5)


# @todo to take in consideration the number of screens
def get_screen():
    if DEBUG is True:
        pyautogui.displayMousePosition()
    return _region_grabber(coordinates=(0, 0, screenWidth, screenHeight))


def hover(x=0, y=0, duration=0.0, tween='linear', pause=None):
    x = int(x)
    y = int(y)
    pyautogui.moveTo(x, y, duration, tween, pause)


def typewrite(text, interval=0.02):
    logger.debug("Type: " + str(text))
    pyautogui.typewrite(text, interval)


def press(key):
    logger.debug("Press: " + key)
    pyautogui.keyDown(str(key))
    pyautogui.keyUp(str(key))
